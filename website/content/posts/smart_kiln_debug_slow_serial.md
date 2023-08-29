---
title: "Debugging and fixing a slow arduino serial connection"
date: 2023-05-07
tags: ["pottery", "internet of things", "automation", "arduino"]
draft: false
---

My Smart Kiln runs of a Raspberry pi (or something like that) and an arduino.
The arduino is in charge of reading data from all sensors, running the PID loop
and switching the SSR (Solid State Relay) that controls the heater element. It
also has a serial interface to communicate. It can be used to tune PID params
and set the setpoint as well as read data back. This is used to feed data into
Grafana. The Pi communicates with the arduino to retrieve the sensor readings
for multiple temperatures, the pid params, setpoints, state and anything else I
might think worth logging. It also runs a separate control loop that reads
file with a firing schedule and communicates with the arduino to make it
follow the schedule.

The temperature inside the kiln has a lot of "inertia", ie it can't change very
fast, so we don't need a pid loop running at a super high frequency. A few
hertz should be more than enough. The first version, which only had the data
logger, ran at a neat 1hz without me doing anything in particular. I remember
going back and being like "I don't recall adding a 1 second delay in the loop"
but I didn't think much of it. When I added the firing schedule feature,
running from a second loop, I noticed that things slowed down to a bit over 2
seconds per iteration. Later I added a third monitoring loop to make sure
things weren't on fire and it got down to 3 seconds per iteration. The pid loop
was now running way slower than I expected, and it clearly ran slower the more
I used the serial port. While the oven can operate fine at 0.3 hertz, the
nerd/engineer in me couldn't sleep at night knowing that it should be running
several times per second. I expected to have to make it slow down. Not to have
to debug it to run faster. The main issue with the inconsistent and slow loop
times, is that the PID output changes depending on how long the last
interaction took. In the image below, the green line is the raw output and the
yellow one is a moving average. We can see 3 clear bands in the output, caused
by the 1, 2 and 3 second delays between iterations.

<div class="container-fluid">
  <div class="row">
    <div class="col">
      <img
        class="img-fluid" src="{% static 'images/smart_kiln/pid_output.png' %}"
        alt="Graph showing the PID output. The magnitude changes depending on
        how long the loop took to run."
      ></img>
    </div>
  </div>
</div>
<br>

First thing was to check the obvious: Hidden (or not so hidden) delays around
the code. There was none except for some bitbanging in the order 1 or 2 digit
microseconds delays. Next I confirmed that using the port less would cause the
loop to run faster, and it did. Serial was running at a whopping 9600 baud
rate. The data logger would send a `READ_TEMPS` command and receive back
something like `"60000,1000.10,20.00,30.00,40.00"` (a counter and readings from
multiple sensors). That is 42 chars in total, including the return character.
Even at a 9600 baud, it should be able to run at 100s of hertz. This wasn't the
issue, but I bumped the baud to 115200 just to make sure and nothing changed.

While working on [Aratu](/tags/aratu/), my hexapode robot, I faced the same
problem. There I needed a much faster iteration, at least 100 hertz. The setup
between the two was completely different. Aratu used a raspberry pi 3 and a
Teensy 4.1 while the smart kiln uses an orange pi and an arduino mega. The only
common thing between the two is the arduino core library, which handles serial.
Looking at the documentation for
[Serial.readString](https://www.arduino.cc/reference/en/language/functions/communication/serial/readstring/)
we have `The function terminates if it times out`. Aha! It seems to have a
timeout for when there is nothing to read. The default timeout is 1 second,
which explains the neat 1 second increments in the iteration times. Using
[Serial.setTimeout](https://www.arduino.cc/reference/en/language/functions/communication/serial/settimeout/)
to set the timeout to 10 ms swiftly solved the issue.

The code starts by first reading data from the serial port, parsing it and
returning the outputs requested. If there isn't data to read, it just waits
until it times out. We know that the messages to be read are quite small, and
failing to parse it every now and then won't have any catastrophic effects, so
it should be fine having a 10 ms timeout.

With this change, the smart kiln pid loop no longer has to wait every iteration
for the serial to timeout and the data syncer script had to be tweaked to not
run as fast as possible. It syncs the full state once per second. As for the
PID loop, it now runs at a fixed 10 hertz, which for the given application is
more than enough.

Well, this is it for now. Stay safe.
