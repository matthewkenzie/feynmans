import os
import subprocess

class feyn:
  def __init__(self, fname='feyn', width=190, height=140, dx=0, dy=0,
                     grid=False, raw=False, wrap_doc=True, wrap_lhcb=True, make_pdf=True
              ):
    """
    fname     : where to write the axodraw .tex code (and put the .pdf if make_pdf=True)
    width     : total width of space required
    height    : total height of space required
    dx        : shift by this amount in x
    dy        : shift by this amount in y
    grid      : draw a grid (helps when testing)
    raw       : just make the raw axodraw code .tex file
    wrap_doc  : wrap the .tex file with documentclass etc so it can be compiled
    wrap_lhcb : wrap the .tex file with lhcb-symbols-def (which must be in current working dir)
    make_pdf  : compile a standalone pdf
    """

    self.fname = fname.replace('.tex','').replace('.pdf','')
    self.width = width
    self.height = height
    self.dx = dx
    self.dy = dy
    self.grid = grid
    self.raw = raw
    self.wrap_doc = wrap_doc
    self.wrap_lhcb = wrap_lhcb
    if self.raw:
      self.wrap_doc = False
      self.wrap_lhcb = False
    self.make_pdf = make_pdf
    if self.wrap_lhcb and self.make_pdf:
      if not os.path.exists('lhcb-symbols-def.tex'):
        raise FileNotFoundError('Cannot find lhcb-symbols-def.tex file and option wrap_lhcb is set to True')

    # defaults
    self.oval_width  = 5
    self.oval_height = 20
    self.oval_grey   = 0.7
    self.vertex_rad  = 2

    self.lines = []
    self.maxw  = 0
    self.buffer = 2

  def text(self,x,y,text=None,align=None):
    if text is None: return ''
    else:
      ret = r'\Text' + '({0},{1})'.format(x+self.dx,y+self.dy)
      if align is not None:
        if '[' in align and ']' in align:
          ret += align
        else:
          ret += '['+align+']'
      ret += f'{{{text}}}'
      return ret

  def state(self,x,y):
    ret = r'\GOval' + '({0},{1})'.format(x+self.dx,y+self.dy)
    ret += '({0},{1})(90){{{2}}}'.format(self.oval_width,self.oval_height,self.oval_grey)
    return ret

  def fermion(self,start,end,reverse=False,opts=[]):
    st = start
    ed = end
    if reverse:
      st = end
      ed = start

    optstr = ','.join( ['arrow'] + opts )

    assert(len(st)==2)
    assert(len(ed)==2)

    return r'\Line[{}]'.format(optstr) + '({0},{1})'.format(st[0]+self.dx,st[1]+self.dy) + '({0},{1})'.format(ed[0]+self.dx,ed[1]+self.dy)

  def fermion_arc(self, centre, radius, start, end, reverse=False, opts=[]):
    st = start
    ed = end
    if reverse:
      st = end
      ed = start
      if 'clockwise' in opts: opts.remove('clockwise')
      else: opts.append('clockwise')
      rms = []
      adds = []
      for opt in opts:
        if opt.startswith('arrowpos'):
          pos = float(opt.split('=')[-1])
          rms.append( opt )
          adds.append( 'arrowpos={:.2f}'.format(1-pos) )
      for rm in rms: opts.remove(rm)
      for add in adds: opts.append(add)


    optstr = ','.join( ['arrow'] + opts )

    return r'\Arc[{}]'.format(optstr) + '({0},{1})'.format(centre[0]+self.dx,centre[1]+self.dy) + '({0},{1},{2})'.format(radius,st,ed)

  def photon(self,start,end,ampl,N):
    st = start
    ed = end
    return r'\Photon' + '({0},{1})'.format(st[0]+self.dx,st[1]+self.dy) + '({0},{1})'.format(ed[0]+self.dx,ed[1]+self.dy) + '{{{0}}}{{{1}}}'.format(ampl,N)

  def gluon(self,start,end,ampl,N):
    st = start
    ed = end
    return r'\Gluon' + '({0},{1})'.format(st[0]+self.dx,st[1]+self.dy) + '({0},{1})'.format(ed[0]+self.dx,ed[1]+self.dy) + '{{{0}}}{{{1}}}'.format(ampl,N)

  def photon_arc(self, centre, radius, start, end, ampl, N):
    return r'\PhotonArc' + '({0},{1})'.format(centre[0]+self.dx,centre[1]+self.dy) + '({0},{1},{2})'.format(radius,start,end) + '{{{0}}}{{{1}}}'.format(ampl,N)

  def vertex(self,x,y):
    return r'\Vertex' + '({0},{1}){{{2}}}'.format(x+self.dx,y+self.dy,self.vertex_rad)

  def add_element(self, obj, comment=None):
    comm = comment or ''
    self.lines.append( [obj, comm] )
    self.maxw = max(self.maxw, len(obj) )

  def write(self, header=None):

    print(f'Writing file, {self.fname}.tex')
    with open(self.fname+'.tex','w') as f:

      if header: print(header, '\n', file=f)

      if self.wrap_doc:
        print(r'\documentclass{standalone}', file=f)
        print(r'\usepackage{axodraw2}', file=f)

      if self.wrap_lhcb:
        print(r'\usepackage{ifthen}', file=f)
        print(r'\newboolean{uprightparticles}', file=f)
        print(r'\setboolean{uprightparticles}{false}', file=f)
        print(r'\newboolean{pdflatex}', file=f)
        print(r'\setboolean{pdflatex}{true}', file=f)
        print(r'\input{lhcb-symbols-def}', file=f)

      if self.wrap_doc:
        print(r'\begin{document}', file=f)

      print(r'\begin{axopicture}'+f'({self.width},{self.height})\n',file=f)

      if self.grid:
        nx = int(self.width / 10 )
        ny = int(self.height / 10 )
        print(r'\AxoGrid(0,0)(10,10)'+f'({nx},{ny})'+r'{LightGray}{0.5}',file=f)

      for line in self.lines:
        print('  {:<{width}}'.format(line[0],width=self.maxw+self.buffer),line[1],file=f)

      print(r'\end{axopicture}',file=f)

      if self.wrap_doc:
        print(r'\end{document}', file=f)

    if self.make_pdf:
      print(f'Compiling tex file into {self.fname}.pdf')
      os.system(f'cp {self.fname}.tex /tmp/')
      if self.wrap_lhcb:
        os.system(f'cp lhcb-symbols-def.tex /tmp/')

      cwd = os.getcwd()
      os.chdir('/tmp')
      dirname = os.path.dirname(self.fname)
      basename = os.path.basename(self.fname)
      subprocess.run(f'pdflatex {basename}; axohelp {basename}; pdflatex {basename}', shell=True, check=True, capture_output=True)
      os.system(f'cp {basename}.pdf {cwd}/{dirname}')
      os.chdir(cwd)

