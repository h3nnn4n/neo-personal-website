---
title: "Cracks"
date: 2018-10-10
tags: ["javascript", "visual", "creative"]
draft: false
---

Recently after looking at the works of [inconvergent](https://inconvergent.net/generative/fractures/)
I decided to try to implement some of the techniques that he uses.
This one here was inspired mostly by [fractures](https://inconvergent.net/generative/fractures/).
While his algorithm for this is something that I want to explore in the future, the work
here is somewhat different from what he did.

<iframe class='iframe' src="/cracks/index.html" width="700" height="680" frameBorder="0"></iframe>

My implementation works in a much simpler way. It generates a line equation with random coefficients
and it picks a random point in this line. From this random point, it finds the intersections to the
right and left and draws a line segment connecting these two intersection points. And this is it :D
A very simple logic and a very simple implementation, which produces a very interesting result.
As usual, the implementation is opensource and available [here](https://github.com/h3nnn4n/cracks).
