# `!quote`

## `!quote [id]`

Minimum Role Required: **User**

Retrieve a quote. If a numeric `id` is supplied, return the quote with the specific identifier. Otherwise, choose a random quote.

```
[cass3rz] !quote
[CactusBot] "Someone stole my waffles!" -Innectic
```

```
[TransportLayer] !quote 12
[CactusBot] "Potato!" -2Cubed
```

## `!quote add <quote...>`

Minimum Role Required: **Moderator**

Add a quote.

```
[Daegda] !quote add "Python 3.6 is out!" -pylang
[CactusBot] Added quote #37.
```

## `!quote edit <id> <quote...>`

Minimum Role Required: **Moderator**

Edit the contents of a quote.

```
[alfw] !quote edit 12 "Potato salad!" -2Cubed
[CactusBot] Edited quote #12.
```

## `!quote remove <id>`

Minimum Role Required: **Moderator**

Remove a quote.

```
[QueenOfArt] !quote remove 4
[CactusBot] Removed quote #4.
```
