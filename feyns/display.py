import os
from glob import glob
from pdf2image import convert_from_path

def convert(fname):
  pages = convert_from_path(fname)
  pages[0].save(fname.replace('.pdf','.png'),'PNG')

for f in glob('*.pdf'):
  convert(f)

pngs = sorted(glob('*.png'))

with open('README.md','w') as f:
  f.write('# List of diagrams already available\n\n')

  f.write('The following diagrams are available in this directory in .tex, .png and .pdf format.\n\n')

  for png in pngs:
    f.write('- [`{}`]({})\n\n'.format(png.replace('.png',''),png.replace('.png','.pdf')))
    f.write('  ![image]({})\n\n'.format(png))

