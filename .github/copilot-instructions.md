# SOCRATES_FW Copilot Instructions

## Build, test, and lint commands

### Build
- Full build (default target set):  
  `./build_code`
- Build a specific make target through `build_code` (examples):  
  `./build_code cdl`  
  `./build_code cdf`  
  `./build_code l_run_cdf`
- Compiler/environment presets used in this repo:  
  `./build_code azure_gfortran12`  
  `./build_code azure_ifort19`  
  `./build_code monsoon3_gfortran12`
- Build the C helpers in `sbin/` only:  
  `cd sbin && make`

After building, always load runtime paths before running scripts/tools:

`. ./set_rad_env`

### Tests
- Quick regression set:  
  `cd examples && ./quick_tests`
- Slower/fuller regression set:  
  `cd examples && ./slow_tests`

Run a single test case by executing its case script directly (from `examples/`), for example:

- `cd examples/netcdf/CIRC_case6 && ./run_me`
- `cd examples/netcdf/CIRC_case6 && ./run_me_sph`
- `cd examples/netcdf/7460_28 && ./run_me`
- `cd examples/corr_k && ./run_me`

### Lint
- CI runs Fortran lint via Fortitude (`.github/workflows/lint-fortran.yaml`) using rules in `.fortitude.toml`.
- Local lint (if `fortitude` is installed):  
  `fortitude check .`

## High-level architecture

- This is a Fortran-first radiation transfer suite. `build_code` stages sources from many `src/` subpackages into `bin/`, runs dependency generation (`mkdep`), selects host/compiler config (`Mk_cmd*`, `set_prog_env*`), then builds through `make/Makefile`.
- Core source domains are separated under `src/`: shared/general modules (`general`, `modules_gen`, `modules_core`), radiative transfer/drivers (`radiance_core`, `aux`, `illumination`, `interface_core`, `nlte`), correlated-k (`correlated_k`), scattering (`scatter`), and optional coupled components (`cosp_*`, `flexchem`, `odepack`).
- `make/Makefile` builds multiple static libraries (`radlib`, `cklib`, `scatlib`, `cosplib`, `flexchemlib`) and then links many executables from `Mk_target_*` include files.
- Runtime command-line entry points are primarily in `sbin/` scripts (e.g., `Cl_run_cdf`, `Cl_run_cdl`, `Ccorr_k`) that wrap executables in `bin/`. Man pages in `man/man1` are the authoritative option reference for these scripts.
- Example/regression workflows live under `examples/`; `quick_tests` and `slow_tests` orchestrate many scenario scripts and compare outputs against reference data.
- `spectraltools/` is a separate Python tooling layer for spectral-file generation workflows and depends on compiled SOCRATES executables plus environment setup from `set_rad_env`.

## Key conventions in this repository

- Build from repository root via `./build_code`; do not compile directly in `src/`. The project expects staged builds in `bin/` and generated runtime env in `set_rad_env`.
- Prefer invoking drivers via `sbin/` wrappers (`Cl_*`, `C*`) in examples/tests rather than calling Fortran binaries directly; wrappers handle temporary files and expected CLI behavior.
- Many test scripts assume `RAD_DIR`, `RAD_BIN`, `RAD_SCRIPT`, and related env vars are set (via sourcing `set_rad_env`) before execution.
- When adding/changing gases, updates are cross-language and multi-location (Fortran core + Julia + `spectraltools`), and gas entries are appended to existing lists (per `README.md`).
- Avoid “lazy” Fortran array extension patterns when adding gas/species metadata; explicit assignments are required so `generate_wrappers.jl` can parse sources reliably.
- NetCDF-linked tools depend on `nf-config`/netCDF Fortran flags configured through `Mk_cmd`; failures around netCDF paths are usually configuration issues, not source issues.
