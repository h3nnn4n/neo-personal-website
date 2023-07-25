---
title: "Debugging and fixing a slow arduino serial connection"
date: 2023-05-07
tags: ["pottery", "internet of things", "automation", "arduino"]
draft: true
---

My Smart Kiln runs of a Raspberry pi (or something like that) and an arduino. The arduino
is in charge of reading data from all sensors, running the PID loop and switching the
SSR (Solid State Relay) that controls the heater element. It also has a serial interface
to communicate. It can be used to tune PID params and set the setpoint as well as read
data back. This is used to feed data into Grafana. The Pi communicates with the arduino
to retrieve the sensor readings for multiple temperatures, the pid params, setpoints,
state and anything else I might think worth logging. It also runs a separate control loop
that reads file with a firing schedule and communicates with the arduino to make it follow
the schedule.

The temperature inside the kiln has a lot of "inertia", ie it can't change very fast,
so we don't need a pid loop running at a super high frequency. A few hertz should be more
than enough. The first version, which only had the data logger,
ran at a neat 1hz without me doing anything in particular.
I remember going back and being like "I don't recall adding a 1 second delay in the loop"
but I didn't think much of it. When I added the firing schedule feature, running from a
second loop, I noticed that things slowed down to a bit over 2 seconds per iteration.
Later I added a third monitoring loop to make sure things weren't on fire and it got down
to 3 seconds per iteration. The pid loop was now running way slower than I expected, and it
clearly ran slower the more I used the serial port. While the over could operate fine at 
0.3 hertz, the nerd/engineer in me couldn't sleep at night knowing that it should be
running several times per second. I expected to have to make it slow down. Not to have
to debugg it to run faster.

First thing was to check the obvious: Hidden (or not so hidden) delays around the code.
There was none except for some bitbanging in the order 1 or 2 digit microseconds delays.
Next I confirmed that using the port less would cause the loop to run faster, and it did.
Serial was running at a whopping 9600 baud rate. The data logger would send a `READ_TEMPS`
command and receive back something like `"60000,1000.10,20.00,30.00,40.00"` (a counter and
readings from multiple sensors). That is 42 chars in total, including the return character.
Even at a 9600 baud, it should be able to run at 100s of hertz. This wasn't the issue, but
I bumped the baud to 115200 just to make sure and nothing changed. 
