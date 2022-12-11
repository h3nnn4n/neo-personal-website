---
title: "Dancing Room Zero"
date: 2018-09-29
tags: ["javascript", "physics", "visual", "creative"]
draft: false
---

After writing a bit about the original Dancing with Friends and Enemies and my [reimplementation](/post/dancing-room/)
I decided to try to implement something more close to the original. The first version used [matter.js](http://brm.io/matter-js/)
which added a different behavior style to the particles while being somewhat similar to the original.

<iframe src="{% static 'external/dancing-friends-zero/src/index.html' %}" width="720" height="630" frameBorder="0"></iframe>

I was satisfied with the results and glad to be able to keep its original behavior while adding my own touch to it.
However, the whole thing was quite heavy due to the JS physics engine. Furthermore, things like angular momentum,
velocity and acceleration made the whole thing too finicky to adjust. Since it required lots of computation time per frame,
having the number of particles adaptable was something that I desired, but the physics engine made it hard to adapt.
The change in the number of particles required that I changed some parameters like the particle weight. In the end, the
system was good but not too easy to change. This led me to reimplement it using pretty much the same approach as the original.
It simply updates the position based on the simple set rules. It moves a big distance towards the particle that it likes, then it
takes a small step away from the particle it is afraid off, and then it takes another small step towards the center.

This small change made the whole system much lighter to run and less sensitive about the parameters. Now it can support a few hundred
to a thousand particles. It can adapt the number of particles on the fly based on the computer performance without changing
the overall behavior. And it shows a more lifelike behavior overall. I am quite pleased with the result.
