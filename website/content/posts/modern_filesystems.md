---
title: "Experimenting a modern filesystem (btrfs)"
date: 2023-11-25
tags: ["btrfs", "linux"]
draft: true
---

Recently I bought myself a beefy new desktop computer as an upgrade from my 12
year old computer, which was still running strong but showing signs of its age.
over the 12 years that I had this computer, I accumulated 5 hdds and 4 ssds
(plus a few more that died). after going every single one of them and reviewing
all the data in it and copying what was worth keeping around, I was left with
12.5 terabytes spread across 9 devices. I knew I was going to use at least some
of the disks and the old computer as a data storage server. managing all the
disks was the issue. having 9 (or more) different mount points is not fun to
manage and very easy to lose data, considering that some hard drives were 8+
years old and had pretty much constant use. what I needed was a way to use
multiple devices as one, and in a raid1 setup if possible. encryption was also
something I set as a requirement.

On linux there are quite a few ways of doing this, for example using a
combination of `luks`, `lvm` and/or `mdadm` and putting a filesystem (such as
ext4) on top. having done this in the past, but with a single device, I really
didn't want to use this approach again since I found it to be a bit too clunky
to manage. another issue is the overall lack a assurance regarding how to
handle disk failures, since the setup would be custom-ish and assembled from
some basic building blocks.

