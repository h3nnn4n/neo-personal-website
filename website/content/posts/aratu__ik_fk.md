---
title: "Project Aratu: IK and FK"
date: 2023-07-08
tags: ["robotics", "project", "aratu", "inverse kinematics", "forward kinematics"]
draft: true
---

Articulated robots usually need to coordinate multiple actuators in order to
position an end effector at some desired position. For example a 7dof robotic
arm with an welder attachment needs to do move its actuators through a precise
sequence of moviments in order to weld along the desired path. Assuming that
all the actuators are rotary, `Forward Kinematics` (FK) can be though as taking
the angles that each actuator is set at, and knowing the physical model of the
arm, finding out where the end effector will be. Now, often we know where we
want the end effector to be at and we need to work backwards to figure out how
to position each actuator. This is known as `Inverse Kinematics` (IK).
Calculating FK is relativelly easy in most cases, meanwhile IK tends to be more
complex.

FK are commonly calculated analytically, ie, by a set of equations. In simple
cases, such as in [Aratu](TODO.com) it can be derived manually. Some general
solutions can be used to model FK, such as the [Denavit–Hartenberg
Parameters](https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters).
Regardless of the approach taken, FK is the easy part. Calculating IK tends to
be more complex. There will be constrains, potentially multiple solutions and
the more degrees of freedom there are, more variables to solve for. For simpler
robots with 2 or 3dofs it is possible to derive closed form solutions, but for
more complex models, it is often infeasible. This is where numerical and
heuristicals methods comes in. A popular numerical solution is to use the
Jacobian inverse. It is a relativelly math heavy solution, but very common. For
heuristics, likely the two more common ones are Cyclic Coordinate Descent (CCD)
and FABRIK (Forward And Backward Reaching Inverse Kinematics).
