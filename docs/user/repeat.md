# `!repeat`
Minimum Role Required: **Moderator**

Repeat a command every so often

## `!repeat add <interval> <command> [args]`
Create a repeating command

 - `interval` is the amount of time between messages, in seconds. Minimum is `60`
 - `command` is the command to be repeated on the interval
 - `args` is the optional arguments to call the command with

```
[misterjoker] - !repeat add 120 waffle ParadigmShift3d
[CactusBot] Repeating command !waffle every 120 seconds.
[ParadigmShift3d] Yay! Time to eat all the waffles. :D
```

## `!repeat remove <command>`
Remove a repeating command

```
[AlphaBravoKilo] !repeat remove waffle
[CactusBot] Repeat for command !waffle has been removed.
```

## `!repeat list`
List all repeating commands in a channel.

```
[impulseSV] !repeat list
[CactusBot] Active repeats: waffle, kittens.
