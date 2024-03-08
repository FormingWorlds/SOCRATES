# Physical constants 

from chemicals import MW, search_chemical

# Universal gas constant [J K-1 mol-1]
R_gas = 8.31446261815324 

# Stefan-boltzmann constant [W m−2 K−4]
sigma = 5.670367e-8 

# Avogadro's constant [mol-1]
N_av = 6.02214076e+23

# Rydberg constant (infinity) [m-1]
Ryd_inf = 10973731.568160

# Mass of proton [kg]
m_proton = 1.67262192369e-27

# Mass of electron [kg]
m_electron = 9.1093837015e-31

# Rydberg constant (hydrogen) [m-1]
Ryd_H = Ryd_inf * m_proton / (m_proton + m_electron)

# Convert isotopologue to formuka
def iso_to_formula(iso:str):
    f = ""
    atoms = iso.split("-") # Split atoms
    for a in atoms: # for each atom
        amu = True
        for c in str(a):  # for each char
            if amu: # skip AMU
                if c.isdigit():
                    continue 
                else:
                    amu=False 
            f += c
    return f

# Get chemical's safe name
def chemsafe(name:str):
    return str(search_chemical(name).formula)

# Get chemical's mean molecular weight [kg mol-1]
def mmw(form):
    return MW(chemsafe(form)) * 1.0e-3
