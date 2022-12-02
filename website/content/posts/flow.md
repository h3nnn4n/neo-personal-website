---
title: "Flow field"
date: 2018-09-22
tags: ["javascript", "physics", "visual", "creative"]
draft: false
---

One of the most popular coding exercises out there is a Flow Field. The main idea behind that is
to generate a [vector field](https://en.wikipedia.org/wiki/Vector_field)
randomly, which is very often based on [Perlin Noise](https://en.wikipedia.org/wiki/Perlin_noise).
Then a set of particles are placed on the vector field and they are free to move along it,
where the vector field determines the force placed upon the particle.
To make things more dynamic and alive it is possible to vary the vector field
over time. The result is something like the interactive animation written
in JavaScript and using the [p5js](https://p5js.org/) library, as shown below.

The Vector Field is drawn on the screen to better illustrate how it works. It can be disabled using the
checkbox `Show Field`, which will generate a much more pleasing visualization. The `Wrap Noise` checkbox
control if the vector is symmetrical along the axes or not. Having it symmetrical makes it more well
behaved overall, where the flow connects across the borders. This makes possible for a particle that
leaves the screen on the right, to continue its journey when it appears on the right. Now, if
this option is turned off, the field on the left may be pointing in the opposite direction that
the particle came from, possibly in a way that it will get stuck in the borders.

<iframe class='iframe' src="/flow-net/src/index.html" width="800" height="700" frameBorder="0"></iframe>

The slider that shows `500 Particles` is auto explanatory, it shows the number of active particles.
Another control is the `Noise Level` slider. This one control how noisy the vector field is. The smaller
this value is, the straighter the trajectory will be. On the other hand, a high value makes the
field very noisy which will make the particles to behave very errantly. Finally. the `Flow Rate`
determines how fast the field changes in function of time. Have it set to 0 and the flow will be static.
If this is set to its maximum value then the particles will switch its direction very often, even if
the field is not noisy.

An interesting aspect that I implemented here is different properties for the particles. The attent reader
may have noticed that some particles behave slightly different than other. With the blue and green ones
having a more straight trajectory, while the pink and orange ones making more shape turns. This is due
to differences in mass between the particles. The lighter ones undergo a more rapid change in velocity
while the heavier ones may need a lucky sequence of vectors to make it turn a sharp 90 degrees turn.

Writing this was pretty much my first experience with JavaScript in a `just for fun` context.
This project also got me willing again to do some creative coding, so expect to see some more around.
Check out the [Dancing room](Dancing Room) for a similar project and the
[creative](http://localhost:1313/tags/creative) tag.
