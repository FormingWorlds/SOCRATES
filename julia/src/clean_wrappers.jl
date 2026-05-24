# Restore to bare minimum when cloning git repo

SOCRATES_DIR = normpath(ENV["RAD_DIR"])
println("Cleaning up old wrappers in $SOCRATES_DIR")

# Clean up
gendir = joinpath(SOCRATES_DIR,"julia","gen")
rm(gendir, force=true, recursive=true)
mkdir(gendir)

# Remove old compiled files
libdir = joinpath(SOCRATES_DIR,"julia","lib")
if isdir(libdir)
    for f in readdir(libdir; join=true)
        if endswith(f, ".so") || endswith(f, ".mod") || endswith(f, ".o")
            rm(f, force=true)
        end
    end
end
