[](https://github.com/Procybit/Ky3M)

[![GitHub Repo stars](https://img.shields.io/github/stars/Procybit/Ky3M?style=social)](https://github.com/Procybit/Ky3M)

[![PyPI - Downloads](https://img.shields.io/pypi/dm/ky3m?style=for-the-badge)](https://pypi.org/project/ky3m/)

[![GitHub](https://img.shields.io/github/license/Procybit/Ky3M?style=for-the-badge)](LICENSE)

[![GitHub contributors](https://img.shields.io/github/contributors/Procybit/Ky3M?style=for-the-badge)](https://github.com/Procybit/Ky3M) [![GitHub commit activity](https://img.shields.io/github/commit-activity/w/Procybit/Ky3M?style=for-the-badge)](https://github.com/Procybit/Ky3M) [![GitHub issues](https://img.shields.io/github/issues-raw/Procybit/Ky3M?style=for-the-badge)](https://github.com/Procybit/Ky3M)

# Ky3M

Minecraft Mod Manager by Leon "Procybit" Shepelev

## Installing

Via pip or any other PyPI package manager:

```
python -m pip install ky3m
```

**Make sure you have Python 3.10 or above installed!**

## Program launch

Via terminal:

```
python -m ky3m
```

## Using the CLI

If the program is run correctly, this should be in the terminal:
```
Ky3M :>
```
At the moment, the only thing that can be entered into the CLI is methods.

Methods are simple commands that work directly with Ky3M internals.

The name of the method is written in CAPITAL LETTERS, the specification fields of the method are written with spaces:

```
Ky3M :> METHOD Field_1 Field_2 ANoTheR--fiEld00;[-+^ 4thFIELD
Something happened...
```

If the method name starts with the "adv" prefix, then the associated log will be displayed:

```
Ky3M :> advMETHOD Field_1 Field_2 ANoTheR--fiEld00;[-+^ 4thFIELD
Something happened...

Log intercepted!
[ky3m.methods] METHOD started!
[ky3m.something] Something happened! (something: True)
[ky3m.methods] METHOD ended!
```

## Methods

### INSPECT

Outputs all .jar files names from Minecraft mods folder.

ASSIGNS A UNIQUE ID TO EACH NEWLY OUTPUT FILE.

### PEER `id`

Outputs information about certain .jar file in Minecraft mods folder.

Uses `id`  assigned by *INSPECT*

### EXPEL `id`

Permanently deletes certain .jar file from Minecraft mods folder.

Uses `id` assigned by *INSPECT*

### ADOPT `id`

Copies certain .jar file from Minecraft mods folder to local library.

Uses `id` assigned by *INSPECT*

CAN INTERRUPT CLI AND REQUEST NAME OF SAVED FILE IF NEEDED.

DOESN'T DELETE CERTAIN FILE.

ASSIGNS A UNIQUE ID TO EACH SAVED FILE.

### ADOPTS

Outputs all saved .jar files names from local library.

### RELEASE `id`

Copies certain .jar file from local library to Minecraft mods folder.

Uses `id` assigned by *ADOPT*

### PUNISH `id`

Permanently deletes certain .jar file from local library.

Uses `id` assigned by *ADOPT*

## License
This project follows MIT license. (see [LICENSE](LICENSE))
