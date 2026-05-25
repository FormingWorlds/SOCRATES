#!/usr/bin/env python3
# Download CIA databases from HITRAN website

import requests
import os

import src.utils as utils

def main():

    file_map = {
        "H2-CH4":	"H2-CH4_norm_2011.cia",
        "H2-H2":	"H2-H2_2011.cia",
        "H2-H":	    "H2-H_2011.cia",
        "H2-He":	"H2-He_2011.cia",
        
        "He-H":     "He-H_2011.cia",

        "N2-H2": 	"N2-H2_2024.cia",
        "N2-He": 	"N2-He_2018.cia",
        "N2-N2": 	"N2-N2_2021.cia",
        "N2-H2O":	"N2-H2O_2018.cia",

        "O2-CO2":	"O2-CO2_2024.cia",
        "O2-N2":	"O2-N2_2024.cia",
        "O2-O2":	"O2-O2_2024.cia",

        "CO2-CO2":  "CO2-CO2_2024.cia",
        "CO2-H2":	"CO2-H2_2024.cia",
        "CO2-He":	"CO2-He_2018.cia",
        "CO2-CH4":  "CO2-CH4_2024.cia",
        "CO2-Ar":	"CO2-Ar_2021.cia",

        "CH4-He":	"CH4-He_2018.cia",
        "CH4-Ar":   "CH4-Ar_2011.cia",
        "CH4-CH4":  "CH4-CH4_2011.cia",

    }

    # Check path
    if not os.path.exists(utils.dirs["cia"]):
        os.mkdir(utils.dirs["cia"])

    # Download the files
    flag = 0
    for p in file_map.keys():
        print("Downloading %s database"%p)

        succ = False

        for src in ["main","alternate"]:

            url = f"https://hitran.org/data/CIA/{src}/{file_map[p]}"
            out = os.path.join(utils.dirs["cia"] , "%s.cia"%p)

            # Check server
            response = requests.get(url)

            # Download file if request is ok
            if response.status_code == 200:
                utils.rmsafe(out)
                with open(out, 'wb') as file:
                    file.write(response.content)
                succ = True
                print(f"    obtained from {src}")
                break

        if not succ:
            print("    failed. Status:", response.status_code)
            flag += 1

    return flag



if __name__ == "__main__":
    flag = main()
    print("Goodbye")
    exit(flag)

