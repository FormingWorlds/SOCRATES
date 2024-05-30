! Autogenerated from Fortran file src/radiance_core/def_spectrum.F90
! svn revision 1226

module StrSpecDataAerosol_C

use, intrinsic :: iso_c_binding

use UTILITIES_CF
use def_spectrum

implicit none

private

contains

    function StrSpecDataAerosol_get_integer(spectrum_Cptr, field_Cstr, val) result(field_OK) &
        bind(C, NAME='PS_StrSpecDataAerosol_get_integer')

        implicit none
        type(c_ptr), value, intent(in)          :: spectrum_Cptr
        type(c_ptr), value, intent(in)          :: field_Cstr
        logical(c_bool)                         :: field_OK
        integer(c_int), intent(out) :: val

        ! local variables
        TYPE(StrSpecData), pointer                  :: spectrum
        character(len=:), allocatable           :: field

        ! convert types
        call C_F_POINTER(spectrum_Cptr, spectrum)
        field = c_to_f_string(field_Cstr)

        field_OK = .TRUE.
    
        if (field == 'n_aerosol') then
            val = spectrum%Aerosol%n_aerosol
        else if (field == 'n_aerosol_mr') then
            val = spectrum%Aerosol%n_aerosol_mr
        else if (field == 'n_aod_wavel') then
            val = spectrum%Aerosol%n_aod_wavel
        else
            field_OK = .FALSE.
        end if

    end function StrSpecDataAerosol_get_integer

    function StrSpecDataAerosol_set_integer(spectrum_Cptr, field_Cstr, val) result(field_OK) &
        bind(C, NAME='PS_StrSpecDataAerosol_set_integer')

        implicit none
        type(c_ptr), value, intent(in)          :: spectrum_Cptr
        type(c_ptr), value, intent(in)          :: field_Cstr
        logical(c_bool)                         :: field_OK
        integer(c_int), value, intent(in) :: val

        ! local variables
        TYPE(StrSpecData), pointer                  :: spectrum
        character(len=:), allocatable           :: field

        ! convert types
        call C_F_POINTER(spectrum_Cptr, spectrum)
        field = c_to_f_string(field_Cstr)

        field_OK = .TRUE.
    
        if (field == 'n_aerosol') then
            spectrum%Aerosol%n_aerosol = val
        else if (field == 'n_aerosol_mr') then
            spectrum%Aerosol%n_aerosol_mr = val
        else if (field == 'n_aod_wavel') then
            spectrum%Aerosol%n_aod_wavel = val
        else
            field_OK = .FALSE.
        end if

    end function StrSpecDataAerosol_set_integer

    function StrSpecDataAerosol_get_logical_array(spectrum_Cptr, field_Cstr, loc, dims_C, ndim, lbounds_C) result(field_OK) &
        bind(C, NAME='PS_StrSpecDataAerosol_get_logical_array')

        implicit none
        type(c_ptr), value, intent(in)          :: spectrum_Cptr
        type(c_ptr), value, intent(in)          :: field_Cstr
        logical(c_bool)                         :: field_OK
        type(c_ptr), intent(out)                :: loc
        type(c_ptr), value, intent(in)          :: dims_C
        integer(c_int), intent(inout)           :: ndim
        type(c_ptr), value, intent(in)          :: lbounds_C

        ! local variables
        TYPE(StrSpecData), pointer             :: spectrum
        character(len=:), allocatable           :: field
        integer(c_int), pointer, dimension(:)   :: dims, lbounds    

        ! convert types
        call C_F_POINTER(spectrum_Cptr, spectrum)
        field = c_to_f_string(field_Cstr)
        call C_F_POINTER(dims_C, dims, [ndim])
        call C_F_POINTER(lbounds_C, lbounds, [ndim])

        field_OK = .TRUE.
    
        if (field == 'l_aero_spec') then
            if (allocated(spectrum%Aerosol%l_aero_spec)) then
                loc = C_LOC(spectrum%Aerosol%l_aero_spec)
                ndim = size(shape(spectrum%Aerosol%l_aero_spec))
                dims(1:ndim) = shape(spectrum%Aerosol%l_aero_spec)
                lbounds(1:ndim) = lbound(spectrum%Aerosol%l_aero_spec)
            else
                loc = C_NULL_PTR
            end if

        else
            field_OK = .FALSE.
        end if

    end function StrSpecDataAerosol_get_logical_array

    function StrSpecDataAerosol_get_integer_array(spectrum_Cptr, field_Cstr, loc, dims_C, ndim, lbounds_C) result(field_OK) &
        bind(C, NAME='PS_StrSpecDataAerosol_get_integer_array')

        implicit none
        type(c_ptr), value, intent(in)          :: spectrum_Cptr
        type(c_ptr), value, intent(in)          :: field_Cstr
        logical(c_bool)                         :: field_OK
        type(c_ptr), intent(out)                :: loc
        type(c_ptr), value, intent(in)          :: dims_C
        integer(c_int), intent(inout)           :: ndim
        type(c_ptr), value, intent(in)          :: lbounds_C

        ! local variables
        TYPE(StrSpecData), pointer             :: spectrum
        character(len=:), allocatable           :: field
        integer(c_int), pointer, dimension(:)   :: dims, lbounds    

        ! convert types
        call C_F_POINTER(spectrum_Cptr, spectrum)
        field = c_to_f_string(field_Cstr)
        call C_F_POINTER(dims_C, dims, [ndim])
        call C_F_POINTER(lbounds_C, lbounds, [ndim])

        field_OK = .TRUE.
    
        if (field == 'type_aerosol') then
            if (allocated(spectrum%Aerosol%type_aerosol)) then
                loc = C_LOC(spectrum%Aerosol%type_aerosol)
                ndim = size(shape(spectrum%Aerosol%type_aerosol))
                dims(1:ndim) = shape(spectrum%Aerosol%type_aerosol)
                lbounds(1:ndim) = lbound(spectrum%Aerosol%type_aerosol)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'i_aerosol_parm') then
            if (allocated(spectrum%Aerosol%i_aerosol_parm)) then
                loc = C_LOC(spectrum%Aerosol%i_aerosol_parm)
                ndim = size(shape(spectrum%Aerosol%i_aerosol_parm))
                dims(1:ndim) = shape(spectrum%Aerosol%i_aerosol_parm)
                lbounds(1:ndim) = lbound(spectrum%Aerosol%i_aerosol_parm)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'n_aerosol_phf_term') then
            if (allocated(spectrum%Aerosol%n_aerosol_phf_term)) then
                loc = C_LOC(spectrum%Aerosol%n_aerosol_phf_term)
                ndim = size(shape(spectrum%Aerosol%n_aerosol_phf_term))
                dims(1:ndim) = shape(spectrum%Aerosol%n_aerosol_phf_term)
                lbounds(1:ndim) = lbound(spectrum%Aerosol%n_aerosol_phf_term)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'nhumidity') then
            if (allocated(spectrum%Aerosol%nhumidity)) then
                loc = C_LOC(spectrum%Aerosol%nhumidity)
                ndim = size(shape(spectrum%Aerosol%nhumidity))
                dims(1:ndim) = shape(spectrum%Aerosol%nhumidity)
                lbounds(1:ndim) = lbound(spectrum%Aerosol%nhumidity)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'i_aod_type') then
            if (allocated(spectrum%Aerosol%i_aod_type)) then
                loc = C_LOC(spectrum%Aerosol%i_aod_type)
                ndim = size(shape(spectrum%Aerosol%i_aod_type))
                dims(1:ndim) = shape(spectrum%Aerosol%i_aod_type)
                lbounds(1:ndim) = lbound(spectrum%Aerosol%i_aod_type)
            else
                loc = C_NULL_PTR
            end if

        else
            field_OK = .FALSE.
        end if

    end function StrSpecDataAerosol_get_integer_array

    function StrSpecDataAerosol_get_real_array(spectrum_Cptr, field_Cstr, loc, dims_C, ndim, lbounds_C) result(field_OK) &
        bind(C, NAME='PS_StrSpecDataAerosol_get_real_array')

        implicit none
        type(c_ptr), value, intent(in)          :: spectrum_Cptr
        type(c_ptr), value, intent(in)          :: field_Cstr
        logical(c_bool)                         :: field_OK
        type(c_ptr), intent(out)                :: loc
        type(c_ptr), value, intent(in)          :: dims_C
        integer(c_int), intent(inout)           :: ndim
        type(c_ptr), value, intent(in)          :: lbounds_C

        ! local variables
        TYPE(StrSpecData), pointer             :: spectrum
        character(len=:), allocatable           :: field
        integer(c_int), pointer, dimension(:)   :: dims, lbounds    

        ! convert types
        call C_F_POINTER(spectrum_Cptr, spectrum)
        field = c_to_f_string(field_Cstr)
        call C_F_POINTER(dims_C, dims, [ndim])
        call C_F_POINTER(lbounds_C, lbounds, [ndim])

        field_OK = .TRUE.
    
        if (field == 'abs') then
            if (allocated(spectrum%Aerosol%abs)) then
                loc = C_LOC(spectrum%Aerosol%abs)
                ndim = size(shape(spectrum%Aerosol%abs))
                dims(1:ndim) = shape(spectrum%Aerosol%abs)
                lbounds(1:ndim) = lbound(spectrum%Aerosol%abs)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'scat') then
            if (allocated(spectrum%Aerosol%scat)) then
                loc = C_LOC(spectrum%Aerosol%scat)
                ndim = size(shape(spectrum%Aerosol%scat))
                dims(1:ndim) = shape(spectrum%Aerosol%scat)
                lbounds(1:ndim) = lbound(spectrum%Aerosol%scat)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'phf_fnc') then
            if (allocated(spectrum%Aerosol%phf_fnc)) then
                loc = C_LOC(spectrum%Aerosol%phf_fnc)
                ndim = size(shape(spectrum%Aerosol%phf_fnc))
                dims(1:ndim) = shape(spectrum%Aerosol%phf_fnc)
                lbounds(1:ndim) = lbound(spectrum%Aerosol%phf_fnc)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'humidities') then
            if (allocated(spectrum%Aerosol%humidities)) then
                loc = C_LOC(spectrum%Aerosol%humidities)
                ndim = size(shape(spectrum%Aerosol%humidities))
                dims(1:ndim) = shape(spectrum%Aerosol%humidities)
                lbounds(1:ndim) = lbound(spectrum%Aerosol%humidities)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'aod_wavel') then
            if (allocated(spectrum%Aerosol%aod_wavel)) then
                loc = C_LOC(spectrum%Aerosol%aod_wavel)
                ndim = size(shape(spectrum%Aerosol%aod_wavel))
                dims(1:ndim) = shape(spectrum%Aerosol%aod_wavel)
                lbounds(1:ndim) = lbound(spectrum%Aerosol%aod_wavel)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'aod_abs') then
            if (allocated(spectrum%Aerosol%aod_abs)) then
                loc = C_LOC(spectrum%Aerosol%aod_abs)
                ndim = size(shape(spectrum%Aerosol%aod_abs))
                dims(1:ndim) = shape(spectrum%Aerosol%aod_abs)
                lbounds(1:ndim) = lbound(spectrum%Aerosol%aod_abs)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'aod_scat') then
            if (allocated(spectrum%Aerosol%aod_scat)) then
                loc = C_LOC(spectrum%Aerosol%aod_scat)
                ndim = size(shape(spectrum%Aerosol%aod_scat))
                dims(1:ndim) = shape(spectrum%Aerosol%aod_scat)
                lbounds(1:ndim) = lbound(spectrum%Aerosol%aod_scat)
            else
                loc = C_NULL_PTR
            end if

        else
            field_OK = .FALSE.
        end if

    end function StrSpecDataAerosol_get_real_array

end module StrSpecDataAerosol_C
