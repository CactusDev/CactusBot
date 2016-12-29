`Variables` enable dynamic responses based on the message

## `%NAME%`
The `%NAME%` variable is replaced with the name of the user who ran the command

```
[2Cubed] !command add kittens %NAME% likes kittens!
[CactusBot] Command !kittens added!
[ParadigmShift3d] !kittens
[CactusBot] ParadigmShift3d likes kittens!
```

## `%ARGN%`
The `%ARGN%` variable is replaced with the `N`th argument passed with the command, where `N` is an integer.

```
[ParadigmShift3d] !command add throw %ARG2% you %ARG1%!
[CactusBot] Command !throw added.
[Alkali_Metal] !throw potato Innectic,
[CactusBot] Innectic, you potato!
```

## `%ARGS%`
The `%ARGS%` variable is replaced with all the arguments passed.

```
[Innectic] !command add hug %NAME% hugs %ARGS%!
[CactusBot] Command !hug added.
[BreachBreachBreach] !hug the whole chat
[CactusBot] BreachBreachBreach hugs the whole chat!
```

## `%COUNT%`
The `%COUNT%` variable is replaced with the amount of times the command has been run

```
[misterjoker] !command add derp Joker has derped %COUNT% times!
[CactusBot] Command !derp added
[ripbandit] !derp
[CactusBot] Joker has derped 2056 times!
```

## `%CHANNEL%`
The `%CHANNEL%` variable is replaced with the name of the channel

```
[Rival_Laura] !command add channel This channel is %CHANNEL%
[CactusBot] Command !channel added. 
[Epicness] !channel 
[CactusBot] This channel is Xyntak
```
