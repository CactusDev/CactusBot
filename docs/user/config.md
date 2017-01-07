# `!config`

Minimum Role Required: **Moderator**

Set a configuration option.

## `!config announce <follow|subscribe|host>`

Edit the announcement messages for events.

### `!config announce <follow|subscribe|host> <response...>`

Update the response for an event announcement. The `%USER%` variable may be used for username substitution.

```
[misterjoker] !config announce follow Thanks for following the channel, %USER%!
[CactusBot] Updated announcement.

*ParadigmShift3d follows*
[CactusBot] Thanks for following the channel, ParadigmShift3d!
```

### `!config announce <follow|subscribe|host> toggle [on|off]`

Toggle a specific type of event announcement. Either `on` or `off` may be used to set the exact state.

```
[Jello] !config announce follow toggle
[CactusBot] Follow announcements are now disabled.

*Innectic follows*
*CactusBot does not respond*
```

## `!config spam <urls|emoji|caps> <value>`

Change the configuration value for a spam filter.

- `urls` accepts either `on` or `off`, which allows or disallows URLs, respectively.
- `emoji` accepts a number, which is the maximum amount of emoji which one message may contain.
- `caps` accepts a number, which is the maximum "score" which a message may have before being considered spam.

  - The "score" is calculated by subtracting the total number of lowercase letters from the total number of uppercase letters.

```
[DnatorGames] !config spam urls off
[CactusBot] URLs are now disallowed.

[QuirkySquid] Whoa, check out google.com!
*CactusBot times out QuirkySquid*
```

```
[QueenofArt] !config emoji 5
[CactusBot] Maximum number of emoji is now 5.

[pingpong1109] Wow! :O :O :O :D :D :D
*CactusBot times out pingpong1109*
```
