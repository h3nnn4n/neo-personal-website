---
title: "Rubiks Cube Solver"
date: 2021-02-27
tags: ["rubiks cube", "solver", "c"]
draft: true
---

The Rubik's cube, invented in 1974 by Ernő Rubik, is the most sold puzzle of
all time. Me, being born on 1994, am 20 years younger than the puzzle. And as
most children of my age, I got my first cube and had no clue how to solve it.
For many years, the only way was to disassemble it and put it back together.
That changed when I started studying computer science in 2012. There I met a
guy that know how to solve it. Not only that, but he could solve it in under 2
minutes and that blew my mind. Fast forward 2 months and I became a Rubik's cube
addict. I would watch youtube videos on how to solve the cube and watch
competitions only, train for several hours a day and make small competitions on
my university.

Being someone that learned to code at an younger, and that loved coding all sorts
of things, soon I had the idea of coding a Rubik's solver. The idea was very simple:
Make a 3x3x3 matrix and populate it with letters indicating the colors, then write a
function that effects the cube by twisting one of the sides and take a parameter to
specify which one. Being a big lover of recursion, I made a recursive function to
enumerate all possible moves of length between one and twenty voilà, the first solution
to be found would be the shortest one.
