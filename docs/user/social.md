# `!social`

Store and retrieve social data.

## `!social [services...]`

Retrieve the URL for social services.

If any `services` are provided, the data for only those will be returned. Otherwise, all social URLs will be returned.

```
[cass3rz] !social
[CactusBot] Twitter: https://twitter.com/Innectic, Github: https://github.com/Innectic
```

```
[innectic] !social github
[CactusBot] Github: https://github.com/Innectic
```

## `!social add <service> <url>`

Minimum Role Required: **Moderator**

Store a social URL.

```
[eenofonn] !social add twitter https://twitter.com/eenofonn
[CactusBot] Added social service twitter.

[duke] !social twitter
[CactusBot] Twitter: https://twitter.com/eenofonn
```

## `!social remove <service>`

Minimum Role Required: **Moderator**

Remove a social URL.

```
[Daegda] !social remove twitch
[CactusBot] Removed social service twitch.
```
