# Installation

!!! tip "Installation within the PROTEUS framework"
    If used within PROTEUS, SOCRATES is installed alongside other modules following the
    [PROTEUS installation guide](https://proteus-framework.org/PROTEUS/How-to/installation.html).
    It can also be installed within the atmosphere models
    [AGNI](https://www.h-nicholls.space/AGNI/dev/howto/getting_started/) or
    [JANUS](https://proteus-framework.org/JANUS), as outlined in [Installing via other frameworks](#installing-via-other-frameworks). Use the instructions below if you
    would like a **standalone version of SOCRATES on your system**.

## Supported platforms

- **Linux (x86_64 / AMD64):** Ubuntu, Fedora, RedHat, CentOS, Arch, Debian
- **macOS (ARM64 / Apple Silicon)**

Older Intel-based Mac systems and Linux running on ARM64 architectures are not currently
supported.

!!! info "Software requirements"
    The following tools must be available on your system before installing SOCRATES:

    - gfortran
    - netCDF
    - netCDF-Fortran
    - make
    - cmake
    - wget
    - curl
    - unzip

## Standalone install

1. Clone SOCRATES from GitHub:
   ```bash
   git clone https://github.com/FormingWorlds/SOCRATES.git
   ```
2. Change into the new directory:
   ```bash
   cd SOCRATES
   ```
3. Configure the installation:
   ```bash
   ./configure
   ```
4. Compile the code:
   ```bash
   ./build_code
   ```

### Setting `RAD_DIR`

SOCRATES needs the location of its root directory, referred to as `RAD_DIR`, available as
an environment variable. Run the following commands from inside the SOCRATES directory.

To set this temporarily, for the current terminal session only:

```bash
export RAD_DIR=$(pwd)
```

To set this permanently:

=== "Bash"
    ```bash
    echo "export RAD_DIR=$(pwd)" >> ~/.bashrc
    source ~/.bashrc
    ```

=== "Zsh"
    ```zsh
    echo "export RAD_DIR=$(pwd)" >> ~/.zshrc
    source ~/.zshrc
    ```

### Setting `FWL_DATA` (optional)

`FWL_DATA` is the directory where PROTEUS shared data files, including spectral files, are
stored. Choose a location with sufficient disk space.

To set this temporarily:

```bash
export FWL_DATA=/path/to/fwl_data
```

To set this permanently:

=== "Bash"
    ```bash
    echo 'export FWL_DATA=/path/to/fwl_data' >> ~/.bashrc
    source ~/.bashrc
    ```

=== "Zsh"
    ```zsh
    echo 'export FWL_DATA=/path/to/fwl_data' >> ~/.zshrc
    source ~/.zshrc
    ```

Spectral files will be downloaded into `$FWL_DATA/spectral_files/`.

### Set up a Python environment (optional)

An easy way to work with SOCRATES is by accessing it via Python, which requires a Python
installation with additional dependencies. If you have Conda installed, create a clean
environment and install the required dependencies:

```bash
conda create -n socrates python=3.12 -y
conda activate socrates
pip install -r python/requirements.txt
```

## Installing via other frameworks

This SOCRATES fork is most commonly used as a component of a larger framework rather than
installed standalone. Installation instructions for these are available in their respective
documentation:

- [PROTEUS framework](https://proteus-framework.org/PROTEUS/): see [installing SOCRATES within PROTEUS](https://proteus-framework.org/PROTEUS/How-to/manual_installation.html#5-install-socrates-radiative-transfer)
- [AGNI](https://www.h-nicholls.space/AGNI/) atmosphere model, which provides a `get_socrates.sh` script to automate this installation process
- [JANUS](https://proteus-framework.org/JANUS) atmosphere model: see [installing SOCRATES within JANUS](https://proteus-framework.org/JANUS/How-to/installation.html)