---
title: "Project Aratu: yet another 3dof hexapod"
date: 2023-06-24
tags: ["robotics", "project", "aratu"]
draft: true
---

I once read something along the lines of "some people can only live they
childhood dreams after they become adults". Well, child me really liked robots
and wanted to build some. Of course at the time I didn't have the know-how nor
the resources required. Heck, much of the technology available today didn't
even exist back then or wasn't available commercialy at a developing country
like Brazil. Now, a lot has changed. We have microcontrollers 10x faster than
computers were back then, and they are wide available worldwide (when there
isn't a chip shortage going on anyways). I am also fortunate enough to be able
to afford to build a relativelly complex robot, and more importantly I have
developed all the skills and meta skills.

All projects need a name. Given that the project itself is a 6 legged robot,
taking inspiration from nature is an obvious step. I wanted something that
was a reference to something Brazilian, while being memorable in both
Portuguese and English. After some research, I settled on "Aratu", which is
a crab found from the south of Brazil up to Florida. It is found both in the
pacific and atlatic coasts. Although crabs are decapods, while my project
is an Hexapod, I decided to go with it. Most 6 legged insects I found didn't
meet the "being memorable" criteria.

Considering that relativelly little experience with robotics and I am not
much the research first kind of person, one priority was to be able to
iterate, fail and recover fast. I found that I am often more productive
when I go ahead and just try to make things and go as far as I can without
losing momentum. Once I hit a blocker that I can't easily resolve, then I
start researching on how to fix that particular problem. Rinse and repeat.
The coxa and tibia bones were two such cases were the first designs failed,
but I was able to fix them without having to change the other components.
The robot body was implemented having a grid of holes spaces 10mm apart
to allow attaching things that I didn't forsee, without having to print
new parts. This came in very handy.

<div class="container-fluid">
  <div class="row">
    <div class="col">
      <img
        class="img-fluid" src="{% static 'images/aratu_1/side_leg_view.png' %}"
        alt="Side view of the robot leg, with all the bone lengths measured."
      ></img>
    </div>
  </div>
  <div class="row">
    <div class="col">
      <img
        class="img-fluid" src="{% static 'images/aratu_1/top_leg_view__sliced_.png' %}"
        alt="Top view of the robot leg, with all the bone lengths measured."
      ></img>
    </div>
  </div>
</div>
</br>

TODO: pics of the old leg with a short tibia, and the long curved ones.

During prototyping I took the first dev board I found, which happened to be an
Arduino Uno R3. With it I was able to implement the (Forward
Kinematics)[https://en.wikipedia.org/wiki/Forward_kinematics] routine, which is
relatively straightforward. Even on the relatively weak 8bit AVR
microcontroller running at 16MHz and without floating point arithmetic support
the FK can be solved more than a thousand times per second. The (Inverse
Kinematics)[https://en.wikipedia.org/wiki/Inverse_kinematics] model isn't so
simple though, and it can vary a lot if the leg model changes. Given my
Optimization background, I decided to implement a numerical solution instead of
an analytical one (keeping in sync with the modern software development
approach of spending CPU time to save Engineering time). The IK solver couldn't
run fast enough even for a single leg, but with some tricks the situation
improved. The solver uses a poor's man gradient descent (more like a greedy
search), which can take advantage of previously found solutions. Given that in
50 ms or so the leg can only move so far, the solver can start there and try to
find the new updated position. This works very fast in most cases. Another
simple optimizations can be used too, like having an acceptable error in the
position. For cheap servos this is specially relevant, since having the exact
angles down to 6 decimal places won't improve things if the servo can be a
couple of degrees off from where it should be. Another way is to timeout the
solver and return the best solution found so far, and on the next update
continue from there. This helps with long moves where the movement is
interpolated. This allowed the IK solved to run fast enough on the Uno for a
single leg to validate the physical construction of the leg, the electronics
and the code.

TODO: Single IK test video

Despite the optimizations, it was very unlikely that the Uno would be able to
keep up with 6 legs to control. This was quickly proven when I tried 3 legs.
Time to upgrade. My choice was the (Teensy
4.1)[https://www.pjrc.com/store/teensy41.html], a very capable 32bits
microcontroller having a cloc of 600 MHz, with floating point support and even
branch prediction. It has more features that I could ever want. It is even
superscalar, meaning that it can execute more than one instruction at the same
time under ideal circumstances. A quick benchmark between the Uno and the
Teensy had very impressive results. The Uno could do on average 1355 FK solves
per second, while the teensy could do 1086956. About 800x faster. One funny bug
happened due to the Teensy being too fast. To move at a constant speed, the IK
has to run periodically, but since there are no real guarantees on how long it
will take to run again, it needs to account for the time between updates. On
the Uno, this was usually in the 5~50ms range. For the teensy, it would often
be 0ms, causing it to not move at all. The Uno required timeouts to keep it
responsible, while the Teensy required some breaks. Instead of using
microseconds to time it, I opted for using a timer to ensure it wasn't updated
too often.

Topics:
- Inspiration?
- Explain the name
- Fast prototyping
- Arduino Uno performance vs Teensy 4.1
  - Teensy fk ips: 1086956.50
  - Arduino uno 1355.60
- Objetivos
- Dumb IK approach
- Teensy and PCAs dying :(
