# Manage cross-sections

# Libraries
import numpy as np
import struct, os, io
import matplotlib.pyplot as plt

# Files 
import common.phys as phys

# Object for holding cross-sections at a given T,P
class xsec():

    # Set up class
    def __init__(self, formula:str, fname:str) -> None:

        # Meta parameters
        self.dummy  = bool(len(formula) == 0)
        if not self.dummy:
            self.form   = phys.chemsafe(formula)   # Molecule formula
            self.mmw    = phys.mmw(self.form)
        else:
            self.form = "XX"
            self.mmw  = 0.0
        self.fname  = fname     # DACE filename
        self.t      = -1.0      # Temperature [K]
        self.p      = -1.0      # Pressure [bar]
        self.loaded = False     # Loaded data?

        # Data descriptive parameters
        self.numin  = -1.0      # Wavenumber min [cm-1]
        self.numax  = -1.0      # Wavenumber max [cm-1]
        self.nbins  = -1        # Quantity of wavenumber bins

        # The data itself 
        self.arr_k  = np.array([])  # Cross-sections [cm2 molec-1]
        self.arr_nu = np.array([])  # Wavenumbers [cm-1]

    # Read the filename information and use it to set scalar variables in this object
    def parse_binname(self):
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
        self.arr_k = np.array(k_read, dtype=float) * self.mmw / (1.0e3 * phys.N_av)

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

    # Read an xsc file (for validation)
    def readxsc(self):
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
        
        print(self.nbins)
        print(self.p , "bar")
        print(self.t , "K")

        # Process body 
        raw_data = np.array([],dtype=float)
        for b in body:
            raw_data = np.append(raw_data, [float(v) for v in b.split()])
        self.arr_k = raw_data

        # Generate wavenumber grid
        self.nbins = len(self.arr_k)
        self.arr_nu =  np.linspace(self.numin, self.numax, self.nbins)

        # Flag as loaded 
        self.loaded = True 


    # Return cross-section in units of cm2.molecule-1
    def cross_per_molec(self):
        return np.array(self.arr_k[:])
    
    # Return cross-section in units of cm2.g-1
    def cross_per_gram(self):
        return np.array(self.arr_k[:]) * 1.0e3 * phys.N_av / self.mmw

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
            for k in self.arr_k:
                counter += 1

                hdl.write("%10.3e" % k)
                
                if counter == 10:
                    counter = 0
                    hdl.write("\n")

            # Write footer
            hdl.write("")

        return fpath

    # Plot cross-section versus wavenumber (and optionally save to file)
    # `units` sets the cross-section units (0: cm2/g, 1: cm2/molecule)
    def plot(self, units=1, fig=None, ax=None, show=True):

        if not self.loaded:
            raise Exception("Cannot plot data because xsec object is empty!")

        if (fig==None) or (ax==None):
            fig,ax = plt.subplots(figsize=(10,5))

        lw=0.4
        
        if units == 0:
            ax.plot(self.arr_nu,self.cross_per_gram(), lw=lw)
            ax.set_ylabel("Cross-section [cm$^2$ g$^{-1}$]")
        elif units == 1:
            ax.plot(self.arr_nu, self.cross_per_molec(), lw=lw)
            ax.set_ylabel("Cross-section [cm$^2$ molecule$^{-1}$]")
        else:
            raise Exception("Invalid unit choice for plot")
        
        ax.set_xlabel("Wavenumber [cm$^{-1}$]")

        title = self.form + " : %.2f K, %.3e bar" % (self.t, self.p)
        ax.set_title(title)

        if show:
            plt.show()
            return 
        else:
            return fig,ax

