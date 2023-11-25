---
title: "Experimenting a modern filesystem (BTRFS)"
date: 2023-11-25
tags: ["btrfs", "linux"]
draft: true
---

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