! Autogenerated from Fortran file src/radiance_core/def_spectrum.F90
! svn revision 1226

module StrSpecDataIce_C

use, intrinsic :: iso_c_binding

use UTILITIES_CF
use def_spectrum

implicit none

private

contains

    function StrSpecDataIce_get_logical_array(spectrum_Cptr, field_Cstr, loc, dims_C, ndim, lbounds_C) result(field_OK) &
        bind(C, NAME='PS_StrSpecDataIce_get_logical_array')

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
    
        if (field == 'l_ice_type') then
            if (allocated(spectrum%Ice%l_ice_type)) then
                loc = C_LOC(spectrum%Ice%l_ice_type)
                ndim = size(shape(spectrum%Ice%l_ice_type))
                dims(1:ndim) = shape(spectrum%Ice%l_ice_type)
                lbounds(1:ndim) = lbound(spectrum%Ice%l_ice_type)
            else
                loc = C_NULL_PTR
            end if

        else
            field_OK = .FALSE.
        end if

    end function StrSpecDataIce_get_logical_array

    function StrSpecDataIce_get_integer_array(spectrum_Cptr, field_Cstr, loc, dims_C, ndim, lbounds_C) result(field_OK) &
        bind(C, NAME='PS_StrSpecDataIce_get_integer_array')

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
    
        if (field == 'i_ice_parm') then
            if (allocated(spectrum%Ice%i_ice_parm)) then
                loc = C_LOC(spectrum%Ice%i_ice_parm)
                ndim = size(shape(spectrum%Ice%i_ice_parm))
                dims(1:ndim) = shape(spectrum%Ice%i_ice_parm)
                lbounds(1:ndim) = lbound(spectrum%Ice%i_ice_parm)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'n_phf') then
            if (allocated(spectrum%Ice%n_phf)) then
                loc = C_LOC(spectrum%Ice%n_phf)
                ndim = size(shape(spectrum%Ice%n_phf))
                dims(1:ndim) = shape(spectrum%Ice%n_phf)
                lbounds(1:ndim) = lbound(spectrum%Ice%n_phf)
            else
                loc = C_NULL_PTR
            end if

        else
            field_OK = .FALSE.
        end if

    end function StrSpecDataIce_get_integer_array

    function StrSpecDataIce_get_real_array(spectrum_Cptr, field_Cstr, loc, dims_C, ndim, lbounds_C) result(field_OK) &
        bind(C, NAME='PS_StrSpecDataIce_get_real_array')

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
    
        if (field == 'parm_list') then
            if (allocated(spectrum%Ice%parm_list)) then
                loc = C_LOC(spectrum%Ice%parm_list)
                ndim = size(shape(spectrum%Ice%parm_list))
                dims(1:ndim) = shape(spectrum%Ice%parm_list)
                lbounds(1:ndim) = lbound(spectrum%Ice%parm_list)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'parm_min_dim') then
            if (allocated(spectrum%Ice%parm_min_dim)) then
                loc = C_LOC(spectrum%Ice%parm_min_dim)
                ndim = size(shape(spectrum%Ice%parm_min_dim))
                dims(1:ndim) = shape(spectrum%Ice%parm_min_dim)
                lbounds(1:ndim) = lbound(spectrum%Ice%parm_min_dim)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'parm_max_dim') then
            if (allocated(spectrum%Ice%parm_max_dim)) then
                loc = C_LOC(spectrum%Ice%parm_max_dim)
                ndim = size(shape(spectrum%Ice%parm_max_dim))
                dims(1:ndim) = shape(spectrum%Ice%parm_max_dim)
                lbounds(1:ndim) = lbound(spectrum%Ice%parm_max_dim)
            else
                loc = C_NULL_PTR
            end if

        else
            field_OK = .FALSE.
        end if

    end function StrSpecDataIce_get_real_array

end module StrSpecDataIce_C
