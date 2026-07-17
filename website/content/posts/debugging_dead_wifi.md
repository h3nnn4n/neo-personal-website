---
title: "Debugging a Kernel Panic at Boot"
date: 2024-03-02
tags: ["debugging", "network", "linux"]
draft: true
---

TODO:
- Kiln setup
- Got worse as we tracked more things
- sensors grew from 1 to 4
- fails faster when away from router (ie in the garage)
- Dumb implementation with one thread and connection per metric point
- Fix was to batch writes and remove data races
    - batch size getting delayed and tracking batch size before it could stop the batch
