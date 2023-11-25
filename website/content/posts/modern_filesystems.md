---
title: "experimenting a modern filesystem (btrfs)"
date: 2023-11-25
tags: ["btrfs", "linux"]
draft: true
---

recently i bought myself a beefy new desktop computer as an upgrade from my 12
year old computer, which was still running strong but showing signs of its age.
over the 12 years that i had this computer, i accumulated 5 hdds and 4 ssds
(plus a few more that died). after going every single one of them and reviewing
all the data in it and copying what was worth keeping around, i was left with
12.5 terabytes spread across 9 devices. i knew i was going to use at least some
of the disks and the old computer as a data storage server. managing all the
disks was the issue. having 9 (or more) different mount points is not fun to
manage and very easy to lose data, considering that some hard drives were 8+
years old and had pretty much constant use. what i needed was a way to use
multiple devices as one, and in a raid1 setup if possible. encryption was also
something i set as a requirement.

on linux there are quite a few ways of doing this, for example using a
combination of `luks`, `lvm` and/or `mdadm` and putting a filesystem (such as
ext4) on top. having done this in the past, but with a single device, i really
didn't want to use this approach again since i found it to be a bit too clunky
to manage. another issue is the overall lack a assurance regarding how to
handle disk failures, since the setup would be custom-ish and assembled from
some basic building blocks.

the solution? using a "modern" filesystem! some of the options available are
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

the alternative left was `btrfs`, which seems to have a reputation for eating
away the data it stores. a bit of searching around reveals that these are
usually from several years ago and that the situation has changed. several blog
posts exist with people telling they stories of using `btrfs` without much
issue. one notable post which helped make up my mind was
[this](https://markmcb.com/linux/btrfs/five-years-of-btrfs/).

the setup i went for consisted of encrypting the full disks using `lusk`, which
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

Topics:
- explain new pc with a bunch of old disks
    - Wanted to use them as a single disk
    - lvm could do it, but couldnt tolerate disk failures
    - Investigated zfs, btrfs and bcachefs
- How setup worked
    - How to make it
- Main pc and backup computer
- Installing windows and losing one disk
    - Me or windows nuked one of the disks with an efi partition
    - Recovery process
        - `btrfs balance start -v -mconvert=raid1c3,soft /mnt/disk_pool`
        - `btrfs device delete missing /mnt/disk_pool`
