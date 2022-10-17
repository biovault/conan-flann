## Package Status
###GitHub Actions status

![Branch stable/1.9.1_dual](https://github.com/biovault/conan-flann/actions/workflows/build.yml/badge.svg?branch=stable%2F1.9.1_dual)

Currently the following build matrix is performed

OS | Architecture | Compiler
--- | --- | ---
Windows | x84_64 | msvc 2017
Windows | x84_64 | msvc 2019
Linux | x86_64 | gcc 8
Linux | x86_64 | gcc 9
Macos | x86_64 | clang 10
Macos | x86_64 | clang 12


## General Information

This GIT repository wraps the CMake base build for flann and produces a multiple (Release, Debug, RelWithDebInfo) conan package containing 

## Conan Information

Building with conan. 

- Install conan (at least 1.40)
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
conan create . flann/1.9.1 --profile build_profile -s build_type=Release
```

### What gets built?

Both the C and CPP binding versions are built as are static and shared on all platforms. This means that library files with names flann.*, flann_s.*, flann_cpp.*, flann_cpp_s.*are produces (* is lib, dylib, dll depending on platform)

The build includes **CMake Package Configuration Files**.

### "dual" branch

The branch with the *_dual* suffix in the name create a conan package containing Debug, Release and RelWithDebInfo
binaries.


## CI artifacts

Artifacts produced are uploaded to https://lkeb-artifactory.lumc.nl/artifactory/api/conan/conan-local as flann/<version_number>@lkeb/stable.

The artifact includes **CMake Package Configuration Files**.

The conan packages contain a conan_package.tgz with the binaries for the supported configurations in the following tree structure:

```text
bin
    flann_example.c
include
    flann
        + include files and subdirectories
lib
    cmake
        flann
            flannConfig.cmake
            + supporting files
    Debug
        + shared objects and static libs
    Release
        + shared objects and static libs
    RelWIthDebInfo
        + shared objects and static libs
share
    doc
        flann
            manual.pdf
```

## Issues

If you wish to report an issue or make a request for the package, please do so here:

[conan-flann issues](https://github.com/biovault/conan-flann/issues)

## License Information

The contents of this GIT repository are completely separate from the software being packaged and therefore licensed separately.  The license for all files contained in this GIT repository are defined in the [LICENSE.md](LICENSE.md) file in this repository.  

### License(s) for packaged software:

See https://github.com/flann-lib/flann

*Note :   The most common filenames for OSS licenses are `LICENSE` AND `COPYING` without file extensions.*

### License for recipe:

 See [MIT License](./LICENSE.md)
