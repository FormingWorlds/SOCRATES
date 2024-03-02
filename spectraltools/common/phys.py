# Physical constants 

from chemicals import MW, search_chemical

# Universal gas constant [J K-1 mol-1]
R_gas = 8.31446261815324 

# Stefan-boltzmann constant [W m−2 K−4]
sigma = 5.670367e-8 

# Avogadro's constant [mol-1]
N_av = 6.02214076e+23

# Get chemical's safe name
def chemsafe(name):
    return str(search_chemical(name).formula)

# Get chemical's mean molecular weight [kg mol-1]
def mmw(form):
    return MW(chemsafe(form)) * 1.0e-3
