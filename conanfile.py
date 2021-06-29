from conans import ConanFile, CMake, tools
import os
import glob
import shutil


class FlannDualConan(ConanFile):
    name = "flann"
    version = "1.8.4"
    license = "MIT"
    author = "B. van Lew b.van_lew@lumc.nl"
    url = "https://dl.bintray.com/bldrvnlw/conan-repo/flann"
    description = """3rd party library for Fast Library for
    Approximate Nearest Neighbors by Marius Muja and David Lowe"""
    topics = ("nearest neighbor", "high dimensions", "approximated")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/mariusmuja/flann.git")
        os.chdir("./flann")
        self.run("git checkout tags/{0}".format(self.version))
        os.chdir("..")
        # Workaround for empty source error with CMake > 3.10
        # see issue https://github.com/mariusmuja/flann/issues/369
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.run("touch flann/src/cpp/empty.cpp")
            tools.replace_in_file(
                "flann/src/cpp/CMakeLists.txt",
                'add_library(flann_cpp SHARED "")',
                'add_library(flann_cpp SHARED empty.cpp)')
            tools.replace_in_file(
                "flann/src/cpp/CMakeLists.txt",
                'add_library(flann SHARED "")',
                'add_library(flann SHARED "empty.cpp")')
        if self.settings.os == "Macos":
            tools.replace_in_file(
                "flann/src/cpp/flann/algorithms/kdtree_index.h",
                "#include <cstring>", '''#include <cstring>
#include <cmath>''')
            tools.replace_in_file(
                "flann/src/cpp/flann/algorithms/kdtree_index.h",
                "abs", "std::fabs")

    def _configure_cmake(self, build_type):
        if self.settings.os == "Macos":
            cmake = CMake(self, generator='Xcode', build_type=build_type)
        else:
            cmake = CMake(self, build_type=build_type)
        # <bvl> These don't work out of the box on Windows and are not needed
        # for my environment.
        # If someone can get them working that would be great!
        cmake.definitions["BUILD_PYTHON_BINDINGS"] = "OFF"
        cmake.definitions["BUILD_MATLAB_BINDINGS"] = "OFF"
        cmake.definitions["BUILD_TESTS"] = "OFF"
        cmake.definitions["BUILD_EXAMPLES"] = "OFF"
        # work around failure to produce .lib file for flann_cpp
        if self.settings.os == "Windows" and self.options.shared:
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = True
        cmake.configure(source_folder="flann")
        cmake.verbose = True
        return cmake

    def build(self):
        # Build both release and debug for dual packaging
        cmake_debug = self._configure_cmake('Debug')
        cmake_debug.build()
        # For linux the binary need to be moved to Debug & Release sub folders
        if self.settings.os == "Linux":
            os.mkdir(f"{self.build_folder}/lib/Debug")
            bins = [f for f in glob.glob(f"{self.build_folder}/lib/*")
                    if os.path.isfile(f)]
            for bin in bins:
                shutil.copyfile(bin, f"{self.build_folder}/lib/Debug")

        cmake_release = self._configure_cmake('Release')
        cmake_release.build()
        if self.settings.os == "Linux":
            os.mkdir(f"{self.build_folder}/lib/Release")
            bins = [f for f in glob.glob(f"{self.build_folder}/lib/*")
                    if os.path.isfile(f)]
            for bin in bins:
                shutil.copyfile(bin, f"{self.build_folder}/lib/Release")

    def _pkg_bin(self, build_type):
        src_dir = f"{self.build_folder}/lib/{build_type}"
        dst_lib = f"lib/{build_type}"
        dst_bin = f"bin/{build_type}"
        self.copy("*flann.lib", src=src_dir, dst=dst_lib, keep_path=False)
        self.copy("*.dll", src=src_dir, dst=dst_bin, keep_path=False)
        self.copy("*.so", src=src_dir, dst=dst_lib, keep_path=False)
        self.copy("*.dylib", src=src_dir, dst=dst_lib, keep_path=False)
        self.copy("*.a", src=src_dir, dst=dst_lib, keep_path=False)
        if ((build_type == 'Debug') and
                (self.settings.compiler == "Visual Studio")):
            self.copy("*.pdb", src=src_dir, dst=dst_bin, keep_path=False)

    def package(self):
        self.copy("*.h", src="flann/src/cpp", dst="include", keep_path=True)
        self.copy("*.hpp", src="flann/src/cpp", dst="include", keep_path=True)

        # Debug
        self._pkg_bin('Debug')
        # Release
        self._pkg_bin('Release')
