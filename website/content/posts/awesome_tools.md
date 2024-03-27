---
title: "Awesome tools I found over the years"
date: 2024-03-02
tags: ["tools"]
draft: false
---

Hi :)

This is a list of awesome tools I have found over the years that are incredibly
useful, time savers, game changers or just plain fun to use. Often I forget
about then and then at some point my brain goes like "I am pretty sure I knew a
tool for this". This list serves both as a reminder to future me, and as a way
to share these tools with the world. As I find more tools, I will add them
here, or maybe update the information regarding the tools. It will be an ever
changing post.

Here it goes:

- [rr](https://rr-project.org/): GDB extension that allows recording and
  replaying program runs, to deterministacally reproduce bugs. Has GDB
  scripting support. Has a chaos mode that helps reproduce nondeterministic
  bugs in multi-threaded programs.

- [multitime](https://tratt.net/laurie/src/multitime/): Time on steroids. Can
  run a program multiple times and report some basic statistics (min, max, avg,
  stddev).

- [autoclave](https://github.com/silentbicycle/autoclave): Runs a program
  multiple times until failure, stores the `stdout` and `stderr` and can attach
  a debugger automatically when the program crashes.

- [tmate](https://mxschmitt.github.io/action-tmate/): Allows SSH-ing into a
  github actions runner for debugging (or whatever else you need to do).
