# Autogenerated from src/radiance_core/def_atm.F90
# svn revision 1226


    mutable struct StrAtm
        cptr::Ptr{Cvoid}

        function StrAtm()
            handle = new(ccall((:PS_create_StrAtm, libSOCRATES_C), Ptr{Cvoid}, ()))
            finalizer(delete_StrAtm, handle)
            return handle
        end
    end

    function delete_StrAtm(handle::StrAtm)
        if getfield(handle, :cptr) == Ptr{Cvoid}()
            ccall(:jl_safe_printf, Cvoid, (Cstring, ), "error: delete_StrAtm attempt to delete null pointer")
        else
            ccall((:PS_delete_StrAtm, libSOCRATES_C), Cvoid, (Ptr{Cvoid},), getfield(handle, :cptr))
            setfield!(handle, :cptr, Ptr{Cvoid}())
        end
        return nothing
    end


    # this is used to show values in the REPL and when using IJulia
    function Base.show(io::IO, m::MIME"text/plain", handle::StrAtm)
        println(io, handle)
        dump_properties(io, handle)                
    end


    function Base.propertynames(handle::StrAtm, private::Bool=false)
        names = [
            :n_profile,
            :n_layer,
            :lon,
            :lat,
            :n_direction,
            :n_viewing_level,
            :direction,
            :viewing_level,
            :mass,
            :density,
            :p,
            :p_level,
            :t,
            :t_level,
            :r_layer,
            :r_level,
            :gas_mix_ratio,
        ]

        return names
    end


    function Base.getproperty(handle::StrAtm, field::Symbol)


        cptr = getfield(handle, :cptr)
        cptr != Ptr{Cvoid}() || error("invalid handle (null cptr)")            


        if field == :cptr
            return cptr

        elseif field in (
            :n_profile,
            :n_layer,
            :n_direction,
            :n_viewing_level,
        )
            val = Ref{Cint}()
            field_ok = ccall(
                (:PS_StrAtm_get_integer, libSOCRATES_C),
                Cuchar,
                (Ptr{Cvoid}, Cstring, Ref{Cint}),
                cptr, String(field), val
            )
            Bool(field_ok) || error("StrAtm integer field $field not present - coding error")
            return val[]
        elseif field in (
            :lon,
            :lat,
            :direction,
            :viewing_level,
            :mass,
            :density,
            :p,
            :p_level,
            :t,
            :t_level,
            :r_layer,
            :r_level,
            :gas_mix_ratio,
        )
            loc = Ref{Ptr{Cdouble}}()
            ndim = Ref{Cint}(10)
            dims = zeros(Cint, ndim[])
            lbounds = zeros(Cint, ndim[])
            field_ok = ccall(
                (:PS_StrAtm_get_real_array, libSOCRATES_C),
                Cuchar, 
                (Ptr{Cvoid}, Cstring, Ref{Ptr{Cdouble}}, Ref{Cint}, Ref{Cint}, Ref{Cint}),
                cptr, String(field), loc, dims, ndim, lbounds
            )
            Bool(field_ok) || error("StrAtm Cdouble array field $field not present - coding error")
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


    function Base.setproperty!(handle::StrAtm, field::Symbol, val)
              

        cptr = getfield(handle, :cptr)
        cptr != Ptr{Cvoid}() || error("invalid handle (null cptr)")            

        if field in (
            :n_profile,
            :n_layer,
            :n_direction,
            :n_viewing_level,
        )
                    
            field_ok = ccall(
                (:PS_StrAtm_set_integer, libSOCRATES_C),
                Cuchar,
                (Ptr{Cvoid}, Cstring, Cint),
                cptr, String(field), val
            )
            Bool(field_ok) || error("StrAtm integer field $field not present - coding error")
            return val
        else
            error("type StrAtm has no writeable field $field")    
        end    
           
    end

