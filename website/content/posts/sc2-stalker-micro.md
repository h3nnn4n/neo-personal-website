---
title: "Starcraft 2 Stalker Micro"
date: 2018-08-19
tags: ["starcraft 2", "artificial intelligence", "micro"]
draft: false
---


Starcraft 2 is currently the most competitive 1 vs 1 game, and from a
Artificial Intelligence point of view it is a good (and hard) problem to
tackle. It is very complex, having very delayed rewards, high dimensionality,
volatility (baneling hit = rip), partial information and other things. Recently
Blizzard shared an [interface](https://github.com/Blizzard/s2client-proto) that
makes possible for agents to play the game.


[DeepMind](https://deepmind.com/blog/deepmind-and-blizzard-open-starcraft-ii-ai-research-environment/)
is probably the leading research force on Starcraft 2 right now on a professional level.
On the community side, there is [Sc2ai](https://sc2ai.net/), which is a
community driven ladder board for bots. It supports several API's, including
DeepMinds's [pysc2](https://github.com/deepmind/pysc2) and Dentosal's
[python-sc2](https://github.com/Dentosal/python-sc2). The ladder features more
than 20 bots and has a very active community.


Two of the bots on Sc2ai are mine:
[Spatial Llama](https://github.com/h3nnn4n/h3nnn4n-sc2-ai/tree/master/SpatialLlama/SpatialLlama)
and [Tapioca Bot](https://github.com/h3nnn4n/h3nnn4n-sc2-ai/tree/master/TapiocaBot/TapiocaBot).
The former is a proof of concept, where I wanted to learn the basic of
Dentosal's API and get a grip of doing a scripted bot for Starcraft 2. The
latter is my under development bot, where I am focusing the most. It is
~~somewhat~~ modular (I am still working on that). Several modules are
available: Research Controllers, Building Controllers, Build Order Controllers,
an Army Controller and more. The use of modules allows for the bot to be more
flexible, where one main module (the coordinator) can change the parameters of
the other modules to change the bot behavior.


Recently I developed a Three Gate Blink Stalker All In, based of
[herO's](https://lotv.spawningtool.com/build/62763/). The build order is very
simple and it relies heavily on micro. Previous versions of Tapioca Bot were
macro focused (and they sucked). This current iteration applies pressure as soon
as possible and relies on unit control to keep the pressure going.


The first feature of the
[Stalker](https://liquipedia.net/starcraft2/Stalker_(Legacy_of_the_Void))
control is unit grouping, where a small squad is formed and they start the
attack together. This helps to prevent one single unit from getting overwhelmed
by zerglings for example. The group is not permanent, it stays usually until a
fight starts. One of the things on my TODO list is to make the groups more
permanent and make them work together with focus firing for example. The
following video shows this (the grouping) in action.


<video autoplay loop muted src="/videos/wait_for_allies.webm"></video>


The unit control while in combat is based on a simple set of conditions. The
unit tries to stay far away as possible from the enemy units while staying in
shooting range. If the stalker is faster than the enemy unit, it will stay in a
safe distance from the enemy while being able to attack it. In the case where
the stalker is not faster, but can out range the enemy unit, it will walk back
without stop while allied units shoot the enemy unit. When blink is available,
the unit will be able to blink away from the fight after losing its shields,
which allows for the damage to be distributed among all units and keeping the
number of allied units high.


<video autoplay loop muted src="/videos/kite.webm"></video>


The position where the unit will walk back, if needed, is directly behind it,
when facing the closest enemy unit. While this is very simple and has some
drawbacks, such as getting stuck on allied units, it has one big advantage: The
units will tend to make an arc around the enemy units. The group in a convex
shape fighting the units in a concave one will have a big disadvantage,
because more units can shoot the same unit at the same time. The attack surface
is maximized. This can be seem happening in the following videos.


<video autoplay loop muted src="/videos/arc1.webm"></video>


As it can be seem, the closer that an enemy unit tries to get to the stalkers,
the higher surface of attack it will have. Furthermore, since the units tend to
form an arc (or even a circle), they become less susceptible to Area of Effect
spells and attacks. The shape also makes hard for one unit to be focused down,
thus increasing the overall survivability of the unit and the army.


<video autoplay loop muted src="/videos/arc2.webm"></video>


The Three Gate Blink All In bot, before having micro added, had a very small
win rate versus the default game AI on the Elite difficulty. After adding the
micro functionality to the stalkers, the win rate went from less than 10% to
about 60% over 250 games. Most of the wins are versus zerg opponents, since
their early ranges units (roaches) are slow and have a shorter range than
stalkers (4 versus 6), making them an easy target. They also take bonus damage
from stalkers, due to their armored tag. Zerglings can be fast than an stalker
with upgrades, but they are very fragile and will not do too much damage.
Versus Protoss, the win rate gets lowers, since micro can not do too much in a
stalker versus stalker battle. However, they do help versus adepts, zealots and
sentries. Finally, versus Terran the win rate is the smallest one. Marine and
marauders with Stimpack can gun down stalkers very fast. Also, siege tanks will
outrange the stalkers, and when siege, will quickly destroy the stalkers.
