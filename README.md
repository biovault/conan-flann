## Package Status
###GitHub Actions status

![Branch stable/1.8.4_dual](https://github.com/biovault/conan-flann/actions/workflows/build.yml/badge.svg?branch=stable%2F1.8.4_dual)

Currently the following build matrix is performed

OS | Architecture | Compiler
--- | --- | ---
Linux | x86_64 | gcc 8
Linux | x86_64 | gcc 9
Macos | x86_64 | clang 10
Macos | x86_64 | clang 12

## Conan Information

Building with conan. 

- Install conan (at least 1.38)
- Create a profile (called build_profile) e.g. for Windows:
```
[settings]
os=Windows
os_build=Windows
arch=x86_64
arch_build=x86_64
compiler=Visual Studio
compiler.version=15
[options]
[conf]
[build_requires]
[env]
```

- from the package route run :
```
conan create . flann/1.8.4 --profile build_profile -s build_type=Release
```

### What gets built?

Both the C and CPP binding versions are built as are static and shared on all platforms. This means that library files with names flann.*, flann_s.*, flann_cpp.*, flann_cpp_s.*are produces (* is lib, dylib, dll depending on platform)

### "dual" branch

The branch with the *_dual* suffix in the name create a conan package containing Debug, Release and RelWithDebInfo
binaries.

## Issues

If you wish to report an issue or make a request for a Bincrafters package, please do so here:

[Bincrafters Community Issues](https://github.com/bincrafters/community/issues)

## General Information

This GIT repository wraps the CMake base build for flann and produces a multiple (Release & Debug) conan package containing 


## License Information

The contents of this GIT repository are completely separate from the software being packaged and therefore licensed separately.  The license for all files contained in this GIT repository are defined in the [LICENSE.md](LICENSE.md) file in this repository.  

### License(s) for packaged software:

See https://github.com/flann-lib/flann

*Note :   The most common filenames for OSS licenses are `LICENSE` AND `COPYING` without file extensions.*

### License for recipe:

 See [MIT License](./LICENSE.md)
