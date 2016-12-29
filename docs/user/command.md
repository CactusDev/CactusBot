# `!command`
Minimum Role Required: **Moderator**

## `!command add [limiter]<command> <response...>`

Create a custom command.

If `<command>` is in the form of `main-sub`, it may be run later as either `!main-sub` or `!main sub`.

 - `limiter` represents the minimum role required to access the command.
    - `+`: Moderator-Only
    - `$`: Subscriber-Only

 `%VARIABLES%` can be used to create dynamic responses.
    
```
[Jello] !command add waffle Time to feed %ARGS% some waffles!
[CactusBot] Added command !waffle
[BreachBreachBreach] !waffle Innectic
[CactusBot] Time to feed Innectic some waffles!
```

## `!command remove <command>`

Remove a custom command.

```
[Epicness] !command remove waffle
[CactusBot] Removed command !waffle
[Innectic] Oh no, my waffles! /cry
```

## `!command list`
List all custom commands.

```
[Xyntak] !command list
[CactusBot] Commands: nowaffles, potato, kittens
```
