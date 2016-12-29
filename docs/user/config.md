# `!config`
Minimum Role Required: **Moderator**
The config command has the ability to set every aspect about the bot.

## `!config announce <follow|subscribe|host> <response...|toggle>`
Edit the announcement messages for events.

- `response` - The response for the message
- `toggle` - Toggle the event announcement

```
[misterjoker] !config announce follow Thanks for following the channel, %USER%
[CactusBot] Updated announcement
```

```
{follow event}
[CactusBot] Thanks for following the channel, ParadigmShift3d!
```

```
[Jello] !config announce follow toggle
[CactusBot] Follow announcements are now disabled.
```

```
{follow event}
{no message from the bot}
```

## `!config spam <urls|emoji|caps> <value>`
Change settings about the spam filter

```
[DnatorGames] !config spam urls off
[CactusBot] URLs are now disallowed.
```

```
[QueenOfArt] !config emoji 20
[CactusBot] Maximum number of emoji is now 20.
```
