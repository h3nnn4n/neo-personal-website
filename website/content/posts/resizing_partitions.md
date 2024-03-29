---
title: "Moving disk space from home to root and resizing"
date: 2024-03-29
tags: ["btrfs", "linux"]
draft: true
---

- Take disk out of the pool, safely
- Close the luks device
- delete the partition
- Create swap partition at the end
- growpart
- resize2fs
- (nothing to do), turns out growpart failed
```
Warning! Secondary partition table overlaps the last partition by
1359 blocks!
Try reducing the partition table size by 5436 entries.
(Use the 's' item on the experts' menu.)
Aborting write of new partition table.
FAILED: disk=/dev/nvme2n1 partition=3: failed to repartition
***** WARNING: Resize failed, attempting to revert ******
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot or after you
run partprobe(8) or kpartx(8)
The operation has completed successfully.
***** Restore appears to have gone OK ****
```
