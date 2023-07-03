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

TODO: pics of the old leg with a short tibia, and the long curved ones.

Topics:
- Inspiration?
- Explain the name
- Fast prototyping
- Arduino Uno performance vs Teensy 4.1
  - Teensy fk ips: 1086956.50
  - Arduino uno 1355.60
- Objetivos
- Dumb FK approach
- Teensy and PCAs dying :(
