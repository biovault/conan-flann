import os

from conans import ConanFile, CMake, tools


class FlannTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = (("hdf5/1.10.6"), 
                ("lz4/1.9.2"))
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package"
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')
        self.copy("flann", dst="flann", folder=True)

    def test(self):
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            tools.download("http://www.cs.ubc.ca/research/flann/uploads/FLANN/datasets/dataset.hdf5", "dataset.hdf5")
            self.run(".%sexample" % os.sep)
