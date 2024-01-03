---
title: Python Simplified Concurrency Guide
---

So you want to do multiple tasks concurrently in Python because your ugly ass code should be bothering as many CPU cores as possible all the time with its mere existence.

In Python there are three modules that will help you to achieve your perfectly sane goals.

## [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)

Imagine executing the `python ...` command multiple times, but them having a way to talk with each other to sync and pass information.

Creating processes here mean creating actual operating system processes, each with it's own Python interpreter, memory, and all the overhead involved.

Processes look all the same to the OS, and the OS will assign CPU time to each process by its own criteria.

You can communicate between processes by:

- Passing [pickle](https://docs.python.org/3/library/pickle.html)-able values to `Process(args=...)` and receive them at the start.
- Passing to `Process(args=...)` mechanisms like a `Lock` or a `Queue` to sync or pass information around with them afterwards.
- Using the `fork` or `forkserver` start methods which involve making a complete copy of the memory of an already initialized process instead of starting a pristine new one. After the fork, each process will continue evolving it's memory independently. It's like parallel universes with a common starting point, but without Marvel fucking it up.

## [threading](https://docs.python.org/3/library/threading.html)

Creating threads here mean creating actual operating system threads. This way we have a single process with a single Python interpreter and memory space, but with multiple threads working on it independently.

Threads look all the same to the OS, and the OS will assign CPU time to each thread by its own criteria.

The OS doesn't know that there is a thread with stuff to do and a thousand threads just waiting for IO. They look all the same. Don't expect the scheduler to know better and assign CPU time sooner to the thread that can continue working.

You won't achieve any parallelism with threading, because threads under a Python process are synced with the Global Interpreter Lock. Only one thread is allowed to do work at a time.

You'll probably need some Locks to prevent pesky race conditions. Remember, threads share memory.

You can communicate between threads by... just leaving values there or using Locks and Queues for safety. Again, threads share memory, remember?!

## [asyncio](https://docs.python.org/3/library/asyncio.html)

So there's this thing popularized by JavaScript called an Event Loop in which instead of endlessly waiting for IO you can pause the execution and let the runtime call you back whenever it's done so more tasks can be performed during that time. It's Starbucks putting your name on the cup and calling you back whenever your Pumpkin Spice Latte is ready but without child labor in under-developed economies.

Python has exactly that, even with the `async/await` keywords, because life is nothing without [color](https://journal.stuffwithstuff.com/2015/02/01/what-color-is-your-function/).

The event loop is implemented in Python and uses a mechanism provided by the operating system to have a map of pending IO and functions to be called back whenever the pending IO is completed. This is the only way in Python to have concurrency with scheduling that knows which tasks can continue and which ones can't because their IO hasn't resolved yet.

This means that every IO operation needs to be performed "the async way" to take advantage of the event loop instead of blocking the thread.

Asyncio only affects how you interact with IO. It doesn't affect how you communicate between different parts of your program. Just be aware that an event loop runs on a single thread.

## Which one should I use

Make your own informed decissions, for fuck's sake.
