from conans import ConanFile, tools
from conan.tools.cmake import CMakeDeps, CMake, CMakeToolchain
import os
import shutil
from pathlib import Path


class FlannDualConan(ConanFile):
    name = "flann"
    version = "1.8.5"
    license = "MIT"
    author = "B. van Lew b.van_lew@lumc.nl"
    url = "https://dl.bintray.com/bldrvnlw/conan-repo/flann"
    description = """3rd party library for Fast Library for
    Approximate Nearest Neighbors by Marius Muja and David Lowe"""
    topics = ("nearest neighbor", "high dimensions", "approximated")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": True}
    generators = "CMakeDeps"
    exports = "cmake/*"

    def source(self):
        self.run("git clone https://github.com/mariusmuja/flann.git")
        os.chdir("./flann")
        self.run("git checkout tags/{0}".format(self.version))
        os.chdir("..")

    def generate(self):
        print("In generate")

        generator = None
        if self.settings.os == "Macos":
            generator = "Xcode"

        tc = CMakeToolchain(self, generator=generator)
        tc.variables["BUILD_PYTHON_BINDINGS"] = "OFF"
        tc.variables["BUILD_MATLAB_BINDINGS"] = "OFF"
        tc.variables["BUILD_TESTS"] = "OFF"
        tc.variables["BUILD_EXAMPLES"] = "OFF"
        tc.variables["CMAKE_TOOLCHAIN_FILE"] = "conan_toolchain.cmake"
        tc.variables["CMAKE_INSTALL_PREFIX"] = Path(self.build_folder).joinpath(
            "install"
        )
        if self.settings.os == "Windows" and self.options.shared:
            tc.variables["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = "ON"
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(source_folder="flann")
        cmake.verbose = True
        return cmake

    def _fixup_code(self):
        # Workaround for empty source error with CMake > 3.10
        # see issue https://github.com/mariusmuja/flann/issues/369
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.run("touch flann/src/cpp/empty.cpp")
            tools.replace_in_file(
                "flann/src/cpp/CMakeLists.txt",
                'add_library(flann_cpp SHARED "")',
                "add_library(flann_cpp SHARED empty.cpp)",
            )
            tools.replace_in_file(
                "flann/src/cpp/CMakeLists.txt",
                'add_library(flann SHARED "")',
                'add_library(flann SHARED "empty.cpp")',
            )
        if self.settings.os == "Macos":
            tools.replace_in_file(
                "flann/src/cpp/flann/algorithms/kdtree_index.h",
                "#include <cstring>",
                """#include <cstring>
#include <cmath>""",
            )
            # not used in 1.8.5
            # tools.replace_in_file(
            #    "flann/src/cpp/flann/algorithms/kdtree_index.h", "abs", "std::fabs"
            # )

        # Inject flannTargets.cmake logic
        # Logic for flannTargets.cmake
        # This install logic is missing from flann:
        # 1.8.5, 1.8.5 and 1.9.1 but is in master
        shutil.copyfile(
            "./cmake/Config.cmake.in",
            "flann/cmake/Config.cmake.in",
        )

        shutil.copyfile(
            "./cmake/ConfigInstall.cmake", "flann/cmake/ConfigInstall.cmake"
        )

        tools.replace_in_file(
            "flann/CMakeLists.txt",
            "# CPACK options",
            """
include(./cmake/ConfigInstall.cmake)

# CPACK options""",
        )

        # Version is wrong in flann 1.8.5
        if self.version == "1.8.5":
            tools.replace_in_file(
                "flann/CMakeLists.txt",
                "set(FLANN_VERSION 1.8.4)",
                "set(FLANN_VERSION 1.8.5)",
            )

    def build(self):
        self._fixup_code()
        install_dir = Path(self.build_folder).joinpath("install")
        install_dir.mkdir(exist_ok=True)
        # Build both release and debug for dual packaging
        cmake_debug = self._configure_cmake()
        cmake_debug.install(build_type="Debug")

        cmake_release = self._configure_cmake()
        cmake_release.install(build_type="Release")

    # Package has no build type marking
    def package_id(self):
        del self.info.settings.build_type
        if self.settings.compiler == "Visual Studio":
            del self.info.settings.compiler.runtime

    # Package contains its own cmake config file
    def package_info(self):
        self.cpp_info.set_property("skip_deps_file", True)
        self.cpp_info.set_property("cmake_config_file", True)

    def _pkg_bin(self, build_type):
        src_dir = f"{self.build_folder}/lib/{build_type}"
        dst_lib = f"lib/{build_type}"
        dst_bin = f"bin/{build_type}"
        self.copy("*flann.lib", src=src_dir, dst=dst_lib, keep_path=False)
        self.copy("*.dll", src=src_dir, dst=dst_bin, keep_path=False)
        self.copy("*.so", src=src_dir, dst=dst_lib, keep_path=False)
        self.copy("*.dylib", src=src_dir, dst=dst_lib, keep_path=False)
        self.copy("*.a", src=src_dir, dst=dst_lib, keep_path=False)
        if (build_type == "Debug") and (self.settings.compiler == "Visual Studio"):
            self.copy("*.pdb", src=src_dir, dst=dst_bin, keep_path=False)

    def package(self):
        self.copy("*.h", src="flann/src/cpp", dst="include", keep_path=True)
        self.copy("*.hpp", src="flann/src/cpp", dst="include", keep_path=True)

        # Debug
        self._pkg_bin("Debug")
        # Release
        self._pkg_bin("Release")
