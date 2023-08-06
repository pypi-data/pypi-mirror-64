# Simple declarative package management
## For Debianish Linux

Declarative package management means you make a file containing everything you want installed, and the package manager adds/removes to make the system match that.  It's good if you happen to install lots of random programs and forget to remove them until you forgot whether they were important to have installed or not in the first place!

1. `pip install decapt`
2. `decapt generate`
3. Modify `decapt.luxem`
4. Update your system with `decapt`

## Features

* Manage snap packages
* Manage manual debian packages
  Add an entry like `{ name: mypackage, path: ~/debs/mypackage }` where there's a `build.sh` script in `path` which creates a `mypackage.deb` in `path`.
* [Luxem](https://gitlab.com/rendaw/luxem)

## Friends (not really)

* [Nix](https://nixos.org/nix/) - A strict declarative package (and config) manager, and also the basis of Linux distro [NixOS](https://nixos.org/)
* [Guix](https://guix.gnu.org/) - A strict declarative package (and config) manager, and also the basis of Linux distro GuixSD
* [aconfmgr](https://github.com/CyberShadow/aconfmgr) - A declarative Arch-native package and config manager
* [decpac](https://gitlab.com/rendaw/decpac) - I made something similar for Arch
