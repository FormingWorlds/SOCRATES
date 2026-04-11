# Interface to the calling model

!!! note
    This overview is adapted from the technical guide by James Manners, John M. Edwards, Peter Hill & Jean-Claude Thelen (Met Office, 2017), which can be found [here](https://github.com/FormingWorlds/SOCRATES/tree/main/docs/techguide). It is under Crown Copyright. 

## Overview

The SOCRATES interface is designed to present a **clear and logical structure** to the input and output fields required by the radiation code. All variables passed to the core routine are wrapped into well-defined Fortran derived types.

---

## Input and output types

All arguments to the core routine `radiance_calc` are contained within **eight derived types**:

| Type | Intent | Description |
|---|---|---|
| `control` | `IN` | Control options, initially read via a namelist |
| `dimen` | `IN` | Array dimension sizes |
| `spectrum` | `IN` | Spectral discretisation and optical properties read from the spectral file |
| `atm` | `IN` | Grid discretisation and atmospheric profiles of thermodynamic quantities and gas amounts |
| `cld` | `IN` | Cloud fields: fractions, mixing ratios, and sub-grid structure |
| `aer` | `IN` | Aerosol fields: mixing ratios for CLASSIC aerosols, optical properties for GLOMAP-MODE aerosols |
| `bound` | `IN` | Boundary conditions at top-of-atmosphere and surface: input fluxes, albedo/emissivity |
| `radout` | `OUT` | All output variables: fluxes and other diagnostics |

The first seven types are `INTENT(IN)` and `radout` is `INTENT(OUT)`. All variables required or produced by the code are contained within these types. Modules are used only to pass parameters, constants, and type definitions.

---

## Call structure

The recommended structure for a calling model (such as the Unified Model) is:

```fortran
CALL read_control   ! Sets up control (elements that are not time-step dependent)
CALL read_spectrum  ! Sets up spectrum by reading from a standard spectral file

! --- Begin loop over time-steps / calls to radiation ---

    CALL set_control  ! Sets control options for this call

    ! --- Begin loop over OpenMP segments ---

        CALL set_dimen   ! Sets dimen for this segment
        CALL set_atm     ! CALL allocate_atm(atm, dimen), set atm
        CALL set_cld     ! CALL allocate_cld(cld, dimen), set cld
        CALL set_aer     ! CALL allocate_aer(aer, dimen), set aer
        CALL set_bound   ! CALL allocate_bound(bound, dimen), set bound

        CALL radiance_calc(control, dimen, spectrum, atm, cld, aer, bound, radout)
        ! --> CALL allocate_out(radout, dimen), calculate radout
        ! --> Assign required variables from radout onto the full model grid

        DEALLOCATE(atm, cld, aer, bound, radout)

    ! <-- End loop over OpenMP segments ---

! <-- End loop over time-steps / calls to radiation ---
```

This structure is repeated separately for the SW and LW radiation calls.

---

## Core routines

The core radiation code provides the following routines and modules:

**`read_spectrum`**
: A standard routine to read in spectral files, which can then be used interchangeably between models.

**Type definition modules** (`def_spectrum`, `def_control`, `def_dimen`, `def_atm`, `def_cld`, `def_aer`, `def_bound`, `def_out`)
: Type definitions including associated `allocate` and `deallocate` routines, and netCDF read/write routines in future.

**`radiance_calc` and called routines**
: The core radiation code itself.

---

## Routines provided by the calling model

The calling model provides routines to set the input variables:

**`set_control`, `set_dimen`, `set_atm`, `set_cld`, `set_aer`, `set_bound`**
: These routines USE the type-definition modules from the core code.