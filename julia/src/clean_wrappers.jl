# Restore to bare minimum when cloning git repo

using Glob

SOCRATES_DIR = normpath(ENV["RAD_DIR"])
println("Cleaning up old wrappers in $SOCRATES_DIR")

# Clean up
gendir = joinpath(SOCRATES_DIR,"julia","gen")
rm(gendir, force=true, recursive=true)
mkdir(gendir)

# Remove old compiled files
libdir = joinpath(SOCRATES_DIR,"julia","lib")
for ext in ["*.so", "*.mod", "*.o"]
    for f in glob(ext, libdir)
        rm(f, force=true)
    end
end
