---
title: PID 1 Bash script for Docker containers explained line by line
date: 2024-10-10 20:00
---

You wake up one morning, feeling bit spicy, daring to break rules, but you aren't the bravest one in town, so you choose something easy: "Let's break that rule about only running one process in a container".

As an actual person that works in this garbage fire called software development and NOT a Medium shitposter, this is something that you might run into.

Having multiple processes in a container involves that, at least, one of them should be the ruling one, PID 1. (Sorry anarchists and flat organizations believers, reality exists, go cry at your V for Vendetta poster).

If you're still with me, a PID 1 process in a Docker container should:

- Be the first one running (duh).
- Start the rest of processes.
- Repeat every signal that it receives. (If you receive a SIGINT, you send a SIGINT to every other process).
- Trigger a SIGINT to all the processes as soon as one of them exits for any reason.
- Wait for the rest of processes to finish before exiting.
- Be the last running.

You could solve this, and much more, with something like systemd or [s6-overlay](https://github.com/just-containers/s6-overlay), but for me that's way too much for starting a couple of processes together.

Let's solve this the way absolutely nothing should be ever solved in this century: With **Bash**.

```bash
#!/usr/bin/env bash
set -euo pipefail

function main {
  trap 'true' SIGINT SIGTERM

  start-service-a &
  start-service-b &

  wait -n || true
  kill -s SIGINT -1
  wait
}

function start-service-a {
  exec service-a
}

function start-proxy {
  exec service-b
}

main "$@"
```

Let's analyze the script line by line.

```bash
#!/usr/bin/env bash
```

When using this text file as an executable, thanks to the first bytes `#!`, the operating system (and by operating system I mean the UNIX family) will use the rest of the line as the interpreter for the given file. `#!` is called the **shebang**.

By using `/usr/bin/env bash` instead of something more direct like `/bin/bash`, we're leveraging on the environment's PATH variable to decide where is the `bash` executable that should be used as the interpreter.

Thanks to that shebang, running `./script.sh` is equivalent to running `/usr/bin/env bash script.sh`.

```bash
set -euo pipefail
```

> The Set Builtin: This builtin is so complicated that it deserves its own section. —— [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin)

The builtin command [`set`](https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin) in Bash is used for configuring the running bash shell. The flags I'm using here mean:

- `-e`: Exit immediately whenever a command exits with an exit code non zero.
- `-u`: Using unset variables is considered an error.
- `-o`: Yo dawg, I heard you like options, so I put options in your options. (Yes, nested options.)
  - `pipefail`: The exit value of a pipeline is the exit value of the last command in the pipeline that exits with a non zero status (or zero if everything exits with zero).

It's a sane default that I always use for Bash scripts.

```bash
function main {
  # ...
}
```

I always create a function called `main` for two reasons:

First, it allows me to define helper functions _after_ using them, and I think that having that part of the script be the first one visible on the file is useful for knowing that the fuck is going on.

Second, combining this with a `main "$@"` at the end of the file, we're forcing Bash to read and interpret the whole file. Why is this important? Bash interprets files lazily, whenever it needs to interpret more code, it will keep reading the file, it doesn't matter if the file changed during the execution. If a Bash script starts, encounters a `sleep 10`, the script file changes, and after 10 seconds the Bash script continues, it will read the **new** contents of the file starting from whatever byte it stopped reading when found the `sleep 10`, actually executing a mix of the old and new script, making a lot of really funny bugs to debug.

```bash
trap 'true' SIGINT SIGTERM
```

