# mfixer

A python script which fixes tag / name encoding and removes (some) duplicates in a directory of mp3 files. The mutagen package is used to handle metadata.

usage: ./mfixer.py [root] [source_enc desired_enc]

By default mfixer attempts to fix improperly encoded cyrillic files by converting from cp1252 to cp1251. For example, running ./mfixer.py ./sample will fix all the "gibberish" song titles in the sample directory.
