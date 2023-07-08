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

Let's start working on our IK solver. A simple approach would be to go over all
joints, move them in both directions by a step and see which direction improves
it. We will need to iterate over all joints in two directions. We can simplify this
by having a list of vectors that we apply to the vector `(a, b, c)`, like this:

```c++
const vec3_t offsets[] = {
    vec3_t(1.0f, 0.0f, 0.0f), vec3_t(-1.0f, 0.0f, 0.0f),  // Coxa
    vec3_t(0.0f, 1.0f, 0.0f), vec3_t(0.0f, -1.0f, 0.0f),  // Femur
    vec3_t(0.0f, 0.0f, 1.0f), vec3_t(0.0f, 0.0f, -1.0f),  // Tibia
};
```

For `(a, b, c)`, assuming `a`, `b` and `c` maps to the `coxa`, `femur` and
`tibia` angles respectively, then the 6 vectors defined are the 6 different
perturbations we can do to our angle vector. If our angle space is in degrees,
then the unit vectors might be a reasonable step size. Applying the step size
once is unlikely to get us very far though, so let's iterate multiple times
for each offset.

```c++
vec3_t Leg::inverse_kinematics(vec3_t target_position) {
    const uint16_t n_iters   = 25;
    const uint8_t  n_offsets = 6;

    const vec3_t offsets[] = {
        vec3_t(1.0f, 0.0f, 0.0f), vec3_t(-1.0f, 0.0f, 0.0f),  // Coxa
        vec3_t(0.0f, 1.0f, 0.0f), vec3_t(0.0f, -1.0f, 0.0f),  // Femur
        vec3_t(0.0f, 0.0f, 1.0f), vec3_t(0.0f, 0.0f, -1.0f),  // Tibia
    };

    vec3_t angles      = {0.0f, 0.0f, 0.0f};
    vec3_t best_angles = {0.0f, 0.0f, 0.0f};
    float best_error   = feet_position_error(forward_kinematics(_current_position), target_position);
    float error        = best_error;

    for (uint16_t i = 0; i < n_iters; i++) {
        for (uint16_t i_offset = 0; i_offset < n_offsets; i_offset++) {
            angles = best_angles + offsets[i_offset];

            vec3_t position = forward_kinematics(angles.x, angles.y, angles.z);
            error           = feet_position_error(position, target_position);

            if (error < best_error) {
                best_error  = error;
                best_angles = angles;
            }
        }
    }

    return best_angles;
}
```

This simple IK routine could already get us pretty far, but it has some issues
that would limit its usefulness in an actual robot. This current setup, for an
arbitrary target position of `0, 100, -115` (which is something that would make
the robot standup if applied to all legs) gives us an error of `135.37`, taking
`0.000168` seconds to calculate (`5952` updates per second).

1. Our offset is `1` and we iterate `25` times, so it can only find a solution
   if it is at most 25 degrees away from the starting point. Pretty bad. In
   most cases it won't find a feasible solution.
2. In the rare case where it finds the solution, it would keep going, wasting
   precious cycles.
3. The solution is limited to `1` degree increments, which might be too much.
4. It converges slowly. If it is `x` units away, with an step of `1` it will
   take `x` iterations to converge. With 3 angles to optimize, this can be even
   longer.
5. The solution starts from scratch every time and doesn't account for the
   current position. In some cases there might be multiple solutions and we
   want the one requiring the least amount of movement to reach.
6. Might get stuck on a local minima.
7. Doesn't account for physical constraints.

Quite a lot of issues! But all of them can be fixed, worked around or even
completely avoided. Item 1 can be fixed by adding 360 iterations instead of 25,
which makes sense. This would increase the solve time though by a linear factor
though. For Item 2 we can add a short circuit and finish early if a solution
good enough is found. For Item 3 and 4 we can add a scale factor to take
smaller / bigger steps. This could also be used to address item 1 without
making it significantly slower. Let's start implementing these improvements.

If we try to increase the number of iterations to `360`, we get a final error
of around `3.12`, much better. But it now takes `0.002660` seconds per update
(`375` updates per second). Not terrible, but we can do better. Let's apply the
tweaks above and see what happens.

Let's add an early termination if we get close enough to our target. Let's set
a big tolerance to test, such as `10`. This can be accomplished by exiting the
inner loop if the `best_error` is less than the target error.

Now we take `0.000917` seconds per udate (`1090` ups) and we get down to an
error of `9.825376`. A big improvement in terms of speed, but we have a worse
position. For this to be useful, we need to 1) be able to converge to a better
solution, and 2) get there faster.
