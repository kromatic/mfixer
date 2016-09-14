#!/usr/bin/env python3

import os, sys
from os.path import join
from mutagen.easyid3 import EasyID3

def fix_string_encoding(s, source_enc, desired_enc):
    '''Attempt to convert string s from source to desired encoding.
       Return s upon failure.'''
    try:
        return s.encode(source_enc).decode(desired_enc)
    except UnicodeEncodeError:
        return s

def fix_all(root, source_enc, desired_enc):
    '''Traverse desired directory, correcting file/folder names and metadata
       and deleting duplicates.'''
    print('Fixing music files in {} (source encoding = {}, '
          'desired encoding = {}):\n'.format(root, source_enc, desired_enc))
    # walk through directory
    for path, dirnames, filenames in os.walk(root, topdown=False):
        for filename in filenames:
            # first fix filename and remove file if duplicate
            filename_ = fix_string_encoding(filename, source_enc, desired_enc)
            # check if the filename actually needed fixing
            if filename_ != filename:
                # if file with correct name already in directory,
                # then remove duplicate and move on
                if filename_ in filenames:
                    os.remove(join(path, filename))
                    print('Removed duplicate: {}'.format(filename))
                    continue
                # otherwise rename the file
                else:
                    os.rename(join(path, filename), join(path, filename_))
                    print('Renamed file: {} -> {}'.format(filename, filename_))
            # fix ID3 metadata
            metadata = EasyID3(join(path, filename_))
            for tag, values in metadata.items():
                metadata[tag] = [fix_string_encoding(v, source_enc, desired_enc)
                                 for v in values]
            metadata.save()
            print('Fixed metadata: {}'.format(filename_))
        # finally fix folder names
        for dirname in dirnames:
            dirname_ = fix_string_encoding(dirname, source_enc, desired_enc)
            if dirname_ != dirname:
                os.rename(join(path, dirname), join(path, dirname_))
                print('Renamed directory: {} -> {}'.format(dirname, dirname_))

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
