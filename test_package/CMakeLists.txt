cmake_minimum_required(VERSION 3.12)
project(PackageTest CXX)

find_package(flann CONFIG REQUIRED)
find_package(HDF5 REQUIRED)
find_package(lz4 REQUIRED)

find_package(OpenMP)
if (APPLE)
    find_package(OpenMP)
    find_package(OpenGL REQUIRED)
else()
    find_package(OpenMP REQUIRED)
endif()

add_executable(example example.cpp)
# Enable running  from the build directory on MACOS by fixing flann rpath
if (APPLE)
    add_custom_command(TARGET example
       POST_BUILD COMMAND "${CMAKE_INSTALL_NAME_TOOL}"
        "-change" "libflann.1.9.dylib" "${flann_ROOT}/lib/Release/libflann.1.9.dylib"
        "${CMAKE_BINARY_DIR}/example")
endif()

#hdf5 and lz4 supplied by CMakeDeps
target_link_libraries(example flann::flann hdf5::hdf5_cpp lz4::lz4 OpenMP::OpenMP_CXX)
