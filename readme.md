# BroBot

BroBot can help you workout.

## Features

`weights`: Compute the plates needed at each side of a barbell to reach the given weights.

BroBot optimizes the weight combination to minimize the number of weights that need chaining between sets.

This is optimized for two people sharing a workout plan that lift different weights and alternate sets.

Example:

```bash
brobot weights 235 180

Common plates: 35 5
First Set:     45 10
Second Set:    25 2.5
```

- Load a 5 lb plate and a 35 lb plate onto the barbell.
- Load a 10 lb and 45 lb plates for the first set.
- For the second set replace the plates from the first with those of the second.

## Installing

You can use pip to install a build:

```bash
pip install brobot-1.0.0-py3-none-any.whl
```

## Building

You can use [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) to build BroBot:

```bash
poetry build --format wheel
```

which may produce an output like this:

```bash
Building BroBot (1.0.0)
  - Building wheel
  - Built brobot-1.0.0-py3-none-any.whl
```
