---
title: "Moving my home to btrfs"
date: 2024-02-15
tags: ["btrfs", "linux"]
draft: false
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

Now that we are using our fancy new `btrfs` filesystem, we can remove the old
home and add it to the pool. Only do this after making sure that everything
works with the new set. Also, make sure your backups work too, just in case ;)

The steps are similar up to a point. First, we create the encrypted partition:
`cryptsetup luksFormat /dev/nvme1n1p4 --label ripley`. I named mine, Ripley, after
the character from Alien. Then we unlock it using
`cryptsetup open /dev/disk/by-id/nvme-PCH-ALDPRO-1TB_ALDPRO1TB-05230441_1-part4 ripley`.

Now, instead of using `mkfs`, we call `btrfs` directly to add the device to the
pool. We do this with `btrfs device add /dev/mapper/ripley /home`. With this,
we will have two devices in our pool, but the new one will be mostly unused. We
can do a balance to fix this, and also to customize some settings. The
following command balances the data, sets the data to be stored in a single
place, and metadata to be replicated across devices:
`btrfs balance start -dconvert=single -mconvert=raid1 /home`. While losing data
is bad, losing btrfs metadata is equaly as bad, so we set metadata to raid1.

Since we are using the whole 4tb disk, and a partition from another disk which
is "only" 750gb, we can't do a raid1 setup for data. Well, actually nothing
stops us, but we would only be able to use 750gb, since that is the amount that
overlaps between the two devices. The rest would go ununsed.

A cool thing about this setup, in my opinion, is being able to mix whole
devices (without even a partition table) and partitions in the pool. We could
even go crazy and had a pendrive, a network mounted device, and whatever else
you can imagine as part of the pool. It wouldn't necessarely be a good idea,
but nothing is stoping us :)

Finally we need to set the new member of our pool to be unlocked at boot. Just
copy the `rambo` pam file and replace it with the device for ripley. No need to
update the mount command. Mounting one device from the pool, automatically
mounts everything. And a final note: Don't forget to add the `ripley` script
to the pam config file like I did.

## Note on performance

FWIW, I had around 700gb of data, and the balance operation took around 20
minutes. One thing I noticed, is that the disk throughput and i/o queue were
never saturated during this operation. The CPU usage was relatively low as
well, at around 10% on a 32 core machine. The CPU governor didn't even set a
single core to the highest clock (something that youtube will). The data volume
would barely saturate a one lane pcie 2.0 link. I assume this is a software
limitation when running the balance operation. Read and write operations easily
achieve rates between 2 and 7 GB/s.

## Conclusion ?

Compared to the simplicity of using `ext4`, `btrfs` can be a lot of extra work
to accomplish something that at the end of the day is mostly the same: storing
data. I would say that for the average user the time tradeoff for the `btrfs`
features is likely not worth. However, for the poweruser, the curious, and
alike, it can be a very useful tool. Compression, checksums, raid / jbod /
spam, copy-on-write, volumes and snapshots can give lots of flexibility if used
correctly.

I haven't been running the `btrfs` setup on my home for long (only a few days).
If anything fun happens, I will write a new post about for sure ;)
