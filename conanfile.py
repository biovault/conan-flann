from conans import ConanFile, CMake, tools
import os

class FlannConan(ConanFile):
    name = "flann"
    version = "1.9.1"
    license = "MIT"
    author = "B. van Lew b.van_lew@lumc.nl"
    url = "https://dl.bintray.com/bldrvnlw/conan-repo/flann"
    description = "3rd party library for Fast Library for Approximate Nearest Neighbors by Marius Muja and David Lowe"
    topics = ("nearest neighbor", "high dimensions", "approximated")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/mariusmuja/flann.git")
        os.chdir("./flann")
        self.run("git checkout tags/{0}".format(self.version))
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        conanproj = ("project(flann)\n" 
                "include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\n"
                "conan_basic_setup()"
        )     
        os.chdir("..")
        tools.replace_in_file("flann/CMakeLists.txt", "project(flann)", conanproj)

    def build(self):
        # self.run("cmake --build . --target help")
        cmake = CMake(self)
        # <bvl> These don't work out of the box on Windows and are not needed
        # for my environment. If someone can get them working that would be great!
        cmake.definitions["BUILD_PYTHON_BINDINGS"] = "OFF"
        cmake.definitions["BUILD_MATLAB_BINDINGS"] = "OFF" 
        cmake.definitions["BUILD_TESTS"] = "OFF"
        cmake.definitions["BUILD_EXAMPLES"] = "OFF"        
        # work around failure to produce .lib file for flann_cpp        
        if self.settings.os == "Windows" and self.options.shared:
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = True            
        cmake.configure(source_folder="flann")
        cmake.verbose = True
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", src="flann/src/cpp", dst="include", keep_path=True)
        self.copy("*.hpp", src="flann/src/cpp", dst="include", keep_path=True)  
        self.copy("*flann.lib", dst="lib", keep_path=False)
        self.copy("*flann_cpp_s.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)


