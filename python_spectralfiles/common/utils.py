# General utilities 

import os

# Convert wavenumber [cm-1] to wavelength [nm]
def wn2wl(wn:float) -> float:
    if wn == 0:
        return float("inf")
    else:
        return 10000000.0 / wn

# Convert wavelength [nm] to wavenumber [cm-1]
def wl2wn(wl:float) -> float:
    if wl == 0:
        return float("inf")
    else:
        return 10000000.0 / wl
    
# Return absolute path to pytools directory
def get_tools_dir():
    return os.path.join(os.path.abspath(os.environ["RAD_DIR"]), "python_spectralfiles/")

# Check if output folder exists
def check_output_exists():
    return os.path.exists( os.path.join(get_tools_dir() , "output/" )  )

# DACE temperature grid [K]
grid_t = [  50,
            100,
            150,
            200,
            250,
            300,
            350,
            400,
            450,
            500,
            550,
            600,
            650,
            700,
            800,
            900,
            1000,
            1100,
            1200,
            1300,
            1400,
            1500,
            1700,
            1900,
            2100,
            2300,
            2500,
            2700,
            2900]
grid_t = [float(v) for v in grid_t]

# DACE pressure grid [bar]
grid_p = [  9.8692326700000007768e-09,  # these are in atmosphere units
            2.1262617228243976416e-08,
            4.5808920157398465827e-08,
            9.8692326699999991224e-08,
            2.1262617228243975093e-07,
            4.580892015739846318e-07,
            9.8692326700000004459e-07,
            2.1262617228243974034e-06,
            4.5808920157398460004e-06,
            9.8692326700000012929e-06,
            2.1262617228243976575e-05,
            4.5808920157398456616e-05,
            9.8692326700000002765e-05,
            0.00021262617228243998937,
            0.00045808920157398413248,
            0.00098692326700000002765,
            0.0021262617228243996768,
            0.0045808920157398413248,
            0.0098692326700000002765,
            0.021262617228243983758,
            0.045808920157398416717,
            0.098692326699999999295,
            0.21262617228243987921,
            0.45808920157398430595,
            0.98692326699999999295,
            2.1262617228243989587,
            4.5808920157398427264,
            9.8692326700000005957,
            21.262617228243986034,
            45.808920157398411277,
            98.692326699999995299,
            212.62617228243999534,
            458.0892015739841554,
            986.92326700000000983]
grid_p = [float(v*1.0e-8/9.86923267e-09) for v in grid_p] # convert to bar


