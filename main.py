# Ky3M project

import os
from warnings import warn
from ky3m import main

# working dirs
minecraft_dir = os.getenv('APPDATA') + '\\.minecraft\\'
mods_dir = minecraft_dir + '\\mods'
local_dir = os.getenv('LOCALAPPDATA') + '\\Ky3M'
lml_dir = local_dir + '\\lml'
data_dir = os.getenv('APPDATA') + '\\Ky3M'


def prepare_dirs():
    # if /.minecraft/ does not exist
    if not os.path.isdir(minecraft_dir):
        raise Exception('CHECK IF MINECRAFT IS INSTALLED!')

    if not os.path.isdir(mods_dir):
        warn('mods_dir do not exist, creating it...')
        os.mkdir(mods_dir)

    if not os.path.isdir(local_dir):
        warn('local_dir do not exist, creating it...')
        os.mkdir(local_dir)
        os.mkdir(lml_dir)

    if not os.path.isdir(lml_dir):
        warn('lml_dir do not exist, creating it...')
        os.mkdir(lml_dir)

    if not os.path.isdir(data_dir):
        warn('data_dir do not exist, creating it...')
        os.mkdir(data_dir)


if __name__ == '__main__':
    # noinspection PyBroadException

    # try:
    # prepare_dirs()
    main()
    # except Exception as exception:
    #     warn(str(exception))
    #     for exception_line in traceback.format_tb(exception.__traceback__):
    #         warn(str(exception_line))
