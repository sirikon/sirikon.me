---
title: PID 1 Bash script for Docker containers explained line by line
date: 2024-10-10 20:00
---

You wake up one morning, feeling bit spicy, daring to break rules, but you aren't the bravest one in town, so you choose something easy: "Let's break that rule about only running one process in a container".

As an actual person that works in this garbage fire called software development and NOT a Medium shitposter, this is something that you might run into.

Having multiple processes in a container involves that, at least, one of them should be the ruling one, PID `1`. (Sorry anarchists and flat organizations believers, reality exists, go cry at your V for Vendetta poster).

If you're still with me, a PID `1` process in a Docker container should:

- Be the first one running (duh).
- Start the rest of processes.
- Repeat every signal that it receives. (If you receive a SIGINT, you send a SIGINT to every other process).
- Trigger a SIGINT to all the processes as soon as one of them exits for any reason.
- Wait for the rest of processes to finish before exiting.
- Be the last one running, because if it exits early, everything exits immediately without graceful stops, and we don't want that.

You could solve these problems, and many more, with something like [systemd](https://systemd.io/) or [s6-overlay](https://github.com/just-containers/s6-overlay), but for me that's way too much for starting a couple of processes together.

Let's solve this the way absolutely nothing should ever be solved in this century: With **Bash**.

```bash
#!/usr/bin/env bash
set -euo pipefail

function main {
  trap 'true' SIGINT SIGTERM

  exec service-a &
  exec service-b &

  wait -n || true
  kill -s SIGINT -1
  wait
}

main "$@"
```

Let's analyze the script line by line.

```bash
#!/usr/bin/env bash
```

When using this text file as an executable, thanks to the first two bytes `#!`, the operating system (and by operating system I mean the UNIX family) will use the rest of the line as the interpreter for the given file. `#!` is called the **shebang**.

By using `/usr/bin/env bash` instead of something more direct like `/bin/bash`, we're leveraging on the environment's PATH variable to decide where is the `bash` executable that should be used as the interpreter.

Thanks to that shebang, running `./script.sh` is equivalent to running `/usr/bin/env bash script.sh`.

```bash
set -euo pipefail
```

> The Set Builtin: This builtin is so complicated that it deserves its own section. —— [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin)

The builtin command [`set`](https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin) in Bash is used for configuring the running bash shell. The flags I'm using here mean:

- `-e`: Exit immediately whenever a command exits with a non zero exit code.
- `-u`: Using unset variables is considered an error.
- `-o`: Yo dawg, I heard you like options, so I put options in your options. (Yes, nested options.)
  - `pipefail`: The exit value of a pipeline is the exit value of the last command in the pipeline that exits with a non zero status (or zero if everything exits with zero).

It's a sane default that I always use for Bash scripts.

```bash
function main {
  # ...
}

# ...

main "$@"
```

I always create a function called `main` at the top for two reasons:

First, it allows me to define helper functions that are written _after_ the place they're being used, and I think that having that part of the script be the first one visible on the file is useful for knowing what the fuck is going on. In this example there are no helper functions, but try to use your crippled imagination for once.

Second, combining this with a `main "$@"` at the end of the file, we're forcing Bash to read and interpret the whole file. Why is this important? Bash interprets files lazily, whenever it needs to interpret more code, it will keep reading the file, it doesn't matter if the file changed during the execution. If a Bash script starts, encounters a `sleep 10`, the script file changes, and after 10 seconds the Bash script continues, it will read the **new** contents of the file starting from whatever byte it stopped reading when found the `sleep 10`, actually executing a mix of the old and new script, making a lot of really funny bugs to debug.

By the way, `"$@"` is for passing all the arguments that the script receives to the `main` function. `$@` is the argument collection, and by putting it between double quotes `""` it gets expanded to a list of arguments without resplitting them on whitespace.

```bash
trap 'true' SIGINT SIGTERM
```

The [`trap`](https://www.gnu.org/software/bash/manual/bash.html#index-trap) builtin allows us to execute a command whenever a signal happens, "trapping" the signal.

In this case, we don't want to do anything special. Trapping `SIGINT` and `SIGTERM` and running the command `true` ([which does nothing, successfully](https://linux.die.net/man/1/true)) is enough. We just want to run _anything_ here, so it triggers a silly little detail that will be explained when we arrive to the `wait` calls.

```bash
exec service-a &
exec service-b &
```

"You said it was explained line by line and that's two lines" shut up.

This is where we define all the processes that we want to run in the container, but with two details.

The ampersand (`&`) at the end indicates that the command that precedes it will be executed in the background, in another shell.

We don't need a second shell in this case, as we're just executing a single command. To solve this, we can use [`exec`](https://www.gnu.org/software/bash/manual/bash.html#index-exec), which replaces the running shell with the new command, giving it its own PID.

Now the command's PPID (parent PID) is `1` instead of having a bash shell in the middle doing nothing and having to deal with repeating signals again to the child process.

```bash
wait -n || true
```

The [`wait`](https://www.gnu.org/software/bash/manual/bash.html#index-wait) builtin is for waiting for all the background processes to end, and returning the same exit code of the last background process that exited. This command stops the script's execution until all the background processes have ended.

If you add the `-n` flag it will wait until **a single** background process ends. As soon as a background process ends, any background process, it will return the same exit code as the process that finished.

We don't care about the exit code of `wait -n`, and due to the `set -e` explained before, if it returns something different than zero, it will exit the script immediately, so we put a `|| true` at the end (which is bash's way of saying "do _this_ in case _that_ fails"), with a `true`, because [it does nothing, successfully](https://linux.die.net/man/1/true), ignoring the possible error.

**But there is a catch**. Remember the section about `trap` and how we talked about a silly little detail?

Here's an excerpt from Bash source code:

> POSIX.2 says: When the shell is waiting (by means of the wait utility)
  for asynchronous commands to complete, the reception of a signal for
  which a trap has been set **shall cause the wait utility to return
  immediately** with an exit status greater than 128, after which the trap
  associated with the signal shall be taken. —— [Bash source code](http://git.savannah.gnu.org/cgit/bash.git/tree/builtins/wait.def?id=6794b5478f660256a1023712b5fc169196ed0a22#n170). The text can be read [here](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html) as well. Chapter "2.12 Signals and Error Handling".

When a `trap`, any `trap`, traps a signal, any `wait` running in the shell will return immediately. That's why we only needed to run `true` on the `trap` before, because its mere existence was enough.

Now, when a background process exits, or when a signal is received, we'll stop blocking the script and continue to the next line, which conveniently is...

```bash
kill -s SIGINT -1
```

The [`kill`](https://www.gnu.org/software/bash/manual/bash.html#index-kill) builtin is for sending signals to processes, and accepts many ways to define the signals and the processes to target.

`-s SIGINT` stablishes that we're sending a `SIGINT`s to the target processes.

Now, we're not sending a `SIGINT` to a single process. We want to send it to every background process at once. There's a special notation for `kill`: By giving it negative numbers in the PID argument, we instruct `kill` to interpret it as a PGID (process group id). So `-1` means the PGID `1`, right?

__Well__, there's a special case in `kill` for the pid `-1`:

>  -1: All processes with a PID larger than 1 are signaled. —— [kill(1) man page](https://www.man7.org/linux/man-pages/man1/kill.1.html)

We're not signaling the process group `1`, we're signaling every process with a PID larger than `1`, which is, every process except the script. Exactly what we need. Convenient!

```bash
wait
```

And finally, we make a final call to `wait`. At this point, for one reason or another, all the background processes have been signaled and are, supposedly, stopping gracefully, and we're just waiting for all of them to finish.

When the `wait` finishes, the script finishes.

The End.

**UPDATE**: What if you want to do the same thing (a script goberning a bunch of child processes), but without it being a PID 1 process?

Just change this line:

```bash
kill -s SIGINT -1
```

So it looks like this:

```bash
kill -s SIGINT -$$
```

Replacing `-1` with `-$$` we'll be sending `SIGINT`s to all the processes inside the Bash script's process group. Notice that the Bash script itself is inside this process group, so it will receive the `SIGINT`. This is not a problem because we're trapping all `SIGINT`s and doing [nothing, successfully](https://linux.die.net/man/1/true), so it won't matter, but take it into consideration if you want to change the signals used.

And in case you use `kill` without specifying a signal, remember to use `--` so it doesn't think that `-$$` is the signal.

> either a signal must be specified first, or the argument must be preceded by a `--` option, otherwise it will be taken as the signal to send. —— [kill man page](https://www.man7.org/linux/man-pages/man1/kill.1.html)
