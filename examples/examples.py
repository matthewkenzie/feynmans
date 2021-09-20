from feyn import tree_external, tree_internal, loop_external, loop_internal, mixing1, mixing2

import os
os.system('mkdir -p examples')

from pdf2image import convert_from_path

def convert(fname):
  pages = convert_from_path(fname)
  pages[0].save(fname.replace('.pdf','.png'),'PNG')

tree_external(fname='examples/tree_external')
convert('examples/tree_external.pdf')
tree_internal(fname='examples/tree_internal')
convert('examples/tree_internal.pdf')
loop_external(fname='examples/loop_external')
convert('examples/loop_external.pdf')
loop_internal(fname='examples/loop_internal')
convert('examples/loop_internal.pdf')
mixing1(fname='examples/mixing1')
convert('examples/mixing1.pdf')
mixing2(fname='examples/mixing2')
convert('examples/mixing2.pdf')
