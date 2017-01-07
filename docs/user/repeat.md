# `!repeat`

Minimum Role Required: **Moderator**

Send the contents of a command at a set interval.

## `!repeat add <interval> <command>`

Add a repeat for a specific command.

- `interval` is the amount of time between messages, in seconds. The minimum is `60`.
- `command` is the command response to send at the interval.

```
[misterjoker] !repeat add 1200 waffle
[CactusBot] Repeat !waffle added on interval 1200.
[ParadigmShift3d] Yay! Time to eat all the waffles. :D
```

## `!repeat remove <command>`

Remove a repeat.

```
[AlphaBravoKilo] !repeat remove waffle
[CactusBot] Repeat for command !waffle has been removed.
[Innectic] Aww... no more waffles.
```

## `!repeat list`

List all repeats.

```
[impulseSV] !repeat list
[CactusBot] Active repeats: waffle, kittens.
```
