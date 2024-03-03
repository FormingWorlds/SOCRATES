# Manage cross-sections

# Libraries
import numpy as np
import struct, os, io
import matplotlib.pyplot as plt

# Files 
import common.phys as phys
import common.utils as utils

# Object for holding cross-sections at a given T,P
class xsec():

    # Set up class
    def __init__(self, formula:str, source:str, fname:str) -> None:

        # Meta parameters
        self.dummy  = bool(len(formula) == 0)
        if not self.dummy:
            self.form   = phys.chemsafe(formula)   # Molecule formula
            self.mmw    = phys.mmw(self.form)
        else:
            self.form = "XX"
            self.mmw  = -1.0
        self.source = utils.sourcesafe(source)    # Source database
        self.fname  = fname     # Path to source file
        self.t      = -1.0      # Temperature [K]
        self.p      = -1.0      # Pressure [bar]
        self.loaded = False     # Loaded data?

        # Data descriptive parameters
        self.numin  = -1.0      # Wavenumber min [cm-1]
        self.numax  = -1.0      # Wavenumber max [cm-1]
        self.nbins  = -1        # Quantity of wavenumber bins

        # The data itself 
        self.arr_k  = np.array([])  # Cross-sections [cm2 g-1]
        self.arr_nu = np.array([])  # Wavenumbers [cm-1]

    # Read bin filename information and use it to set scalar variables in this object
    def parse_binname(self):
        if not (self.source == "dace"):
            print("WARNING: Cannot execute parse_binname because source (%s) is not DACE" % self.source)
        splt = self.fname.split("/")[-1].split(".")[0].split("_")[1:]
        self.numin = float(splt[0])  # cm-1
        self.numax = float(splt[1])  # cm-1
        self.t     = float(splt[2])  # K
        exp        = float(splt[3][1:])/100.0 # unsigned exponent for pressure
        if splt[3][0] == 'n':
            self.p = 10.0**(-1.0 * exp)  # bar
        elif splt[3][0] == 'p':
            self.p = 10.0**(+1.0 * exp)  # bar 
        else:
            raise Exception("Cannot parse DACE filename pressure value")

    # Read DACE bin file
    def readbin(self):

        if not (self.source == "dace"):
            print("WARNING: Cannot execute readbin because source (%s) is not DACE" % self.source)

        # check conflicts
        if self.loaded:
            raise Exception("This xsec object already contains data")
        if not os.access(self.fname, os.R_OK):
            raise Exception("Cannot read file '%s'" % self.fname)
        
        # get number of bins 
        nbins = 0
        with open(self.fname, "rb") as hdl:
            hdl.seek(0, io.SEEK_END)
            nbins = int(hdl.tell()/4)

        # check value is reasonable 
        if (nbins < 100) or (nbins > 1e12):
            raise Exception("Error reading DACE file. Too many bins?")
        self.nbins = nbins
        
        # Get cross-sections for each bin
        k_read = []
        with open(self.fname, "rb") as hdl:
            for _ in range(nbins):
                K = struct.unpack('f', hdl.read(4))[0]  # 4 bytes at a time (Float32)
                k_read.append(K)
        self.arr_k = np.array(k_read, dtype=float)

        # Read filename info
        self.parse_binname()

        # Set nu array 
        self.arr_nu = np.linspace(self.numin, self.numax, self.nbins)

        # Check resolution 
        eps = 1.0e-5  # numerical precision
        res = 0.01    # expected resolution
        if (self.arr_nu[5] - self.arr_nu[4] - res) > eps:
            raise Exception("Wavenumber resolution mismatch. Either file size is wrong, or resolution is not %f cm-1" % res)

        # Flag as loaded 
        self.loaded = True 

    # Read HITRAN xsc file
    def readxsc(self):
        if not (self.source == "hitran"):
            print("WARNING: Cannot execute readxsc because source (%s) is not HITRAN" % self.source)

        # check conflicts
        if self.loaded:
            raise Exception("This xsec object already contains data")
        if not os.access(self.fname, os.R_OK):
            raise Exception("Cannot read file '%s'" % self.fname)
        
        # Read file
        with open(self.fname,'r') as hdl:
           content = hdl.readlines()
        head = content[0]
        body = content[1:]

        # Process header 
        i = 20
        self.numin = float(head[i:i+10]);   i += 10
        self.numax = float(head[i:i+10]);   i += 10
        self.nbins = int(  head[i:i+7 ]);   i += 7
        self.t     = float(head[i:i+7 ]);   i += 7
        self.p     = float(head[i:i+6 ]);   i += 6
        self.p /= 750.06 # convert torr to bar 
        
        # Process body 
        raw_data = np.array([],dtype=float)
        for b in body:
            raw_data = np.append(raw_data, [float(v) for v in b.split()])
        self.arr_k = raw_data * phys.N_av / (self.mmw * 1000.0)  # cm2/molec -> cm2/gram

        # Generate wavenumber grid
        self.nbins = len(self.arr_k)
        self.arr_nu =  np.linspace(self.numin, self.numax, self.nbins)

        # Flag as loaded 
        self.loaded = True 

    # Parse ExoMol sigma file name
    def parse_sigmaname(self):
        if not (self.source == "exomol"):
            print("WARNING: Cannot execute parse_sigmaname because source (%s) is not ExoMol" % self.source)
        
        # Exomol values are always at zero pressure
        self.p = 0.0

        # Process filename
        splt = self.fname[:-6].split("_")
        splt_nu = splt[1].split("-")

        self.numin = float(splt_nu[0]) 
        self.numax = float(splt_nu[1]) 
        self.t     = float(splt[2][:-1])


    # Read ExoMol sigma file
    def readsigma(self):
        if not (self.source == "exomol"):
            print("WARNING: Cannot execute readsigma because source (%s) is not ExoMol" % self.source)

        # check conflicts
        if self.loaded:
            raise Exception("This xsec object already contains data")
        if not os.access(self.fname, os.R_OK):
            raise Exception("Cannot read file '%s'" % self.fname)
    
        self.parse_sigmaname()

        data = np.loadtxt(self.fname).T 
        self.arr_nu = data[0]
        self.arr_k  = data[1] * phys.N_av / (self.mmw * 1000.0) 
        self.nbins  = len(data[0])

        # Flag as loaded
        self.loaded = True


    # Read input variables instead of from a file (bar, K, cm-1, cm2/g)
    def readdirect(self, p, t, nu_arr, k_arr):
        # check conflicts
        if self.loaded:
            raise Exception("This xsec object already contains data")

        if len(nu_arr) != len(k_arr):
            raise Exception("nu and k arrays have different lengths")

        self.p = p 
        self.t = t
        self.arr_nu = nu_arr 
        self.numin = nu_arr[0]
        self.numax = nu_arr[1]
        self.nbins = len(nu_arr)
        self.arr_k = k_arr
        self.loaded = True

        
    # Read source file 
    def read(self, p=None, t=None, nu_arr=None, k_arr=None):
        match self.source:
            case "dace":   self.readbin()
            case "hitran": self.readxsc()
            case "exomol": self.readsigma()
            case "direct": self.readdirect(p,t,nu_arr,k_arr)

    # Return cross-section in units of cm2.molecule-1
    def cross_cm2_per_molec(self):
        if self.dummy: print("WARNING: Accessing kabs of dummy xsec object!")
        return np.array(self.arr_k[:]) * self.mmw * 1000.0 / phys.N_av
    
    # Return cross-section in units of cm2.g-1
    def cross_cm2_per_gram(self):
        if self.dummy: print("WARNING: Accessing kabs of dummy xsec object!")
        return np.array(self.arr_k[:])
    
    # Return cross-section in units of cm2.g-1
    def cross_m2_per_kg(self):
        return 100.0 * self.cross_cm2_per_gram()

    # Write to a HITRAN-formatted xsc file in the given folder
    def writexsc(self, dir:str):
        
        # File stuff
        if not self.loaded:
            raise Exception("Cannot write data because xsec object is empty!")
        if not os.path.isdir(dir):
            raise Exception("Argument must be a directory for outputting xsc files!")


        # Other header variables
        k_max   = np.amax(self.arr_k)
        ptorr   = self.p * 750.06
        ires    = 0.01
        broad   = ""
        source  = 0

        # Construct header (https://hitran.org/docs/cross-sections-definitions/)
        head = ""
        head += str.rjust(self.form, 20, ' ')
        head += str("%10.3f" % self.numin)
        head += str("%10.3f" % self.numax)
        head += str("%7d"    % self.nbins)
        head += str("%7.2f"  % self.t)
        head += str("%6.2f"  % ptorr)      # pressure in Torr
        head += str("%10.3e" % k_max)      # maximum xsec
        head += str("%5.3f"  % ires)       # instrument resolution 
        head += str("%15s"   % self.form)  # common name
        head += str("    ")                # dummy 
        head += str("%3s"    % broad)      # broadener
        head += str("%3d"    % source)     # source of data 

        # Construct filename 
        f = "%s_%4.1f-%3.2f_%.1f-%.1f_%d.xsc" % (self.form, self.t, ptorr, self.numin, self.numax, source)

        # Open and write file 
        fpath = dir+"/"+f
        with open(fpath, "w") as hdl:

            # Write header
            hdl.write(head + "\n")

            # Write data 
            counter = 0
            for k in self.cross_cm2_per_molec():
                counter += 1

                hdl.write("%10.3e" % k)
                
                if counter == 10:
                    counter = 0
                    hdl.write("\n")

            # Write footer
            hdl.write("")

        return fpath

    # Plot cross-section versus wavenumber (and optionally save to file)
    # `units` sets the cross-section units (0: cm2/g, 1: cm2/molecule, 2:m2/kg)
    def plot(self, yunits=1, fig=None, ax=None, show=True, saveout="", xmin=None, xmax=1e4):

        if not self.loaded:
            raise Exception("Cannot plot data because xsec object is empty!")

        if (fig==None) or (ax==None):
            fig,ax = plt.subplots(figsize=(10,5))

        lw=0.4
        col = 'k'

        # Crop data
        if (xmin == None):
            xmin = self.numin
        else:
            xmin = max(xmin, self.numin)
        xmin_idx = np.argmin( abs(self.arr_nu-xmin))
        if (xmax == None):
            xmax = self.numax
        else:
            xmax = min(xmax, self.numax)
        xmax_idx = np.argmin( abs(self.arr_nu-xmax))
        xlim = [xmin, xmax]

        if xmin > xmax:
            print("WARNING: Encountered invalid xlimits:", xlim)
        ax.set_xlim(xlim)

        if yunits == 0:
            yarr = self.cross_cm2_per_gram()
            ylbl = "Cross-section [cm$^2$ g$^{-1}$]"
        elif yunits == 1:
            yarr = self.cross_cm2_per_molec()
            ylbl = "Cross-section [cm$^2$ molecule$^{-1}$]"
        elif yunits == 2:
            yarr = self.cross_m2_per_kg()
            ylbl = "Cross-section [m$^2$ kg$^{-1}$]"
        else:
            raise Exception("Invalid unit choice for plot")
        
        xarr = self.arr_nu[xmin_idx:xmax_idx]
        yarr = yarr[xmin_idx:xmax_idx]
        
        ax.plot(xarr, yarr, lw=lw, color=col)

        ax.set_ylabel(ylbl)
        ax.set_xlabel("Wavenumber [cm$^{-1}$]")

        title = self.form + " : %.3e bar, %.2f K" % (self.p, self.t)
        ax.set_title(title)

        if len(saveout) > 0:
            save_path = os.path.join(utils.dirs["output"], saveout)
            print("Saving plot to '%s'"%save_path)
            utils.rmsafe(save_path)
            fig.savefig(save_path, bbox_inches="tight")
            show=False
            plt.close()

        if show:
            plt.show()
            return 
        else:
            return fig,ax

