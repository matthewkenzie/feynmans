import os
os.system('mkdir -p feyns')
from feyn import tree_internal, loop_internal, loop_external

# B0 -> Kst Kstb
dec = loop_external(
    A_label=r'$\Bd$',
    A_quarks=(r'$\bquarkbar$',r'$\dquark$'),
    B_label=r'$\Kstarzb$',
    B_quarks=(r'$\dquarkbar$',r'$\squark$'),
    C_label=r'$\Kstarz$',
    C_quarks=(r'$\squarkbar$',r'$\dquark$'),
    W_label = r'\small{$\Wp$}',
    fname='feyns/Bd2KstKst' )

# B0b -> Kst Kstb
dec = loop_external(
    A_label=r'$\Bdb$',
    A_quarks=(r'$\bquark$',r'$\dquarkbar$'),
    B_label=r'$\Kstarz$',
    B_quarks=(r'$\dquark$',r'$\squarkbar$'),
    C_label=r'$\Kstarzb$',
    C_quarks=(r'$\squark$',r'$\dquarkbar$'),
    W_label = r'\small{$\Wm$}',
    anti_at_top = False,
    fname='feyns/Bdb2KstKst' )

# Bs0 -> Kst Kstb
dec = loop_external(
    A_label=r'$\Bs$',
    A_quarks=(r'$\bquarkbar$',r'$\squark$'),
    B_label=r'$\Kstarz$',
    B_quarks=(r'$\squarkbar$',r'$\dquark$'),
    C_label=r'$\Kstarzb$',
    C_quarks=(r'$\dquarkbar$',r'$\squark$'),
    W_label = r'\small{$\Wp$}',
    fname='feyns/Bs2KstKst' )

# Bs0b -> Kst Kstb
dec = loop_external(
    A_label=r'$\Bsb$',
    A_quarks=(r'$\bquark$',r'$\squarkbar$'),
    B_label=r'$\Kstarzb$',
    B_quarks=(r'$\squark$',r'$\dquarkbar$'),
    C_label=r'$\Kstarz$',
    C_quarks=(r'$\dquark$',r'$\squarkbar$'),
    W_label = r'\small{$\Wm$}',
    anti_at_top = False,
    fname='feyns/Bsb2KstKst' )

# Bs0 -> JpsiPhi Tree
dec = tree_internal(
    A_label=r'$\Bs$',
    A_quarks=(r'$\bquarkbar$',r'$\squark$'),
    B_label=r'$\jpsi$',
    B_quarks=(r'$\cquarkbar$',r'$\cquark$'),
    C_label=r'$\phi$',
    C_quarks=(r'$\squarkbar$',r'$\squark$'),
    W_label = r'\small{$\Wp$}',
    fname='feyns/Bs2JpsiPhi_tree' )

# Bsb0 -> JpsiPhi Tree
dec = tree_internal(
    A_label=r'$\Bsb$',
    A_quarks=(r'$\bquark$',r'$\squarkbar$'),
    B_label=r'$\jpsi$',
    B_quarks=(r'$\cquark$',r'$\cquarkbar$'),
    C_label=r'$\phi$',
    C_quarks=(r'$\squark$',r'$\squarkbar$'),
    W_label = r'\small{$\Wm$}',
    anti_at_top = True,
    fname='feyns/Bsb2JpsiPhi_tree' )

# Bs0 -> JpsiPhi Loop
dec = loop_internal(
    A_label=r'$\Bs$',
    A_quarks=(r'$\bquarkbar$',r'$\squark$'),
    B_label=r'$\jpsi$',
    B_quarks=(r'$\cquarkbar$',r'$\cquark$'),
    C_label=r'$\phi$',
    C_quarks=(r'$\squarkbar$',r'$\squark$'),
    W_label = r'\small{$\Wp$}',
    fname='feyns/Bs2JpsiPhi_loop' )

# Bs0b -> JpsiPhi Loop
dec = loop_internal(
    A_label=r'$\Bsb$',
    A_quarks=(r'$\bquark$',r'$\squarkbar$'),
    B_label=r'$\jpsi$',
    B_quarks=(r'$\cquark$',r'$\cquarkbar$'),
    C_label=r'$\phi$',
    C_quarks=(r'$\squark$',r'$\squarkbar$'),
    W_label = r'\small{$\Wm$}',
    anti_at_top = False,
    fname='feyns/Bsb2JpsiPhi_loop' )

