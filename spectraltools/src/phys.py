# Physical constants

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

# Convert isotopologue to formula
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
chem_dict = {
    "Water Vapour"          :"H2O",
    "Carbon Dioxide"        :"CO2",
    "Ozone"                 :"O3",
    "Dinitrogen Oxide"      :"N2O",
    "Carbon monoxide"       :"CO",
    "Methane"               :"CH4",
    "Oxygen"                :"O2",
    "Nitrogen monoxide"     :"NO",
    "Sulphur dioxide"       :"SO2",
    "Nitrogen dioxide"      :"NO2",
    "Ammonia"               :"NH3",
    "Nitric acid"           :"HNO3",
    "Nitrogen"              :"N2",
    "CFC11"                 :"CFC11",
    "CFC12"                 :"CFC12",
    "CFC113"                :"CFC113",
    "HCFC22"                :"HCFC22",
    "HFC125"                :"HFC125",
    "HFC134A"               :"HFC134a",
    "CFC114"                :"CFC114",
    "Titanium oxide"        :"TiO",
    "Vanadium oxide"        :"VO",
    "Hydrogen"              :"H2",
    "Helium"                :"He",
    "Carbonyl sulphide"     :"OCS",
    "Sodium"                :"Na",
    "Potassium"             :"K",
    "Iron hydride"          :"FeH",
    "Chromium hydride"      :"CrH",
    "Lithium"               :"Li",
    "Rubidium"              :"Rb",
    "Cesium"                :"Cs",
    "Phosphine"             :"PH3",
    "Acetylene"             :"C2H2",
    "Hydrogen cyanide"      :"HCN",
    "Hydrogen sulphide"     :"H2S",
    "Argon"                 :"Ar",
    "Atomic oxygen"         :"O",
    "Atomic nitrogen"       :"N",
    "Nitrate radical"       :"NO3",
    "Dinitrogen pentoxide"  :"N2O5",
    "Nitrous acid"          :"HONO",
    "Peroxynitric acid"     :"HO2NO2",
    "Hydrogen peroxide"     :"H2O2",
    "Ethane"                :"C2H6",
    "Methyl radical"        :"CH3",
    "Formaldehyde"          :"H2CO",
    "Hydroperoxy radical"   :"HO2",
    "Semiheavy water"       :"HDO",
    "Hydrogen chloride"     :"HCl",
    "Hydrogen fluoride"     :"HF",
    "cis-OSSO"              :"cis-OSSO",
    "trans-OSSO"            :"trans-OSSO",
    "OSO-S"                 :"OSO-S",
    "Acetaldehyde"          :"CH3CHO",
    "Methylhydroperoxide"   :"CH3OOH",
    "Acetone"               :"CH3COCH3",
    "Methylglyoxal"         :"CH3COCHO",
    "Glyoxal"               :"CHOCHO",
    "Propanal"              :"C2H5CHO",
    "Glycolaldehyde"        :"HOCH2CHO",
    "Methyl ethyl ketone"   :"C2H5COCH3",
    "Methyl vinyl ketone"   :"MVK",
    "Methacrolein"          :"MACR",
    "Peroxyacetyl nitrate"  :"PAN",
    "Methylnitrate"         :"CH3ONO2",
    "Silicon monoxide"      :"SiO",
    "Silicon dioxide"       :"SiO2",
    "Atomic iron"           :"Fe",
    "Iron(II) oxide"        :"FeO",
    "Disodium"              :"Na2",
    "Sodium oxide"          :"NaO",
    "Atomic magnesium"      :"Mg",
    "Magnesium dimer"       :"Mg2",
    "Magnesium oxide"       :"MgO",
}

# Get chemical's safe name
def chemsafe(name:str):
    # name provided
    if name in chem_dict.keys():
        return chem_dict[name]

    # form provided
    if name in chem_dict.values():
        return name

    # nope
    return None

# Formulae's MMW in g/mol (taken from src/radiance_core/gas_list_pcf.f90 -- see references therein)
form_mmw = {
    "H2O"       : 18.0153,
    "CO2"       : 44.0100,
    "O3"        : 47.9982,
    "N2O"       : 44.0128,
    "CO"        : 28.0106,
    "CH4"       : 16.0430,
    "O2"        : 31.9988,
    "NO"        : 30.0061,
    "SO2"       : 64.0628,
    "NO2"       : 46.0055,
    "NH3"       : 17.0306,
    "HNO3"      : 63.0129,
    "N2"        : 28.0134,
    "CFC11"     : 137.368,
    "CFC12"     : 120.914,
    "CFC113"    : 187.376,
    "HCFC22"    : 86.4689,
    "HFC125"    : 120.022,
    "HFC134a"   : 102.031,
    "CFC114"    : 170.921,
    "TiO"       : 63.866,
    "VO"        : 66.9409,
    "H2"        : 2.01588,
    "He"        : 4.00260,
    "OCS"       : 60.075,
    "Na"        : 22.9897,
    "K"         : 39.0983,
    "FeH"       : 56.853,
    "CrH"       : 53.004,
    "Li"        : 6.941,
    "Rb"        : 85.4678,
    "Cs"        : 132.905,
    "PH3"       : 33.9975,
    "C2H2"      : 26.0373,
    "HCN"       : 27.0253,
    "H2S"       : 34.081,
    "Ar"        : 39.948,
    "Dry air"   : 28.966,
    "O"         : 15.9994,
    "N"         : 14.0067,
    "NO3"       : 63.0128,
    "N2O5"      : 108.010,
    "HONO"      : 47.0134,
    "HO2NO2"    : 79.0122,
    "H2O2"      : 34.0147,
    "C2H6"      : 30.0690,
    "CH3"       : 15.0345,
    "H2CO"      : 30.0260,
    "HO2"       : 33.0067,
    "HDO"       : 19.0214,
    "HCl"       : 36.461,
    "HF"        : 20.0068,
    "cis-OSSO"  : 96.129,
    "trans-OSSO": 96.129,
    "OSO-S"     : 96.129,
    "CH3CHO"    : 44.0526,
    "CH3OOH"    : 48.0413,
    "CH3COCH3"  : 58.0791,
    "CH3COCHO"  : 72.0627,
    "CHOCHO"    : 58.0361,
    "C2H5CHO"   : 58.0791,
    "HOCH2CHO"  : 60.0520,
    "C2H5COCH3" : 72.1057,
    "MVK"       : 70.0898,
    "MACR"      : 70.0898,
    "PAN"       : 121.048,
    "CH3ONO2"   : 77.0394,
    "SiO"       : 44.0849,
    "SiO2"      : 60.0843,
    "Fe"        : 55.8450,
    "FeO"       : 71.8440,
    "Na2"       : 45.9795,
    "NaO"       : 38.9892,
    "Mg"        : 24.3050,
    "Mg2"       : 48.6100,
    "MgO"       : 40.3044,
}

# Get chemical's mean molecular weight [kg mol-1]
def mmw(form):
    return form_mmw[form] * 1.0e-3
