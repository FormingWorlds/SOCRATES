! Autogenerated from Fortran file src/radiance_core/def_spectrum.F90
! svn revision 1226

module StrSpecDataCont_C

use, intrinsic :: iso_c_binding

use UTILITIES_CF
use def_spectrum

implicit none

private

contains

    function StrSpecDataCont_get_integer(spectrum_Cptr, field_Cstr, val) result(field_OK) &
        bind(C, NAME='PS_StrSpecDataCont_get_integer')

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
    
        if (field == 'index_water') then
            val = spectrum%Cont%index_water
        else
            field_OK = .FALSE.
        end if

    end function StrSpecDataCont_get_integer

    function StrSpecDataCont_set_integer(spectrum_Cptr, field_Cstr, val) result(field_OK) &
        bind(C, NAME='PS_StrSpecDataCont_set_integer')

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
    
        if (field == 'index_water') then
            spectrum%Cont%index_water = val
        else
            field_OK = .FALSE.
        end if

    end function StrSpecDataCont_set_integer

    function StrSpecDataCont_get_integer_array(spectrum_Cptr, field_Cstr, loc, dims_C, ndim, lbounds_C) result(field_OK) &
        bind(C, NAME='PS_StrSpecDataCont_get_integer_array')

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
    
        if (field == 'n_band_continuum') then
            if (allocated(spectrum%Cont%n_band_continuum)) then
                loc = C_LOC(spectrum%Cont%n_band_continuum)
                ndim = size(shape(spectrum%Cont%n_band_continuum))
                dims(1:ndim) = shape(spectrum%Cont%n_band_continuum)
                lbounds(1:ndim) = lbound(spectrum%Cont%n_band_continuum)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'index_continuum') then
            if (allocated(spectrum%Cont%index_continuum)) then
                loc = C_LOC(spectrum%Cont%index_continuum)
                ndim = size(shape(spectrum%Cont%index_continuum))
                dims(1:ndim) = shape(spectrum%Cont%index_continuum)
                lbounds(1:ndim) = lbound(spectrum%Cont%index_continuum)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'i_scale_fnc_cont') then
            if (allocated(spectrum%Cont%i_scale_fnc_cont)) then
                loc = C_LOC(spectrum%Cont%i_scale_fnc_cont)
                ndim = size(shape(spectrum%Cont%i_scale_fnc_cont))
                dims(1:ndim) = shape(spectrum%Cont%i_scale_fnc_cont)
                lbounds(1:ndim) = lbound(spectrum%Cont%i_scale_fnc_cont)
            else
                loc = C_NULL_PTR
            end if

        else
            field_OK = .FALSE.
        end if

    end function StrSpecDataCont_get_integer_array

    function StrSpecDataCont_get_real_array(spectrum_Cptr, field_Cstr, loc, dims_C, ndim, lbounds_C) result(field_OK) &
        bind(C, NAME='PS_StrSpecDataCont_get_real_array')

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
    
        if (field == 'k_cont') then
            if (allocated(spectrum%Cont%k_cont)) then
                loc = C_LOC(spectrum%Cont%k_cont)
                ndim = size(shape(spectrum%Cont%k_cont))
                dims(1:ndim) = shape(spectrum%Cont%k_cont)
                lbounds(1:ndim) = lbound(spectrum%Cont%k_cont)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'scale_cont') then
            if (allocated(spectrum%Cont%scale_cont)) then
                loc = C_LOC(spectrum%Cont%scale_cont)
                ndim = size(shape(spectrum%Cont%scale_cont))
                dims(1:ndim) = shape(spectrum%Cont%scale_cont)
                lbounds(1:ndim) = lbound(spectrum%Cont%scale_cont)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'p_ref_cont') then
            if (allocated(spectrum%Cont%p_ref_cont)) then
                loc = C_LOC(spectrum%Cont%p_ref_cont)
                ndim = size(shape(spectrum%Cont%p_ref_cont))
                dims(1:ndim) = shape(spectrum%Cont%p_ref_cont)
                lbounds(1:ndim) = lbound(spectrum%Cont%p_ref_cont)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 't_ref_cont') then
            if (allocated(spectrum%Cont%t_ref_cont)) then
                loc = C_LOC(spectrum%Cont%t_ref_cont)
                ndim = size(shape(spectrum%Cont%t_ref_cont))
                dims(1:ndim) = shape(spectrum%Cont%t_ref_cont)
                lbounds(1:ndim) = lbound(spectrum%Cont%t_ref_cont)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'k_cont_ses') then
            if (allocated(spectrum%Cont%k_cont_ses)) then
                loc = C_LOC(spectrum%Cont%k_cont_ses)
                ndim = size(shape(spectrum%Cont%k_cont_ses))
                dims(1:ndim) = shape(spectrum%Cont%k_cont_ses)
                lbounds(1:ndim) = lbound(spectrum%Cont%k_cont_ses)
            else
                loc = C_NULL_PTR
            end if

        else if (field == 'k_h2oc') then
            if (allocated(spectrum%Cont%k_h2oc)) then
                loc = C_LOC(spectrum%Cont%k_h2oc)
                ndim = size(shape(spectrum%Cont%k_h2oc))
                dims(1:ndim) = shape(spectrum%Cont%k_h2oc)
                lbounds(1:ndim) = lbound(spectrum%Cont%k_h2oc)
            else
                loc = C_NULL_PTR
            end if

        else
            field_OK = .FALSE.
        end if

    end function StrSpecDataCont_get_real_array

end module StrSpecDataCont_C
