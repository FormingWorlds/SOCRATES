# Installation

## Supported platforms

* Linux x86_64 / AMD64: Ubuntu, Fedora, RedHat, CentOS, Arch, Debian.
* MacOS ARM64 / Apple Silicon

Not supported by old Intel-based Apple systems, or by Linux running on ARM64 architectures.

## Software requirements
* gfortran
* netcdf
* netcdf-fortran
* make
* wget
* curl
* unzip
* cmake

## Standalone install

1. Clone SOCRATES from GitHub: `git clone https://github.com/FormingWorlds/SOCRATES.git`
2. Change to the new folder: `cd SOCRATES`
3. Configure your installation: `./configure`
4. Compile the software: `./build_code`

You must now record the location of SOCRATES' root directory (referred to as `RAD_DIR`) in your terminal/shell's environment.

To do this temporarily, for the current terminal session only, run: `export RAD_DIR=$(pwd)`

To set this permanently with a Bash shell, run: `echo $(pwd) >> ~/.bashrc`

With a Zsh shell, such as on MacOS, run: `echo $(pwd) >> ~/.zshrc`

## Other material

This distribution of SOCRATES is most commonly used and installed within the [PROTEUS framework](https://proteus-framework.org/PROTEUS/), or within the atmosphere models [AGNI](https://www.h-nicholls.space/AGNI/) or [JANUS](https://proteus-framework.org/JANUS). You can find some relevant installation instructions there:

- [Installation within PROTEUS framework](https://proteus-framework.org/PROTEUS/How-to/installation.html#7-install-socrates-radiative-transfer)
- [Installation within AGNI](https://www.h-nicholls.space/AGNI/)
- [Installation within JANUS](https://proteus-framework.org/JANUS/How-to/installation.html)

AGNI provides a script called `get_socrates.sh` for automatically performing this installation process.