class tree_external(feyn):
  def __init__(self,
               A_label = None, B_label = None, C_label = None,
               A_quarks = (None,None), B_quarks = (None,None), C_quarks = (None,None),
               W_label = None,
               draw_states = True,
               anti_at_top = True,
               **kwargs
               ):
    super().__init__(**kwargs)
    """
    Draw Feynman diagram (by making axodraw .tex file) for tree decay of A -> BC
    A_label  : text label for A meson (default: None draws nothing)
    B_label  : text label for B meson (default: None draws nothing)
    C_label  : text label for C meson (default: None draws nothing)
    A_quarks : text labels for A meson quarks, should be two element list or tuple,
               where the first item is the top most (default: None draws nothing)
    B_quarks : text labels for B meson quarks, should be two element list or tuple,
               where the first item is the top most (default: None draws nothing)
    C_quarks : text labels for C meson quarks, should be two element list or tuple,
               where the first item is the top most (default: None draws nothing)
    W_label  : text label for the W (default: None draws nothing)
    draw_states : draw ovals for bound states (default: True)
    anti_at_top : draw anti-fermion as the top line and fermion as the bottom line (default: True)
    """
    self.aq = 'anti-quark' if anti_at_top else 'quark'
    self.qq = 'quark' if anti_at_top else 'anti-quark'

    # A meson
    self.add_element( '% A meson' )
    self.add_element( self.text(30,92,A_quarks[0],align='lb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((85,90),(25,90),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(30,48,A_quarks[1],align='lt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((25,50),(85,50),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(18,70,A_label,align='r'), '% Label' )
      self.add_element( self.state(25,70), '% Bound State' )
    self.add_element( '' )

    # External W line
    self.add_element( '% External W line' )
    self.add_element( self.text(105,108,W_label), '% Label' )
    self.add_element( self.photon((85,90),(125,110),-2,5), '% Line' )
    self.add_element( self.vertex(85,90), '% Start Vertex' )
    self.add_element( self.vertex(125,110), '% End Vertex' )
    self.add_element( '' )

    # B meson
    self.add_element( '% B meson' )
    self.add_element( self.text(160,129,B_quarks[0],align='rb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((165,130),(125,110),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(160,91,B_quarks[1],align='rt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((125,110),(165,90),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(172,110,B_label,align='l'), '% Label' )
      self.add_element( self.state(165,110), '% Bound State' )
    self.add_element( '' )

    # C meson
    self.add_element( '% C meson' )
    self.add_element( self.text(160,56,C_quarks[0],align='rb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((165,50),(85,90),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(160,11,C_quarks[1],align='rt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((85,50),(165,10),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(172,30,C_label,align='l'), '% Label' )
      self.add_element( self.state(165,30), '% Bound State' )
    self.add_element( '' )

    # Write it
    self.write()

class tree_internal(feyn):
  def __init__(self,
               A_label = None, B_label = None, C_label = None,
               A_quarks = (None,None), B_quarks = (None,None), C_quarks = (None,None),
               W_label = None,
               draw_states = True,
               anti_at_top = True,
               **kwargs
               ):
    super().__init__(**kwargs)
    """
    Draw Feynman diagram (by making axodraw .tex file) for tree decay of A -> BC
    A_label  : text label for A meson (default: None draws nothing)
    B_label  : text label for B meson (default: None draws nothing)
    C_label  : text label for C meson (default: None draws nothing)
    A_quarks : text labels for A meson quarks, should be two element list or tuple,
               where the first item is the top most (default: None draws nothing)
    B_quarks : text labels for B meson quarks, should be two element list or tuple,
               where the first item is the top most (default: None draws nothing)
    C_quarks : text labels for C meson quarks, should be two element list or tuple,
               where the first item is the top most (default: None draws nothing)
    W_label  : text label for the W (default: None draws nothing)
    draw_states : draw ovals for bound states (default: True)
    anti_at_top : draw anti-fermion as the top line and fermion as the bottom line (default: True)
    """
    self.aq = 'anti-quark' if anti_at_top else 'quark'
    self.qq = 'quark' if anti_at_top else 'anti-quark'

    # A meson
    self.add_element( '% A meson' )
    self.add_element( self.text(30,92,A_quarks[0],align='lb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((85,90),(25,90),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(30,48,A_quarks[1],align='lt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((25,50),(85,50),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(18,70,A_label,align='r'), '% Label' )
      self.add_element( self.state(25,70), '% Bound State' )
    self.add_element( '' )

    # Internal W line
    self.add_element( '% Internal W line' )
    self.add_element( self.text(113,86,W_label), '% Label' )
    self.add_element( self.photon((85,90),(125,70),-2,5), '% Line' )
    self.add_element( self.vertex(85,90), '% Start Vertex' )
    self.add_element( self.vertex(125,70), '% End Vertex' )
    self.add_element( '' )

    # B meson
    self.add_element( '% B meson' )
    self.add_element( self.text(160,129,B_quarks[0],align='rb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((165,130),(85,90),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(160,84,B_quarks[1],align='rt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((125,70),(165,90),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(172,110,B_label,align='l'), '% Label' )
      self.add_element( self.state(165,110), '% Bound State' )
    self.add_element( '' )

    # C meson
    self.add_element( '% C meson' )
    self.add_element( self.text(160,56,C_quarks[0],align='rb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((165,50),(125,70),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(160,11,C_quarks[1],align='rt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((85,50),(165,10),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(172,30,C_label,align='l'), '% Label' )
      self.add_element( self.state(165,30), '% Bound State' )
    self.add_element( '' )

    # Write it
    self.write()

class loop_external(feyn):
  def __init__(self,
               A_label = None, B_label = None, C_label = None,
               A_quarks = (None,None), B_quarks = (None,None), C_quarks = (None,None),
               W_label = None,
               loop_label = None,
               draw_states = True,
               anti_at_top = True,
               **kwargs
               ):
    super().__init__(**kwargs)
    """
    Draw Feynman diagram (by making axodraw .tex file) for loop decay of A -> BC
    A_label  : text label for A meson (default: None draws nothing)
    B_label  : text label for B meson (default: None draws nothing)
    C_label  : text label for C meson (default: None draws nothing)
    A_quarks : text labels for A meson quarks, should be two element list or tuple,
               where the first item is the top most (default: None draws nothing)
    B_quarks : text labels for B meson quarks, should be two element list or tuple,
               where the first item is the top most (default: None draws nothing)
    C_quarks : text labels for C meson quarks, should be two element list or tuple,
               where the first item is the top most (default: None draws nothing)
    W_label  : text label for the W (default: None draws nothing)
    loop_label  : text label for the fermion in the loop (default: None draws nothing)
    draw_states : draw ovals for bound states (default: True)
    anti_at_top : draw anti-fermion as the top line and fermion as the bottom line (default: True)
    """
    self.aq = 'anti-quark' if anti_at_top else 'quark'
    self.qq = 'quark' if anti_at_top else 'anti-quark'

    # A meson
    self.add_element( '% A meson' )
    self.add_element( self.text(30,92,A_quarks[0],align='lb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((64,90),(25,90),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(30,48,A_quarks[1],align='lt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((25,50),(85,50),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(18,70,A_label,align='r'), '% Label' )
      self.add_element( self.state(25,70), '% Bound State' )
    self.add_element( '' )

    # Loop
    self.add_element( '% Loop' )
    self.add_element( self.text(80,115,W_label), '% W Label' )
    self.add_element( self.photon_arc((87,87),23,35,173,-2,7), '% W Line' )
    self.add_element( self.text(83,88,loop_label), '% fermion Label' )
    self.add_element( self.fermion_arc((83,103),23,355,290,reverse=not anti_at_top, opts=['clockwise','arrowpos=0.4']), '% fermion Line1')
    self.add_element( self.fermion_arc((83,103),23,290,215,reverse=not anti_at_top, opts=['clockwise','arrowpos=0.4']), '% fermion Line2')
    self.add_element( self.vertex(64,90), '% Start Vertex')
    self.add_element( self.vertex(106,100.5), '% End Vertex')
    # Gluon
    self.add_element( '% Gluon' )
    self.add_element( self.gluon((97,84),(125,70),-3.5,3), '% gluon Line')
    self.add_element( self.vertex(125,70), '% Start Vertex')
    self.add_element( self.vertex(97,84), '% End Vertex')

    # B meson
    self.add_element( '% B meson' )
    self.add_element( self.text(160,129,B_quarks[0],align='rb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((165,130),(106,100.5),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(160,84,B_quarks[1],align='rt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((125,70),(165,90),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(172,110,B_label,align='l'), '% Label' )
      self.add_element( self.state(165,110), '% Bound State' )
    self.add_element( '' )

    # C meson
    self.add_element( '% C meson' )
    self.add_element( self.text(160,56,C_quarks[0],align='rb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((165,50),(125,70),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(160,11,C_quarks[1],align='rt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((85,50),(165,10),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(172,30,C_label,align='l'), '% Label' )
      self.add_element( self.state(165,30), '% Bound State' )
    self.add_element( '' )

    # Write it
    self.write()

class loop_internal(feyn):
  def __init__(self,
               A_label = None, B_label = None, C_label = None,
               A_quarks = (None,None), B_quarks = (None,None), C_quarks = (None,None),
               W_label = None,
               loop_label = None,
               draw_states = True,
               anti_at_top = True,
               **kwargs
               ):
    super().__init__(**kwargs)
    """
    Draw Feynman diagram (by making axodraw .tex file) for loop decay of A -> BC
    A_label  : text label for A meson (default: None draws nothing)
    B_label  : text label for B meson (default: None draws nothing)
    C_label  : text label for C meson (default: None draws nothing)
    A_quarks : text labels for A meson quarks, should be two element list or tuple,
               where the first item is the top most (default: None draws nothing)
    B_quarks : text labels for B meson quarks, should be two element list or tuple,
               where the first item is the top most (default: None draws nothing)
    C_quarks : text labels for C meson quarks, should be two element list or tuple,
               where the first item is the top most (default: None draws nothing)
    W_label  : text label for the W (default: None draws nothing)
    loop_label  : text label for the fermion in the loop (default: None draws nothing)
    draw_states : draw ovals for bound states (default: True)
    anti_at_top : draw anti-fermion as the top line and fermion as the bottom line (default: True)
    """
    self.aq = 'anti-quark' if anti_at_top else 'quark'
    self.qq = 'quark' if anti_at_top else 'anti-quark'

    # A meson
    self.add_element( '% A meson' )
    self.add_element( self.text(30,92,A_quarks[0],align='lb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((85,90),(25,90),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(30,48,A_quarks[1],align='lt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((25,50),(85,50),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(18,70,A_label,align='r'), '% Label' )
      self.add_element( self.state(25,70), '% Bound State' )
    self.add_element( '' )

    # Loop
    self.add_element( '% Loop' )
    self.add_element( self.text(105,75,W_label), '% W Label' )
    self.add_element( self.photon_arc((108,86),23,171,312,-3,8), '% W Line' )
    self.add_element( self.text(100,105,loop_label), '% fermion Label' )
    self.add_element( self.fermion_arc((102,74),23,350,45,reverse=not anti_at_top, opts=['arrowpos=0.65']), '% fermion Line1')
    self.add_element( self.fermion_arc((102,74),23,45,135,reverse=not anti_at_top, opts=['arrowpos=0.55']), '% fermion Line2')
    self.add_element( self.vertex(85,90), '% Start Vertex')
    self.add_element( self.vertex(125,70), '% End Vertex')
    # Gluon
    self.add_element( '% Gluon' )
    self.add_element( self.gluon((113,95),(135,110),-3.5,3), '% gluon Line')
    self.add_element( self.vertex(113,95), '% Start Vertex')
    self.add_element( self.vertex(135,110), '% End Vertex')

    # B meson
    self.add_element( '% B meson' )
    self.add_element( self.text(160,129,B_quarks[0],align='rb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((165,130),(135,110),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(160,91,B_quarks[1],align='rt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((135,110),(165,90),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(172,110,B_label,align='l'), '% Label' )
      self.add_element( self.state(165,110), '% Bound State' )
    self.add_element( '' )

    # C meson
    self.add_element( '% C meson' )
    self.add_element( self.text(160,56,C_quarks[0],align='rb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((165,50),(125,70),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(160,11,C_quarks[1],align='rt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((85,50),(165,10),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(172,30,C_label,align='l'), '% Label' )
      self.add_element( self.state(165,30), '% Bound State' )
    self.add_element( '' )

    # Write it
    self.write()

class mixing1(feyn):
  def __init__(self,
               A_label = None, Abar_label = None,
               A_quarks = (None,None), Abar_quarks = (None,None),
               qt_label = None, qb_label = None,
               Wl_label = None, Wr_label = None,
               draw_states = True,
               anti_at_top = True,
               **kwargs
               ):
    super().__init__(**kwargs)
    """
    Draw Feynman diagram (by making axodraw .tex file) for mixing of A -> Abar
    A_label     : text label for A meson (default: None draws nothing)
    Abar_label  : text label for Abar meson (default: None draws nothing)
    A_quarks    : text labels for A meson quarks, should be two element list or tuple,
                  where the first item is the top most (default: None draws nothing)
    Abar_quarks : text labels for Abar meson quarks, should be two element list or tuple,
                  where the first item is the top most (default: None draws nothing)
    qt_label    : text label for the top box quark (default: None draws nothing)
    qb_label    : text label for the bottom box quark (default: None draws nothing)
    Wl_label    : text label for the left box W (default: None draws nothing)
    Wr_label    : text label for the right box W (default: None draws nothing)
    draw_states : draw ovals for bound states (default: True)
    anti_at_top : draw anti-fermion as the top line and fermion as the bottom line (default: True)
    """
    self.aq = 'anti-quark' if anti_at_top else 'quark'
    self.qq = 'quark' if anti_at_top else 'anti-quark'

    # A meson
    self.add_element( '% A meson' )
    self.add_element( self.text(40,92,A_quarks[0],align='lb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((75,90),(35,90),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(40,48,A_quarks[1],align='lt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((35,50),(75,50),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(28,70,A_label,align='r'), '% Label' )
      self.add_element( self.state(35,70), '% Bound State' )
    self.add_element( '' )

    # Box
    self.add_element( '% Box' )
    self.add_element( self.text(95,92,qt_label,align='b'), '% q Top Label' )
    self.add_element( self.fermion((115,90),(75,90),reverse=not anti_at_top ), f'% {self.aq} Top Box Line' )
    self.add_element( self.text(95,48,qb_label,align='t'), '% q Bottom Label' )
    self.add_element( self.fermion((75,50),(115,50),reverse=not anti_at_top), f'% {self.qq} Bottom Box Line')
    self.add_element( self.text(71,70,Wl_label,align='r'), '% W Left Label')
    self.add_element( self.photon((75,90),(75,50),4,4), f'% W Left Box Line')
    self.add_element( self.text(119,70,Wr_label,align='l'), '% W Right Label')
    self.add_element( self.photon((115,90),(115,50),4,4), f'% W Right Box Line')
    self.add_element( self.vertex(75,90), '% Top Left Vertex' )
    self.add_element( self.vertex(115,90), '% Top Right Vertex' )
    self.add_element( self.vertex(75,50), '% Bottom Left Vertex' )
    self.add_element( self.vertex(115,50), '% Bottom Right Vertex' )

    # Abar meson
    self.add_element( '% Abar meson' )
    self.add_element( self.text(150,92,Abar_quarks[0],align='rb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((155,90),(115,90),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(150,48,Abar_quarks[1],align='rt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((115,50),(155,50),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(162,70,Abar_label,align='l'), '% Label' )
      self.add_element( self.state(155,70), '% Bound State' )
    self.add_element( '' )

    # Write it
    self.write()

class mixing2(feyn):
  def __init__(self,
               A_label = None, Abar_label = None,
               A_quarks = (None,None), Abar_quarks = (None,None),
               ql_label = None, qr_label = None,
               Wt_label = None, Wb_label = None,
               draw_states = True,
               anti_at_top = True,
               **kwargs
               ):
    super().__init__(**kwargs)
    """
    Draw Feynman diagram (by making axodraw .tex file) for mixing of A -> Abar
    A_label     : text label for A meson (default: None draws nothing)
    Abar_label  : text label for Abar meson (default: None draws nothing)
    A_quarks    : text labels for A meson quarks, should be two element list or tuple,
                  where the first item is the top most (default: None draws nothing)
    Abar_quarks : text labels for Abar meson quarks, should be two element list or tuple,
                  where the first item is the top most (default: None draws nothing)
    ql_label    : text label for the left box quark (default: None draws nothing)
    qr_label    : text label for the right box quark (default: None draws nothing)
    Wt_label    : text label for the top box W (default: None draws nothing)
    Wb_label    : text label for the bottom box W (default: None draws nothing)
    draw_states : draw ovals for bound states (default: True)
    anti_at_top : draw anti-fermion as the top line and fermion as the bottom line (default: True)
    """
    self.aq = 'anti-quark' if anti_at_top else 'quark'
    self.qq = 'quark' if anti_at_top else 'anti-quark'

    # A meson
    self.add_element( '% A meson' )
    self.add_element( self.text(40,92,A_quarks[0],align='lb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((75,90),(35,90),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(40,48,A_quarks[1],align='lt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((35,50),(75,50),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(28,70,A_label,align='r'), '% Label' )
      self.add_element( self.state(35,70), '% Bound State' )
    self.add_element( '' )

    # Box
    self.add_element( '% Box' )
    self.add_element( self.text(95,94,Wt_label,align='b'), '% W Top Label' )
    self.add_element( self.photon((115,90),(75,90),4,4), f'% W Top Box Line' )
    self.add_element( self.text(95,46,Wb_label,align='t'), '% W Bottom Label' )
    self.add_element( self.photon((75,50),(115,50),4,4), f'% W Bottom Box Line')
    self.add_element( self.text(71,70,ql_label,align='r'), '% q Left Label')
    self.add_element( self.fermion((75,50),(75,90),reverse=not anti_at_top), f'% q Left Box Line')
    self.add_element( self.text(119,70,qr_label,align='l'), '% q Right Label')
    self.add_element( self.fermion((115,90),(115,50),reverse=not anti_at_top), f'% q Right Box Line')
    self.add_element( self.vertex(75,90), '% Top Left Vertex' )
    self.add_element( self.vertex(115,90), '% Top Right Vertex' )
    self.add_element( self.vertex(75,50), '% Bottom Left Vertex' )
    self.add_element( self.vertex(115,50), '% Bottom Right Vertex' )

    # Abar meson
    self.add_element( '% Abar meson' )
    self.add_element( self.text(150,92,Abar_quarks[0],align='rb'), f'% {self.aq} Label' )
    self.add_element( self.fermion((155,90),(115,90),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( self.text(150,48,Abar_quarks[1],align='rt'), f'% {self.qq} Label' )
    self.add_element( self.fermion((115,50),(155,50),reverse=not anti_at_top ), f'% {self.qq} Line' )
    if draw_states:
      self.add_element( self.text(162,70,Abar_label,align='l'), '% Label' )
      self.add_element( self.state(155,70), '% Bound State' )
    self.add_element( '' )

    # Write it
    self.write()

class loop_external_quark(feyn):
  def __init__(self,
               A_quark = None, B_quark = None, C_fermions = (None,None),
               W_label = None,
               loop_label = None,
               anti_at_top = True,
               **kwargs
               ):
    super().__init__(**kwargs)
    """
    Draw Feynman diagram (by making axodraw .tex file) for loop decay of A -> BC
    A_quark  : text label for A quark (default: None draws nothing)
    B_quark  : text label for B quark (default: None draws nothing)
    C_fermions : text labels for C fermions, should be two element list or tuple,
               where the first item is the top most (default: None draws nothing)
    W_label  : text label for the W (default: None draws nothing)
    loop_label  : text label for the fermion in the loop (default: None draws nothing)
    anti_at_top : draw anti-fermion as the top line and fermion as the bottom line (default: True)
    """
    self.aq = 'anti-quark' if anti_at_top else 'quark'
    self.qq = 'quark' if anti_at_top else 'anti-quark'

    # A quark
    self.add_element( '% A quark' )
    self.add_element( self.text(23,90,A_quark,align='r'), f'% {self.aq} Label' )
    self.add_element( self.fermion((64,90),(25,90),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( '' )

    # Loop
    self.add_element( '% Loop' )
    self.add_element( self.text(80,115,W_label), '% W Label' )
    self.add_element( self.photon_arc((87,87),23,35,173,-2,7), '% W Line' )
    self.add_element( self.text(83,88,loop_label), '% fermion Label' )
    self.add_element( self.fermion_arc((83,103),23,355,290,reverse=not anti_at_top, opts=['clockwise','arrowpos=0.4']), '% fermion Line1')
    self.add_element( self.fermion_arc((83,103),23,290,215,reverse=not anti_at_top, opts=['clockwise','arrowpos=0.4']), '% fermion Line2')
    self.add_element( self.vertex(64,90), '% Start Vertex')
    self.add_element( self.vertex(106,100.5), '% End Vertex')
    # Gluon
    self.add_element( '% Gluon' )
    self.add_element( self.gluon((97,84),(125,70),-3.5,3), '% gluon Line')
    self.add_element( self.vertex(125,70), '% Start Vertex')
    self.add_element( self.vertex(97,84), '% End Vertex')

    # B quark
    self.add_element( '% B quark' )
    self.add_element( self.text(167,130,B_quark,align='l'), f'% {self.aq} Label' )
    self.add_element( self.fermion((165,130),(106,100.5),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( '' )

    # C fermions
    self.add_element( '% C fermions' )
    self.add_element( self.text(167,90,C_fermions[0],align='l'), f'% {self.qq} Label' )
    self.add_element( self.fermion((125,70),(165,90),reverse=not anti_at_top ), f'% {self.qq} Line' )
    self.add_element( self.text(167,50,C_fermions[1],align='l'), f'% {self.aq} Label' )
    self.add_element( self.fermion((165,50),(125,70),reverse=not anti_at_top ), f'% {self.aq} Line' )
    self.add_element( '' )

    # Write it
    self.write()

