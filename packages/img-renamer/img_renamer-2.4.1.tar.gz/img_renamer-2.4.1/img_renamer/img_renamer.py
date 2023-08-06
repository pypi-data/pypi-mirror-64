#!/usr/bin/env python
from os import path
from os import listdir
from os import rename as osrename
from sys import argv
from getopt import getopt
from getopt import GetoptError
from re import search
from re import compile


# Variables
yes = False
log = False
nro = 0
zeroes = 7
mode = 0
modes = [0, 1]
nro_total = 0
nro_to_skip = []
folder = ''
images = []
images_to_rename = []
img_extension = compile(r'\.[pngje]+$')
img_numbers = compile(r'(^\d+)\.[pngje]+$')


def main():
    get_args(argv[1:])
    get_images()
    get_images_to_rename()
    rename_images()


def get_args(args):
    # If no args given, show usage
    if len(args) < 1:
        usage_text()
        exit(0)
    # check if --help is written
    if args[0] == '--help':
        help_text()
    # Parse arguments
    try:
        opts, args = getopt(args, 'hyln:dz:dm:d')
    except GetoptError as e:
        print(e)
        help_text()
        exit(0)
    # Get options
    for opt, arg in opts:
        if opt == '-h':
            help_text()
        elif opt == '-y':
            global yes
            yes = True
        elif opt == '-n':
            if int(arg) < 0:
                print('You can\'t start counting from negative number')
                exit(0)
            global nro
            nro = int(arg) - 1
        elif opt == '-z':
            if int(arg) < 0:
                print('You can\'t have negative number of zeroes')
                exit(0)
            global zeroes
            zeroes = int(arg)
        elif opt == '-m':
            if int(arg) not in modes:
                print('This mode doesn\'t exists')
                exit(0)
            global mode
            mode = int(arg)
        elif opt == '-l':
            global log
            log = True
            print('log is true')
    # Get folder
    try:
        if path.exists(str(args[0])):
            global folder
            if search(r'/$', str(args[0])):
                folder = str(args[0])
            else:
                folder = '{folder}/'.format(folder=args[0])
        else:
            print('Folder doesn\'t exist')
            exit(0)
    except IndexError:
        print('Please define folder location')
        exit(0)


def get_images():
    imgs = listdir(folder)
    global images
    for image in imgs:
        if img_extension.search(image):
            images.append(image)
    global nro_total
    nro_total = len(images)


def get_images_to_rename():
    global images_to_rename
    global images
    nmax = nro_total
    global nro_to_skip
    if mode == 1:
        # Find all numbers
        nros = []
        nros_missing = []
        # Get numbers to list
        for image in images:
            try:
                i = img_numbers.search(image).group(1)
            except Exception:
                continue
            if len(i) == zeroes:
                nros.append(int(i))
        # Findout what numbers are missing
        nros = sorted(nros)
        i = nro + 1
        for n in nros:
            while(True):
                if not i == n:
                    nros_missing.append(i)
                else:
                    i += 1
                    break
                i += 1
        # Create list what to rename to what
        images = sorted(images)
        if not len(nros_missing) == 0:
            for image in images:
                try:
                    i = img_numbers.search(image).group(1)
                except Exception:
                    # skip other images for now
                    continue
                if int(i) < nros_missing[0]:
                    continue
                ext = img_extension.search(image).group()
                images_to_rename.append([image, generate_name(nros_missing[0]) +
                                         ext])
                del nros_missing[0]
                nros_missing.append(int(i))
                nros_missing = sorted(nros_missing)
        # Add other images to the end of the list
        i = nro_total
        for image in images:
            try:
                img_numbers.search(image).group(1)
            except Exception:
                ext = img_extension.search(image).group()
                images_to_rename.append([image, generate_name(i) + ext])
                i += 1
    elif mode == 0:
        for image in images:
            try:
                i = img_numbers.search(image).group(1)
            except Exception:
                images_to_rename.append(image)
                continue
            if int(i) > nmax + nro or int(i) <= nro:
                # the range needs to be the range of numbers to use in renaming
                images_to_rename.append(image)
            elif not len(i) == zeroes:
                images_to_rename.append(image)
            else:
                nro_to_skip.append(int(i))
    if len(images_to_rename) == 0:
        print('Nothing to rename')
        exit(0)


