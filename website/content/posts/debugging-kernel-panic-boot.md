---
title: "Debugging a Kernel Panic at Boot"
date: 2020-08-31
tags: ["debugging", "kernel panic", "linux"]
draft: false
---


Hey there. I have a small story to share, about how I got myself into a problem
for no good reason and how I got out of it. Currently, I am working on a
project which requires a somewhat peculiar setup. I am using a programming
framework for a project that only runs on windows. While wine on Linux kinda
works, it was a few issues and is too unreliable. As such, I am either
required to work directly on an actual Windows machine or to run a virtual
machine. I chose the latter.

As for now, my main workstation is a MacBook pro. While it can handle the
virtual box with some pain, it would make the system much slower, especially
while I am at work running a heavy-ish app. More so, the project in question
requires a reliable uptime. With that in mind, I decided to use my old 2013
desktop running Linux. It has an overclocked i5-3570k and 24Gb of ram which
has been running pretty much non stop since I bought it. Firstly I set up a
headless virtual machine using VirtualBox. Then auto start on boot was
configured. Thus, if somehow the machine shuts down/reboots, it would
automatically start the virtual machine again on boot. In the virtual
machine, I configured RealVNC on the windows client, and with it, I could
easily work on my project on windows from my comfortable MacBook pro.

So far so good. But this isn't a post about a cool setup. It is a post about a
kernel panic and hours of debugging. It all started with a system-wide update
that I decided to do. As usual, I thought to myself “Hmmm, do I really need to
update right now and risk downtime?”. The answer was an obvious “No”. The
system was relatively fresh (a few weeks, maybe months). Nevertheless, I went
ahead and decided to do it. After more than a decade using Linux, seldom I had
issues when doing a full system update. It is not unheard of. It still happens
once in a while, but what were the odds of it happening right now? I went ahead
and started the update. The list was relatively big. I saw a kernel update,
along with a lot of random packages and virtual box. After thinking “Hmm, this
could go wrong” I decided to run the update anyways. The packages were
downloaded, installed. The `initrd` was generated, `grub-mkconfig` was run.
Everything was ready. The machine was scheduled to reboot at 2 am. I continued
to work on my windows project for a couple of hours before going to sleep.

The next day I work up, did some errands, and ~went~ started to work. After
work, I tried to connect with the VNC to the virtual machine. The VNC server
was off. “Weird”, I thought. I tried to remotely log to my Linux machine but it
didn't work. I rebooted the machine and got the same response. The “I told you
so” thought crossed my mind. The desktop is pretty much just a pile of hard
drives and SDDs laying on top of my desk with a naked motherboard and the power
supply. It has no keyboard or monitor. I quickly fetched both and plugged them.
I got no image nor response from the keyboard. “This gonna be fun,” I thought.
The machine was rebooted, the motherboard manufacturer logo appeared, then
grub, then a black screen with the blinking cursor on the top right followed by
a kernel panic. The first thing that came to mind was a couple of swear words
in Portuguese followed by the image of an old man laughing (that would be my
mental image of Murphy).

The first thing I tried to do was use the fallback image that is automatically
generated with the previous version. I got a kernel panic again. After some
consideration, I think that on my last upgrade I did not reboot the machine. If
so, it is possible that the old state was already “unbootable”. But I am not
sure. I then tried botting another Linux that I had installed on a separate
disk. I got some grub error about a disk with some uuid not being found. “That
is what you get by not testing things until you need them”, I thought. After
this, I decided to try again the next day, which was going to be Saturday.

The next day, I went on to get things to work again. First I used a hardware
analysis tool that I had set up on grub and was still working. A quick look
around and I found that one of my hard drives has a negative size. “Bummer”, I
thought. The computer was turned off and I removed everything except and SSD
with the root. I rebooted and got an error saying that no bootable device was
found. Then I remembered that I was using grub from another disk, which had my
previous installation.

The next step was getting a bootable Linux pen drive to setup grub again. I
tried at least 5 times with my MacBook to get it working but I could not. No
idea why. I am relatively fresh in using Apple’s OS. As a fallback, I got a
10-year-old laptop, which had a somewhat prehistoric version of Linux, but at
least it was working. The pen drive was set up and I booted the desktop using
it. The first thing was to set up grub and generate a configuration file. The
computer was restarted and Kernel Panic again. “I guess the issue isn't the
hard drive”.

My next step was then to chroot into the broken Linux and run the update again.
“Maybe it was a borked package and it got fixed”. Only a couple of packages of
small importance got updated. I rebooted again and the kernel panic again.
Every time the kernel panic backtrace was different, so I could not easily
pinpoint what was causing it. The list of loaded modules had way too much stuff
loaded. A few Google queries after I found nothing useful. Then, I had the idea
to remove the quiet flag from grub. The config file was updated and the
computer rebooted. Lots of white lines appeared and kernel panic again, very
fast. I rebooted a couple of times but I could not see what was the last thing
before the kernel panic. I then recorded the screen using my phone. Watching
the video I saw that docker was the last thing before the kernel panic. I
chrooted and disabled the docker service that was being started on boot. Still
kernel panic.

Trying to pinpoint what was causing it wasn't going very well, so I decided to
take large steps in change trying to get the system to work again. When it
started working I could slowly add things back until the culprit was found. I
listed all the services enabled on boot. There were only half a dozen or so. I
disabled them all. Two were VPN related, there were VirtualBox and some other
unrecognized services. I rebooted and voila. I got a login screen. Finally, I
had some progress.

From there, my main suspect was VirtualBox. So I re-enabled everything except
for it. Rebooted and login screen again. Looks like VirtualBox was somehow the
troublemaker. No idea why. Well, VirtualBox was the reason I was so urgent to
get the machine working again.

My Linux distro of preference has a daily snapshot of the repository, which can
be referenced by the package manager. I pointed the repository to 1 week ago
and downgraded a whole lot of packages, rebuild the initramfs, updated grub,
enabled VirtualBox, and rebooted. Boom, kernel panic again. Then I pointed it 1
month ago and repeated the process. Now it worked.

From when then problem first started until I got it fixed, it was about 8 dead
hours of free time, including some of my weekend. And for what? Upgrading the
system for the sake of it? Not worth it. Leason learned. There is a saying that
I learned from my time in the army, it goes like this: “O trauma é o melhor
professor”. In English, it would be somewhat like “Trauma is the best teacher”.
Indeed. Lessons we learn the hard way are the ones we keep more easily. Lesson
learned. Hopefully, I tend to learn through more efficient and less frustrating
ways.

Well, here are some keypoints from all this:
1) Beware of Murphy's law
2) Dont upgrade for fun
3) Check if your fallbacks are working
4) Know your system and what it has to offer
5) When debugging try to get the system back to an working state asap

This is what I had to share. Stay safe.
