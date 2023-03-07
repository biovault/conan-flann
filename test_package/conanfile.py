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
        if self.settings.os == "Macos":
            proc = subprocess.run(
                "brew --prefix libomp", shell=True, capture_output=True
            )
            tc.variables["OpenMP_ROOT"] = Path(
                proc.stdout.decode("UTF-8").strip()
            ).as_posix()
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            # tools.download("http://www.cs.ubc.ca/research/flann/uploads/FLANN/datasets/dataset.hdf5", "dataset.hdf5")
            # Create a test hdf5 file since the downloadable dataset i snot available
            with h5py.File("dataset.hdf5", "w") as f:
                np_d = np.random.randint(0, 128, size=(9000, 128), dtype=np.uint8)
                np_d = np_d.astype(np.float64)
                np_q = np.random.randint(0, 128, size=(1000, 128), dtype=np.uint8)
                np_q = np_q.astype(np.float64)
                f.create_dataset("dataset", data=np_d)
                f.create_dataset("query", data=np_q)
            print("Running example...")

            if self.settings.os == "Windows":
                self.run(str(Path(Path.cwd(), "Release", "example.exe")))
            else:
                self.run(str(Path(Path.cwd(), "example")))
