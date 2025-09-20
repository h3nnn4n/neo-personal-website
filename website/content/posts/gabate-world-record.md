---
title: "Getting a world record of most Gameboy Tetris lines cleated"
date: 2025-09-15
draft: true
---

In 2000 I started a project called [Garapa](https://github.com/h3nnn4n/garapa).
A Gameboy emulator. It turned out to be pretty accurate, passing some very
demanding precision tests. After it being complete enough, I found myself in
need of a new project. After some thought, I started experimenting with having
the emulator play itself. Not only that, to learn how to do so. This project
got the name of [Gabate](https://github.com/h3nnn4n/gabate).

Gabate means `Genetic Algorithm Based Agent for TEtris`. Not a very catchy
name. Now a days it supports other learning methods which I deem to be more
efficient for the problem at hand. The modern implementation task as an arg a
json setting with a set of weights. These weights are used to select and tune
[feature
functions](https://github.com/h3nnn4n/gabate/blob/develop/src/feature_functions.h),
of which there are many. These were collected from multiple papers and some I
created on my own. Lets say there is a function that returns the sum of the
height of all columns. This one usually has a negative score, since it is bad
to have pieces stacked high. On the other side, having variability in height is
usually good, because it allows pieces to fit in more easily, so this one tends
to be positive. Another obvious one, is whether the move will clear a line.
This pretty much is always positive, although not necessary. A combination of
other fature functions can implicitly combine the knowledge to complete lines.

The learning process is an optimization problem. Given a set of feature
functions, find the weights that maximize the number of lines cleared (could be
points too). Sounds simple, but there is a catch: The function is stochastic.
If a set of weights is evaluated 10 times it will likely get 10 different
results (unless it is a bad set where it will gets lots of numbers in the low
tens). To mitigate that, multiple evaluations can be taken, but now there is
the question of how to aggregate those values. The `minumum` might prefer
agents that are more consistent. While `maximum` would prefer agents that have
a higher variance and can score higher. I haven't confirmed if this is how it
works, but I suspect it is not. Getting the `average` or `median` is probably
closer to the ideal. Using the average makes the score more prone to be
affected by outliers, while the median is more resilient against it. The score
distribution seems to be `log-normal`, or similar. Taking 10 or so samples
seems to be good enough for an accurate evaluation, since most of the
measurements will fall near the peak instead of the tail, and any outliers will
be ignored when taking the median.

When optimizing agents and doing multiple evaluations, because of the
distribution of scores, it is likely that at least one or two agents will take
much longer to evaluate. So if evaluating 10 times concurrently, it still
has to wait for the longest one to conclude. To make things more efficient,
methods that have a population of agents and can continuously provide new
agents for evaluation are the optimum approach. Lets take the genetic algorithm
as an example. It has the concept of generations, where all agents are evaluated
together and we have to wait for them all. This can be wasteful. Now, for an
algorithm such as a random search, we can continuously evaluate new agents
as they are generated. This likely achieves maximum efficency.

I believe that I hold the world record for most lines cleared in the Gameboy
tetris. No confirmation but I couldn't find anything highers than ~700 lines.
The process to obtain this world record was relativelly straight forward.
First, a random search was made until an agent with a median of 10 had a score
in the 2000~3000 lines range. The next step, a grid search was made, tunning
each variable independently, one after the other. As a last step, the optimum
agent was ran in a loop until the record was broken.


- Actually get a world record
- Recording
