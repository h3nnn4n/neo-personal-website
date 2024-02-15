---
title: "Moving my home to btrfs"
date: 2024-02-15
tags: ["btrfs", "linux"]
draft: true
---

Recently I tried using btrfs, as explained in this
[post](/posts/modern_filesystems/). Having read about it eating data, at first
I was a bit skeptical of using it, despite the benefits, but so far the
experience has been quite good. I had a few mishaps, but those were good
learning experiences. From there, I decided to move my home to btrfs as well.

## The migration

My home, along the root folder of my linux distro of choice, is located at a
1tb nvme drive, which tbh is quite small for modern standards. A couple of
games like doom, multiple datasets and models, and a few local databases for
development can easily eat all the disk space (which has happened quite a few
times). This was the "kick" I needed to fix the situation, which I started
by buying a 4tb nvme drive.

Next, I set full disk encryption using LUKS: `cryptsetup luksFormat
/dev/nvme2n1 --label rambo`. Then unlocked the device using
`cryptsetup open /dev/nvme2n1 rambo`. Created the `btrfs` filesystem
using `mkfs.btrfs /dev/mapper/rambo` and mounted it with
`mount /dev/mapper/rambo /mnt/new_home/`. Now, it is a simple as copying the
data over, correctly. Rsync can do the job with
`rsync --archive --hard-links --acls --xattrs --sparse --progress /home/ /mnt/new_home/`.

With the home folder duplicated into the new `btrfs`, we are just missing
making it the new home. First, we remove the old home from `fstab`. Since the
new home is encrypted, we need to decrypt is before being able to mount it. By
using the same key as the login, we can use `pam` for unlocking and mounting it
on login. I accomplished this by creating `/etc/pam_cryptsetup_rambo.sh` with:
```
#!/bin/sh

CRYPT_USER="h3nnn4n"

if [ "$PAM_USER" = "$CRYPT_USER" ]; then
    echo "Decrypting rambo"
    /usr/bin/cryptsetup open /dev/disk/by-id/nvme-Corsair_MP600_PRO_LPX_A5KOB342003WYB rambo || true
fi
```

It checks that the correct user is logging in, then unlocks the device using
the disk id. My motherboard likes to switch things around for no particular
reason (that I know of). Using `/dev/nvmeXnY` results in the dwarf fortress
kind of fun. Another import detail is the `|| true` part. If opening one of the
devices from the pool fails, we still want to log in to be able to debug. On a
`raid1` setup, the files will still be there (assuming one disk failure ofc).

Next, we need to automatically mount the unlocked device. For this we create a second script,
this time at `/etc/pam_cryptsetup_mount.sh`:
```
#!/bin/sh

CRYPT_USER="h3nnn4n"

if [ "$PAM_USER" = "$CRYPT_USER" ]; then
    mountpoint -q /home
    if [[ $? -ne 0 ]]; then
        echo Mounting encrypted home
        mount -o compress-force=zstd:9,barrier,space_cache=v2 /dev/mapper/rambo /home
    fi
fi
```

It does the same username check, then it checks if it isn't already mounted. If
it isn't, then it gets mounted using the desired options. Both scripts need to
be executable. Then, the final step is to tell `pam` to run the scripts on login.
Add to `/etc/pam.d/system-login` the following lines:
```
auth       optional   pam_exec.so expose_authtok debug stdout /etc/pam_cryptsetup_rambo.sh
auth       optional   pam_exec.so expose_authtok debug stdout /etc/pam_cryptsetup_mount.sh
```

The `expose_authtok` option sends the password to the script, which is used to
unlock and mount. `debug` and `stdout` makes the `echo` commands show up during
login. Otherwise it looks like it is stuck while the devices unlock and mount.

Now we reboot and validate that it works :)

## Adding the old home partition to the btrfs mount

TODO: Do this first lol