def rename_images():
    n = nro + 1
    rename = []
    rename_total = 0
    # Create list of images to rename with name to rename to
    if mode == 1:
        # The list is already created in the previous function,
        #  so only copying
        for image in images_to_rename:
            rename.append([image[0], image[1]])
        rename_total = len(rename)
    elif mode == 0:
        for i in range(n, nro_total + n):
            # the range needs to be the range of numbers to use in renaming
            if i not in nro_to_skip:
                ext = img_extension.search(images_to_rename[0]).group()
                rename.append([images_to_rename[0], generate_name(i) + ext])
                images_to_rename.remove(images_to_rename[0])
                rename_total += 1
            if len(images_to_rename) == 0:
                break
    # Ask about renaming
    if not yes:
        print('These will be renamed:')
        n = -1
        for i in rename:
            n += 1
            print('{r0} -> {r1}'.format(r0=rename[n][0], r1=rename[n][1]))
        print('_'*20)
        print('Renaming {nro} of {total}'.format(nro=rename_total,
                                                 total=nro_total))
        y = input('Are you sure you want to rename (y/n): ')
        if y.lower() == 'n':
            print('Aborting')
            exit(0)
        if not log:
            y = input('Do you want to save a log file (y/n): ')
            if y.lower() == 'y':
                create_log(rename)
    elif log:
        create_log(rename)
    if yes:
        print('Renaming:')
        n = -1
        for i in rename:
            n += 1
            print('{r0} -> {r1}'.format(r0=rename[n][0], r1=rename[n][1]))
        print('_'*20)
        print('Renaming {nro} of {total}'.format(nro=rename_total,
                                                 total=nro_total))
    # Rename images with xxx prefix
    n = -1
    for i in rename:
        n += 1
        osrename('{folder}{r0}'.format(folder=folder, r0=rename[n][0]),
                 '{folder}xxx{r1}'.format(folder=folder, r1=rename[n][1]))
    # Rename images to correct name
    n = -1
    for i in rename:
        n += 1
        osrename('{folder}xxx{r1}'.format(folder=folder, r1=rename[n][1]),
                 '{folder}{r1}'.format(folder=folder, r1=rename[n][1]))


def generate_name(number):
    n = zeroes - len(str(number))
    return('0'*n + str(number))


def create_log(rename_list):
    text = ''
    n = -1
    for i in rename_list:
        n += 1
        text += '{r0} -> {rl1}\n'.format(r0=rename_list[n][0],
                                         rl1=rename_list[n][1])
    with open('rename.log', 'w+') as f:
        f.write(text)


def help_text():
    # Print help text and exit
    usage_text()
    print('\n'
          'img_renamer is a command line interface for renaming images in'
          'numberic order.\n\n'
          '-l\t\tSave logfile [rename.log].\n'
          '-y\t\tAutomatic yes to prompts; assume "yes" as answer to all'
          'prompts and run non-interactively.\n'
          '-n NRO\t\tDefine custom number to start counting from.\n'
          '-z NRO\t\tDefine custom number of zeroes before number.\n'
          '-m NRO\t\tChoose what renaming mode to use.\n'
          '\t\t\t0 (Default) Fill numbers from the end or with new images.'
          'And then add new images to the end.\n'
          '\t\t\t1 Move the numbers backwards(if needed) and add new images to'
          'the end.\n\n'
          '-h, --help\tPrint this help text and exit.\n\n'
          'Programmed by @Miicat_47')
    exit(0)


def usage_text():
    # Print usage (also part of help_text)
    print('Usage: renamer [OPTIONS] [FOLDER]')


if __name__ == '__main__':
    main()
