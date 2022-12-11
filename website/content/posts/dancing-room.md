---
title: "Dancing Room"
date: 2018-09-23
tags: ["javascript", "physics", "visual", "creative"]
draft: false
---

A few years ago I found a thread on the Wolfram forum about
[swarm intelligence](https://en.wikipedia.org/wiki/Swarm_intelligence)
and [emergent behavior](http://www.patternsinnature.org/Book/EmergentPatterns.html),
two things that I enjoy a lot. The title of the thread
was something like ''Dancing With Friends and Enemies'' and it does not exist anymore
as far as I can tell. However, I was able to find a copy [here](http://kaurov.com/wordpress/?p=1096).
The idea is pretty simple and below you can see my reinterpretation of it.

<iframe src="{% static 'external/Dancing-Rooms/src/index.html' %}" width="700" height="670" frameBorder="0"></iframe>

The behavior of the original system is based on a very simple set of rules, which I will quote from
Simon Woods here:

> 1000 dancers assume random positions on the dance-floor. Each randomly
> chooses one “friend” and one “enemy”. At each step every dancer moves 0.5%
> closer to the centre of the floor, then takes a large step towards their
> friend and a small step away from their enemy. At random intervals one dancer
> re-chooses their friend and enemy. Here is the dance…

And the original Mathematica code is the following:

```f#
n = 5000;
r := RandomInteger[{1, n}];
f := (#/(.007 + Sqrt[#.#])) &amp; /@ (x[[#]] - x) &amp;;
s := With[{r1 = r}, p[[r1]] = r; q[[r1]] = r];
x = RandomReal[{-1, 1}, {n, 2}];
{p, q} = RandomInteger[{1, n}, {2, n}];
Graphics[{PointSize[0.008], Opacity[.5], Dynamic[If[r &lt; 100, s];
Point[x = 0.995 x + 0.02 f[p] - 0.01 f[q]]]}, PlotRange -&gt; 2]
```

Now, when I reimplemented it, all was done from the top of my head. I could not find
the original post or anything else mentioning it. All I could remember was that
the particles moved towards __friends__ and away from __enemies__. Also, they
moved towards the __center__ a little bit. While on the original each particle had one
__enemie__, I set each particle to have 30 enemies. This, in my opinion, made the system
more dynamic, where one or a set of particles can become isolated from the others.
Another difference is that the particles are attracted both to the center of the __room__
and the __center of mass__ of all particles. This helps them to stay grouped but
nevertheless move around. I also used [matter.js](http://brm.io/matter-js/), a physics
engine. The use of it allows for the particle to have mass, friction, partially
elastic collisions, inertia and more, which gave the system further complexity.
Furthermore, the use of the physics engine and the rectangular shape for the
particles allows them to bump and even get stuck at each other, adding
an extra dimension to their collective behavior.

The system is full of complex behaviors. Initially, the system just looks like a mess of particles
running around. While some little time it is possible to see that the particles are chasing one
another. Sometimes a circle-like pattern appears. And sometimes it looks like there is
one particle running away while several particles are chasing after it. These two are
my favorite patterns so far. The chasing behavior led a [friend](http://khskarl.me/) of mine to say
''It looks like [boids](https://en.wikipedia.org/wiki/Boids), but trying to kill each other''.

A special situation appears when the system reassigns the __friends__ and __enemies__
of the particles. Visually it looks like the particles running away got
tired of fleeing and are taking revenge upon their previous chasers.
Since the reassignment happens gradually, it looks like a single particle
is taking revenge and charging at the other particles. And then inspiring the others
to do the same.

So far this project has been very amusing. I spent hours already just looking at
the behavior of the swarm and tweaking their behavior.
My reinterpretation / reimplementation full source code
is available [here](https://github.com/h3nnn4n/Dancing-Rooms).
It is written in JavaScript and it uses [matter.js](http://brm.io/matter-js/) for the
physics and [p5js](https://p5js.org/) for the graphics. Enjoy and thank you.
