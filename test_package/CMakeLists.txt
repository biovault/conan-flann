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
#hdf5 and lz4 supplied by CMakeDeps
target_link_libraries(example flann HDF5::HDF5 lz4::lz4 OpenMP::OpenMP_CXX)
