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

For Aratu, I am going with a Heuristic approach for IK. It has 6 identical
legs, each with 3dof. If we think of FK as a function that takes 3 angles and
returns an `x, y, z` coordinate, we can define IK as an optimization problem
where we want to optimize `a, b, c` (our angles) to minimize `||(x, y, z) -
(x_t, y_t, z_t)||`. Here `x_t, y_y, z_t` is our target position, ie where we
want to go. How we minimize this is up to us. Basically, our IK routine with be
finding the values for the tuple `(a, b, c)` where when it is fed into FK the
result is as close as possible to where we want to be.

First, lets define our FK function:
```c++
vec3_t Leg::forward_kinematics(float coxa_angle, float femur_angle, float tibia_angle) {
    vec3_t feet_position;

    const float leg_length_top_view = (
      COXA_LENGTH +
      cos(femur_angle) * FEMUR_LENGTH
      + cos(tibia_angle - femur_angle) * TIBIA_LENGTH
    );

    feet_position.x = sin(coxa_angle) * leg_length_top_view;
    feet_position.y = cos(coxa_angle) * leg_length_top_view;
    feet_position.z = sin(femur_angle) * FEMUR_LENGTH - sin(tibia_angle - femur_angle) * TIBIA_LENGTH;

    return feet_position;
}
```

The constants `COXA_LENGTH`, `FEMUR_LENGTH` and `TIBIA_LENGTH` are the bone sizes of our leg.
In my case it is defined as:
```c
#define COXA_LENGTH  52
#define FEMUR_LENGTH 78.984
#define TIBIA_LENGTH 163.148
```
