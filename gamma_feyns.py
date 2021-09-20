import os
os.system('mkdir -p feyns')
from feyn import tree_external, tree_internal

# B+ -> D0b K+
dec = tree_external(
    A_label=r'$\Bp$',
    A_quarks=(r'$\bquarkbar$',r'$\uquark$'),
    B_label=r'$\Kp$',
    B_quarks=(r'$\squarkbar$',r'$\uquark$'),
    C_label=r'$\Dzb$',
    C_quarks=(r'$\cquarkbar$',r'$\uquark$'),
    W_label = r'\small{$\Wp$}',
    fname='feyns/Bp2DzbKp' )

# B- -> D0 K-
dec = tree_external(
    A_label=r'$\Bm$',
    A_quarks=(r'$\bquark$',r'$\uquarkbar$'),
    B_label=r'$\Km$',
    B_quarks=(r'$\squark$',r'$\uquarkbar$'),
    C_label=r'$\Dz$',
    C_quarks=(r'$\cquark$',r'$\uquarkbar$'),
    W_label = r'\small{$\Wm$}',
    anti_at_top = False,
    fname='feyns/Bm2DzKm' )

# B+ -> D0 K+
dec = tree_internal(
    A_label=r'$\Bp$',
    A_quarks=(r'$\bquarkbar$',r'$\uquark$'),
    B_label=r'$\Dz$',
    B_quarks=(r'$\uquarkbar$',r'$\cquark$'),
    C_label=r'$\Kp$',
    C_quarks=(r'$\squarkbar$',r'$\uquark$'),
    W_label = r'\small{$\Wp$}',
    fname='feyns/Bp2DzKp' )

# B- -> D0b K-
dec = tree_internal(
    A_label=r'$\Bm$',
    A_quarks=(r'$\bquark$',r'$\uquarkbar$'),
    B_label=r'$\Dzb$',
    B_quarks=(r'$\uquark$',r'$\cquarkbar$'),
    C_label=r'$\Km$',
    C_quarks=(r'$\squark$',r'$\uquarkbar$'),
    W_label = r'\small{$\Wm$}',
    anti_at_top = False,
    fname='feyns/Bm2DzbKm' )

