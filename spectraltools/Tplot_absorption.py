#!/usr/bin/env python3
# Plot absorption spectrum

# Import local files
import src.cross as cross
import src.utils as utils
import src.ptf as ptf

import os
import argparse

# Main function
def main(formula:str, source:str, target_p:str, target_t:str, yunits:str, xaxis:str, saveout:bool):

    safe = utils.sourcesafe(source)

    print("Plotting absorption spectrum of %s from %s at %.2e bar and %.2f K" % (formula, source, float(target_p), float(target_t)))

    close_path = ptf.find_closest_file(source, formula, 
                                       float(target_p), float(target_t))
                             
    yunits = yunits.strip().lower()
    match yunits:
        case "cm2g-1":          yunits_int=0
        case "cm2molecule-1":   yunits_int=1
        case "m2kg-1":          yunits_int=2
        case _:
            raise Exception("Invalid units [%s]"%yunits)

    xc = cross.xsec(formula, safe, close_path)
    xc.read(UV=False)
    xc.plot(xaxis=xaxis, lim=[None, None], yunits=yunits_int, saveout=saveout, show=True)

# Run main function
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Plot absorption spectrum')
    parser.add_argument('absorber', type=str, help='Absorber name')
    parser.add_argument('source',   type=str, help='Source database name')
    parser.add_argument('pres',     type=str, help='Target pressure [bar]')
    parser.add_argument('temp',     type=str, help='Target temperature [K]')
    parser.add_argument('--yunits', type=str, default="cm2g-1", help='y-axis units')
    parser.add_argument('--xaxis', type=str, default="wavenumber", help='x-axis units')

    args = parser.parse_args()

    saveout = True

    main(args.absorber,   # absorber
         args.source,     # database
         args.pres,       # target pressure [bar]
         args.temp,       # target temperature [K],
         args.yunits,     # y-axis units
         args.xaxis,      # x-axis quantity
         saveout     # Save plot to file
         )


# End of file
