import os
import h5py
import numpy as np
from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from pathlib import Path


class FlannTestConan(ConanFile):
    name = "FlannTest"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"
    requires = ("hdf5/1.10.6", "lz4/1.9.2")
    exports = "CMakeLists.txt", "example.cpp"

    def generate(self):
        print("Generating toolchain")
        tc = CMakeToolchain(self)
        tc.variables["flann_ROOT"] = Path(
            self.deps_cpp_info["flann"].rootpath
        ).as_posix()
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    # def imports(self):
    #    self.copy("*.dll", dst="bin", src="bin")
    #    self.copy("*.dylib*", dst="bin", src="lib")
    #    self.copy("*.so*", dst="bin", src="lib")
    #    self.copy("flann", dst="flann", folder=True)

    def test(self):
        if not tools.cross_building(self.settings):
            with h5py.File("dataset.hdf5", "w") as f:
                np_d = np.random.randint(0, 128, size=(9000, 128), dtype=np.uint8)
                np_d = np_d.astype(np.float64)
                np_q = np.random.randint(0, 128, size=(1000, 128), dtype=np.uint8)
                np_q = np_q.astype(np.float64)
                f.create_dataset("dataset", data=np_d)
                f.create_dataset("query", data=np_q)
            print("Running example...")
            # tools.download("http://www.cs.ubc.ca/research/flann/uploads/FLANN/datasets/dataset.hdf5", "dataset.hdf5")
            if self.settings.os == "Windows":
                self.run(str(Path(Path.cwd(), "Release", "example.exe")))
            else:
                self.run(str(Path(Path.cwd(), "example")))
