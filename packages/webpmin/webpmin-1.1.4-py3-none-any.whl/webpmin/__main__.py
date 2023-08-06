"""
This is a tool written in pure Python to, minify WebP files by stripping out
ancillary data that is used to track the file's origins, which might breach
the privacy (eg. EXIF data).

How? See this post: https://reddit.com/7thzum.

Other chunks, (eg. ICCP) stores the color profile which is quite unnecessary.
It can also eliminate nonstandard chunks which are harmful or unnecessary.
"""

import argparse
from functools import partial
from .webpio import *

REQUIRED_CHUNKS = set((b'VP8 ', b'VP8L'))
SEMI_OPT_CHUNKS = set((b'VP8X', b'ANIM', b'ANMF', b'ALPH'))

parser = argparse.ArgumentParser(__name__, 
    formatter_class= argparse.RawTextHelpFormatter,
    description= __doc__)

parser.add_argument('input',
    type= argparse.FileType('rb'),
    help= "Input file to read WebP data from")

parser.add_argument('output',
    type= argparse.FileType('wb'),
    help= "Output file to write WebP data to")

parser.add_argument('--include',
    dest= 'inclchks', metavar= '', default= set(),
    type= lambda c: set(map(lambda _c: _c.encode('ascii')[:4].ljust(4), c.split(','))),
    help= "Include user-defined chunks separted with commas. If chunk\n"
          "names are over four bytes, latter ones are excluded. By default\n"
          "ANIM, ANMF, ALPH (semi essential chunks) will escape this filter.")

parser.add_argument('--exclude',
    dest= 'exclchks', metavar= '', default= set(),
    type= lambda c: set(map(lambda _c: _c.encode('ascii')[:4].ljust(4), c.split(','))),
    help= "Exclude user-defined chunks separte with commas. Still, essential\n"
          "chunks will escape this filter.")

argv = parser.parse_args()

def main():
    win = WebPParser(argv.input)
    wout = WebPUnparser(argv.output)

    # counts how many bytes were reduced while minfication.
    size_reduced = 0

    for seg in win:
        if seg.name in REQUIRED_CHUNKS or seg.name in (SEMI_OPT_CHUNKS | argv.inclchks - argv.exclchks):
            wout << seg
        else:
            size_reduced+= seg.size + 8
    
    print("Size reduced by: %d bytes" % size_reduced)

if __name__ == "__main__": main()
