# `Filters`

Filters can change the output of variables. To use a filter, append `|` with the filter name to a varible. Ex: `ARGS|upper`

## `upper`
Makes all letters uppercase in the variable

```
%NAME|upper%` -> INNECTIC
```

## `lower`
Makes all letters lowercase in the varible

```
%NAME|lower% -> 2cubed
```

## `title`
Makes the first letter of the variable uppercase
```
%NAME|title% -> ParadigmShift3d
```

## `reverse`
Reverses the text of the variable
```
%NAME|reverse% -> nnofonee
```

## `tag`
Removes the `@` from the variable

```
@%NAME|tag% -> @duke
```

## `shuffle`
Randomizes the varible

```
%ARG1|shuffle% -> ntetik 
```
