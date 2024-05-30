# Autogenerated from src/radiance_core/def_spectrum.F90
# svn revision 1226


    mutable struct StrSpecDataIce{P}
        parent_handle::P
    end


    # this is used to show values in the REPL and when using IJulia
    function Base.show(io::IO, m::MIME"text/plain", handle::StrSpecDataIce)
        println(io, handle)
        dump_properties(io, handle)                
    end


    function Base.propertynames(handle::StrSpecDataIce, private::Bool=false)
        names = [
            :l_ice_type,
            :i_ice_parm,
            :n_phf,
            :parm_list,
            :parm_min_dim,
            :parm_max_dim,
        ]

        return names
    end


    function Base.getproperty(handle::StrSpecDataIce, field::Symbol)


        cptr = getfield(getfield(handle, :parent_handle), :cptr)
        cptr != Ptr{Cvoid}() || error("invalid handle (null cptr)")            

        if field in (
            :l_ice_type,
        )
            loc = Ref{Ptr{Cint}}()
            ndim = Ref{Cint}(10)
            dims = zeros(Cint, ndim[])
            lbounds = zeros(Cint, ndim[])
            field_ok = ccall(
                (:PS_StrSpecDataIce_get_logical_array, libSOCRATES_C),
                Cuchar, 
                (Ptr{Cvoid}, Cstring, Ref{Ptr{Cint}}, Ref{Cint}, Ref{Cint}, Ref{Cint}),
                cptr, String(field), loc, dims, ndim, lbounds
            )
            Bool(field_ok) || error("StrSpecDataIce Cint array field $field not present - coding error")
            if loc[] == C_NULL
                return nothing
            else
                a = unsafe_wrap(Array, loc[], Tuple(dims[1:ndim[]]), own=false)
                oa = OffsetArray(a, (lbounds[1:ndim[]] .- 1)...)
                return oa
            end
        elseif field in (
            :i_ice_parm,
            :n_phf,
        )
            loc = Ref{Ptr{Cint}}()
            ndim = Ref{Cint}(10)
            dims = zeros(Cint, ndim[])
            lbounds = zeros(Cint, ndim[])
            field_ok = ccall(
                (:PS_StrSpecDataIce_get_integer_array, libSOCRATES_C),
                Cuchar, 
                (Ptr{Cvoid}, Cstring, Ref{Ptr{Cint}}, Ref{Cint}, Ref{Cint}, Ref{Cint}),
                cptr, String(field), loc, dims, ndim, lbounds
            )
            Bool(field_ok) || error("StrSpecDataIce Cint array field $field not present - coding error")
            if loc[] == C_NULL
                return nothing
            else
                a = unsafe_wrap(Array, loc[], Tuple(dims[1:ndim[]]), own=false)
                oa = OffsetArray(a, (lbounds[1:ndim[]] .- 1)...)
                return oa
            end
        elseif field in (
            :parm_list,
            :parm_min_dim,
            :parm_max_dim,
        )
            loc = Ref{Ptr{Cdouble}}()
            ndim = Ref{Cint}(10)
            dims = zeros(Cint, ndim[])
            lbounds = zeros(Cint, ndim[])
            field_ok = ccall(
                (:PS_StrSpecDataIce_get_real_array, libSOCRATES_C),
                Cuchar, 
                (Ptr{Cvoid}, Cstring, Ref{Ptr{Cdouble}}, Ref{Cint}, Ref{Cint}, Ref{Cint}),
                cptr, String(field), loc, dims, ndim, lbounds
            )
            Bool(field_ok) || error("StrSpecDataIce Cdouble array field $field not present - coding error")
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


    function Base.setproperty!(handle::StrSpecDataIce, field::Symbol, val)
              

        cptr = getfield(getfield(handle, :parent_handle), :cptr)
        cptr != Ptr{Cvoid}() || error("invalid handle (null cptr)")            

        error("type StrSpecDataIce has no writeable field $field")            
           
    end

