import os
os.system('mkdir -p feyns')
from feyn import mixing1, mixing2

# Bs0 -> Bs0b mixing 1
dec = mixing1(
    A_label=r'$\Bs$',
    A_quarks=(r'$\bquarkbar$',r'$\squark$'),
    Abar_label = r'$\Bsb$',
    Abar_quarks = (r'$\squarkbar$',r'$\bquark$'),
    #qt_label = r'$\uquarkbar,\cquarkbar,\tquarkbar$',
    #qb_label = r'$\uquark,\cquark,\tquark$',
    #Wl_label = r'\small{$W$}',
    #Wr_label = r'\small{$W$}',
    fname = 'feyns/BsMixing1'
    )

# Bs0b -> Bs0 mixing 1
dec = mixing1(
    A_label=r'$\Bsb$',
    A_quarks=(r'$\bquark$',r'$\squarkbar$'),
    Abar_label = r'$\Bs$',
    Abar_quarks = (r'$\squark$',r'$\bquarkbar$'),
    #qt_label = r'$\uquark,\cquark,\tquark$',
    #qb_label = r'$\uquarkbar,\cquarkbar,\tquarkbar$',
    #Wl_label = r'\small{$W$}',
    #Wr_label = r'\small{$W$}',
    anti_at_top = False,
    fname = 'feyns/BsbMixing1'
    )

# Bs0 -> Bs0b mixing 2
dec = mixing2(
    A_label=r'$\Bs$',
    A_quarks=(r'$\bquarkbar$',r'$\squark$'),
    Abar_label = r'$\Bsb$',
    Abar_quarks = (r'$\squarkbar$',r'$\bquark$'),
    #ql_label = r'$\uquark,\cquark,\tquark$',
    #qr_label = r'$\uquark,\cquark,\tquark$',
    #Wt_label = r'\small{$\Wp$}',
    #Wb_label = r'\small{$\Wm$}',
    fname = 'feyns/BsMixing2'
    )

# Bs0b -> Bs0 mixing 2
dec = mixing2(
    A_label=r'$\Bsb$',
    A_quarks=(r'$\bquark$',r'$\squarkbar$'),
    Abar_label = r'$\Bs$',
    Abar_quarks = (r'$\squark$',r'$\bquarkbar$'),
    #ql_label = r'$\uquark,\cquark,\tquark$',
    #qr_label = r'$\uquark,\cquark,\tquark$',
    #Wt_label = r'\small{$\Wm$}',
    #Wb_label = r'\small{$\Wp$}',
    anti_at_top = False,
    fname = 'feyns/BsbMixing2'
    )