The solution? using a "modern" filesystem! some of the options available are
`zfs` at 18 years old, `btrfs` at 15 years old, and `bcachefs` at 8 years old.
all three support encryption either directly or through `luks`, cow (copy on
write), which is very useful for doing snapshots at very low cost, and handling
multiple devices, and checksums for data and metadata. `zfs`, being the older
of the trio, is probably the most well tested and stable option, and often used
on servers (for example on [rsync.net](https://www.rsync.net/)). it isn't
available as part of the linux kernel due to legal/license constraints. and a
bigger issue for me, it doesn't handle pools made of heterogeneous devices
efficiently. a `zfs` raid1 of a 2x1 and 2x2 terabyte disks will have a total
storage 2 terabytes, since it normalizes down to the smallest device. in
contrast, `btrfs` and `bcachefs` both can use heterogeneous disks more
efficiently. `bcachefs` is more feature packed, notably tracking disk latencies
and optimizing reads from faster disks. it also supports using disks as cache
layers, where for example and nvme drive could be used to receive writes, a set
of hdds for storing data, and an ssd for caching reads. it is much newer and
only recently merged into kernel mainline.

The alternative left was `btrfs`, which seems to have a reputation for eating
away the data it stores. a bit of searching around reveals that these are
usually from several years ago and that the situation has changed. several blog
posts exist with people telling they stories of using `btrfs` without much
issue. one notable post which helped make up my mind was
[this](https://markmcb.com/linux/btrfs/five-years-of-btrfs/).

The setup I went for consisted of encrypting the full disks using `lusk`, which
can be done with `cryptsetup luksformat /dev/sda --label foo` for example. this
has to be ran for each device to be used. once encrypted, the device needs to
be opened (as a mapped device, where we can read and write transparently and
the data will be encrypted/decrypted transparently). this is done with
`cryptsetup open /dev/sda foo`. the next step is setting the `btrfs` system. it
starts with by running `mkfs.btrfs` on the mapped devices, eg `mkfs.btrfs
/dev/mapper/foo`. it is possible to pass all devices at a single time.
alternativelly, it is possible to add devices one by one to the pool. first it
needs to me mounted `mount /dev/mapper/foo /mnt/disk_pool/` for example, and
then we can add the devices using `btrfs device add /mnt/mapper/bar
/mnt/disk_pool`. By default, this will use the sum of all storage capacity,
also know as JBOD (Just a Bunch of Disks). While handy, it couples failures
between disks, where losing one may cause more data to be lost than if they
were simply being used individually. This happens because the file system might
store chunks and metadata across devices (haven't confirmed this to be honest).

To switch to a raid1 setup, which can tolerate the loss of a single drive, we
need to run `btrfs balance start --verbose -dconvert=raid1,soft -mconvert=raid1
/mnt/disk_pool`. The `dconvert` sets the profile for the data, while `mconvert`
sets the profile for the metadata. If metadata is lost, it is gameover. If the
pool consists of more than two disks, we can use `-deconvert=raid1c3` or even
`raid1c4` to replicate it to three or four disks. This can be done for data too
for a higher replication rate, but this might be overkill. One cool thing is
that if the motherboard supports hotswapping the disks, then in case of failure
it is possible to swap the disks without downtime or unmounting the brtfs pool.
The partition could even be activelly being used, although this will make the
rebalancing process slower and decrease the performance of the applications
using the btrfs partition. Whenever the profiles change, we can run.

## A small mishap

The initial setup had 3 disks. One HDD with 3 terabytes and two SSDs of 1
terabytes each. In total there were 5 terabytes of storage, but only 2
terabytes were usable. The first terabyte from the HDD was mirrored on one of
the SSDs, and the second terabyte would be mirrored to the second SDD. The
third terabyte doesn't have a match to mirror against, so it isnt utilized.

After a few days of use and storing a bunch of data on it, the pool got full.
Based on my grafana logs, one of the SSDs got filled, and then the second one.
At this point the system switched to readonly. I bought a new 4 terabyte SSD,
plugged it in, and ran `btrfs device add` to add it to the pool. To my surprise
it failed because it had no space left. I tried a couple of times mounting and
unmounting the disk, and any command I ran put the filesystem in readonly mode.
After some annoyance I decided to delete some of the data, and after it I got
the new device properly added in. Rebalancing took several hours, but it worked
well. Going forwards, it is definitelly worth adding or replace disks before it
gets full.

## A Bigger mishap

After many years without a windows install, I decided to install it for the
tooling available for tuning cpu and ram. The process was quite annoying and
took me several hours (mostly due to my own inconpetence / ignorance).
Naturally, this broke my linux boot. After fixing it, I noticed that the btrfs
filesystem failed to mount. Logs showed that it was due to a missing disk (or
in this case, the device mapper being missing). Running `fdisk -l` quickly
revealed the problem: There was an EFI partition at the disk, which overwrote
the `LUKS` header and basically nuked the data in that disk. Well, this is what
the raid1 setup was for hehe. `btrfs` has a command specifically for replacing
a failed disk, but it is intended when you are adding a new device to replace a
physical one. In my case, it was the same device, but it was wiped clean.
Instead of using the `replace` command, I ran `btrfs device delete missing`. I
expected this to run immediately, or at least very quickly. To my surprise, it
took a few minutes, then a few hours, and then it kept running. By running
`watch -d btrfs filesystem usage /mnt/disk_pool` I could see that it was
aparently going over all the data allocated in the disk, which was the 3
terabyte one. Not sure what it is doing, but I would imagine that it is
verifying that all the data is present or something similar.

After 14 hours and only having processed 1 terabyte out of 3, I decided that
would be a good idea to stop the process and just add the disk to the pool and
see what would happen. What happened is that `btrfs` still had 1.3 terabyte
marked as missing, and the disk was showing up as 3 terabytes of unallocated
space. Running a balance with `soft` updated zero chunks. Then I remembered
that the filesystem had to be mounted in degraded mode. Perhaps this is
preventing the balance from running? Well, back to running `btrfs device delete
missing` again.

delete took 14 hours and only went over 1.4tb out of 2.7

TODO: When it finishes running, complete the writting here.

Topics:
- explain new pc with a bunch of old disks
    - Wanted to use them as a single disk
    - lvm could do it, but couldnt tolerate disk failures
    - Investigated zfs, btrfs and bcachefs
- How setup worked
    - How to make it
- Main pc and backup computer
- Pool getting full and adding a new disk
- Installing windows and losing one disk
    - Me or windows nuked one of the disks with an efi partition
    - Recovery process
        - `btrfs balance start -v -mconvert=raid1c3,soft /mnt/disk_pool`
        - `btrfs device delete missing /mnt/disk_pool`
