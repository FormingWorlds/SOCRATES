# Autogenerated from src/radiance_core/def_spectrum.F90
# svn revision 1226


    mutable struct StrSpecDataSolar{P}
        parent_handle::P
    end


    # this is used to show values in the REPL and when using IJulia
    function Base.show(io::IO, m::MIME"text/plain", handle::StrSpecDataSolar)
        println(io, handle)
        dump_properties(io, handle)                
    end


    function Base.propertynames(handle::StrSpecDataSolar, private::Bool=false)
        names = [
            :solar_flux_band,
            :solar_flux_band_ses,
            :weight_blue,
        ]

        return names
    end


    function Base.getproperty(handle::StrSpecDataSolar, field::Symbol)


        cptr = getfield(getfield(handle, :parent_handle), :cptr)
        cptr != Ptr{Cvoid}() || error("invalid handle (null cptr)")            

        if field in (
            :solar_flux_band,
            :solar_flux_band_ses,
            :weight_blue,
        )
            loc = Ref{Ptr{Cdouble}}()
            ndim = Ref{Cint}(10)
            dims = zeros(Cint, ndim[])
            lbounds = zeros(Cint, ndim[])
            field_ok = ccall(
                (:PS_StrSpecDataSolar_get_real_array, libSOCRATES_C),
                Cuchar, 
                (Ptr{Cvoid}, Cstring, Ref{Ptr{Cdouble}}, Ref{Cint}, Ref{Cint}, Ref{Cint}),
                cptr, String(field), loc, dims, ndim, lbounds
            )
            Bool(field_ok) || error("StrSpecDataSolar Cdouble array field $field not present - coding error")
            if loc[] == C_NULL
                return nothing
            else
                a = unsafe_wrap(Array, loc[], Tuple(dims[1:ndim[]]), own=false)
                oa = OffsetArray(a, (lbounds[1:ndim[]] .- 1)...)
                return oa
            end
        else
            return getfield(handle, field)
        end    
           
    end


    function Base.setproperty!(handle::StrSpecDataSolar, field::Symbol, val)
              

        cptr = getfield(getfield(handle, :parent_handle), :cptr)
        cptr != Ptr{Cvoid}() || error("invalid handle (null cptr)")            

        error("type StrSpecDataSolar has no writeable field $field")            
           
    end

