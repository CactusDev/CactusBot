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

# Modifiers

Change the output of variables. To use a modifier, append `|` and the modifier to the end of the variable name.

Multiple modifiers may be chained, and will be evaluated from left to right.

## `upper`

Replace all lowercase letters with their uppercase equivalents.

```
%USER% -> 2Cubed
%USER|upper% -> 2CUBED
```

## `lower`

Replace all uppercase letters with their lowercase equivalents.

```
%USER% -> ParadigmShift3d
%USER|lower% -> paradigmshift3d
```

## `title`

Make the first letter and all letters following non-alphanumeric characters capitalized.

```
%ARG1% -> potatoes
%ARG1|title% -> Potatoes
```

## `reverse`

Reverse the text.

```
%USER% -> Jello
%USER|reverse% -> olleJ

%USER|reverse|title% -> Ollej
```

## `tag`

Remove the initial `@`, if it exists.

```
%ARG1% -> @xCausxn
%ARG1|tag% -> xCausxn

%ARG1% -> UnwrittenFun
%ARG1|tag% -> UnwrittenFun
```

```
[artdude543] !command add +raid Let's go raid @%ARG1|tag%! beam.pro/%ARG1|tag%
[CactusBot] Added command !raid.

[Chikachi] !raid @Innectic
[CactusBot] Let's go raid @Innectic! beam.pro/Innectic

[alfw] !raid TransportLayer
[CactusBot] Let's go raid @TransportLayer! beam.pro/TransportLayer
```

## `shuffle`

Shuffle the text.

```
%ARG1% -> eenofonn
%ARG1|shuffle% -> fnonneoe

%ARG1% -> @eenofonn
%ARG1|tag|shuffle% -> ononneef
```
