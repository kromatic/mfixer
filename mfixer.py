#!/usr/bin/env python3

import os, sys
from os.path import join
from mutagen.easyid3 import EasyID3
from mutagen.id3._util import ID3NoHeaderError

def fix_string_encoding(s, source_enc, desired_enc):
    """Attempt to convert string s from source to desired encoding.
    Return s upon failure.
    """
    try:
        return s.encode(source_enc).decode(desired_enc)
    except:
        return s

# testing

def fix_all(root, source_enc, desired_enc):
    """Correct all names and metadata of files and folders and remove all
    duplicates in the directory tree rooted at root.
    """
    print('Fixing music files in {} (source encoding = {}, '
          'desired encoding = {})...\n'.format(root, source_enc, desired_enc))
    # walk through directory
    for path, dirs, files in os.walk(root, topdown=False):
        for file in files:
            # first fix ID3 metadata
            try:
                metadata = EasyID3(join(path, file))
            except ID3NoHeaderError:
                break
            for tag, values in metadata.items():
                metadata[tag] = [fix_string_encoding(v, source_enc, desired_enc)
                                 for v in values]
            metadata.save()
            # print('Fixed metadata: {}'.format(file))
            # fix filename
            file_ = fix_string_encoding(file, source_enc, desired_enc)
            # rename if the filename actually needed fixing
            if file_ != file:
                if file_ in files:
                    os.remove(join(path, file))
                else:
                    os.rename(join(path, file), join(path, file_))
                # print('Renamed file: {} -> {}'.format(file, file_))
        # finally fix folder names
        for dir in dirs:
            dir_ = fix_string_encoding(dir, source_enc, desired_enc)
            if dir_ != dir and dir_ not in dirs:
                os.rename(join(path, dir), join(path, dir_))
                # fails to handle duplicate directories
                # print('Renamed directory: {} -> {}'.format(dir, dir_))

if __name__ == '__main__':
    # parse command-line arguments
    root, source_enc, desired_enc = os.getcwd(), 'cp1252', 'cp1251'
    arg_len = len(sys.argv)
    if arg_len == 2:
        root = sys.argv[1]
    elif arg_len == 3:
        source_enc, desired_enc = sys.argv[1:]
    elif arg_len == 4:
        root, source_enc, desired_enc = sys.argv[1:]
    elif arg_len > 4:
        raise ValueError('Wrong number of command-line arguments.')
    fix_all(root, source_enc, desired_enc)
