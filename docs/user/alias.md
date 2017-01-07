# `!alias`

Minimum Role Required: **Moderator**

Add and remove aliases for commands.

## `!alias add <alias> <command> [args...]`

Add alias `alias` for `command`, with arguments `args`.

```
[duke] !command add ip-hypixel mc.hypixel.net
[CactusBot] Added command !ip-hypixel.

[2Cubed] !alias add hypixel ip-hypixel
[CactusBot] Alias !hypixel for !ip-hypixel created.
```

```
[TransportLayer] !command add echo %ARGS%
[CactusBot] Added command !echo.

[ParadigmShift3d] !echo Hello, world!
[CactusBot] Hello, world!

[pingpong1109] !alias add cave echo Echoooo!
[CactusBot] Alias !cave for !echo created.

[ParadigmShift3d] !cave Is anyone theeeere?
[CactusBot] Echoooo! Is anyone theeeere?
```

## `!alias remove <alias>`

Remove alias `alias`.

```
[CallMeCyber] !alias remove cave
[CactusBot] Alias !cave removed.
```

## `!alias list`

List all aliases.

```
[pylang] !alias list
[CactusBot] Aliases: hypixel (ip-hypixel), meow (kitten).
```
