# Image renamer

Production [![build status](https://gitlab.com/miicat/img_renamer/badges/production/pipeline.svg)](https://gitlab.com/miicat/img_renamer/commits/production)

Master [![build status](https://gitlab.com/miicat/img_renamer/badges/master/pipeline.svg)](https://gitlab.com/miicat/img_renamer/commits/master)

## Description

**img_renamer** is a Python script to rename images in numberic order.


## Usage

### Rename with CLI

This will rename all images in `~/Pictures` folder like this: `0000001.png`, `0000002.png`, `0000003.png`...
```
img_renamer ~/Pictures
```

### Rename non-interactively / automatic yes to prompts

This will rename all images in `~/Pictures` folder without asking anything. It will still show list what is being renamed
```
img_renamer -y ~/Pictures
```

### Renaming modes

#### Mode 0 / Fill numbers from the end

When using this mode, and you have deleted numbers. The empty space will be filled with new images or from the end of the numbers.

If you run the command and you have the images like this: `0000001.png`, `0000003.png`, `0000004.png`, `0000005.png`  
It will become like this (The last number `0000005.png` will fill the missing `0000002.png`): `0000001.png`, `0000002.png`, `0000003.png`, `0000004.png`

```
img_renamer -m 0 ~/Pictures
```

#### Mode 1 / Move the numbers backwards

When using this mode, and you have deleted numbers. All numbers will be moved backwards, if you have new numbers, those will be added to the end.

If you run the command and you have the images like this: `0000001.png`, `0000003.png`, `0000004.png`, `0000005.png`  
It will become like this (`0000003.png` will become `0000002.png` and `0000004.png` will become `0000003.png`...): `0000001.png`, `0000002.png`, `0000003.png`, `0000004.png`

```
img_renamer -m 1 ~/Pictures
```

### Print help text

Simply run this
```
img_renamer --help
```

## Author
[Miika Launiainen](https://gitlab.com/miicat)

## License

This library is licensed under GPLv3
