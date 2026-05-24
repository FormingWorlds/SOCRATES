# Generate socrates wrappers

SOCRATES_DIR = normpath(ENV["RAD_DIR"])
gendir = joinpath(SOCRATES_DIR,"julia","gen")
libdir = joinpath(SOCRATES_DIR,"julia","lib")

println("Generating wrappers")
println("SOCRATES_DIR = $SOCRATES_DIR")

SOCRATES_VER = readchomp(joinpath(SOCRATES_DIR, "version"))

# Clean up
include("clean_wrappers.jl")

# Tools
include("ParseFortran.jl")
include("GenFortranWrappers.jl")

######################################################################
# Generate Julia and ISO_CBINDING Fortran wrappers for SOCRATES Types
######################################################################

wrappers = [
    # strsuffix, modsuffix, var_name
    ("Ctrl", "control", "control"),
    ("Dim", "dimen", "dimen"),
    ("SpecData", "spectrum", "spectrum"),
    ("Planck", "planck", "planck"),
    ("Atm", "atm", "atm"),
    ("Cld", "cld", "cld"),
    ("Aer", "aer", "aer"),
    ("Bound", "bound", "bound"),
    ("Out", "out", "radout")
]

for (strsuffix, modsuffix, var_name) in wrappers
    local ffile = joinpath(SOCRATES_DIR,"src/radiance_core/def_$(modsuffix).F90")
    local strctrl = ParseFortran.parse_type(joinpath(SOCRATES_DIR, ffile), "Str"*strsuffix)
    GenFortranWrappers.gen_wrappers(
        "Str"*strsuffix, strctrl;
        var_name=var_name,
        fortran_module_dependencies=["def_$(modsuffix)"],
        fortran_file=ffile,
        svn_rev=SOCRATES_VER,
    )
end


ffile = "src/radiance_core/def_spectrum.F90"
for member_name in [
        "Dim", "Basic", "Solar", "Rayleigh", "Gas", "Planck", "Cont", "ContGen", "Drop",
        "Aerosol", "Ice", "Var", "Photol", "Map",
    ]
    strmemb = ParseFortran.parse_type(joinpath(SOCRATES_DIR, ffile), "StrSpec"*member_name)
    GenFortranWrappers.gen_wrappers(
        "StrSpecData", strmemb;
        member_name=member_name,
        var_name="spectrum",
        fortran_module_dependencies=["def_spectrum"],
        fortran_file=ffile,
        svn_rev=SOCRATES_VER,
    )
end

######################################################################
# Generate Julia modules with SOCRATES parameters as Julia const variables
######################################################################

mod_pars = [
    # srcdir, modname, fext
    ("radiance_core", "rad_pcf", ".F90"),
    ("radiance_core", "gas_list_pcf", ".F90"),
    ("modules_gen", "input_head_pcf", ".f90"),
]

for (srcdir, modname, fext) in mod_pars
    local ffile = joinpath("src", srcdir, modname*fext)
    pars_pcf = ParseFortran.parse_module_parameters(
        joinpath(SOCRATES_DIR, ffile),
        modname
    )
    GenFortranWrappers.gen_pars(
        joinpath(SOCRATES_DIR,"julia/gen/$modname.jl"), modname, pars_pcf,
        fortran_file=ffile, svn_rev=SOCRATES_VER)
end

println("Done")
# readdir(joinpath(SOCRATES_DIR,"julia","gen"))
