# CMake configuration file creation
# Building C and CPP bindings static and shared
install(TARGETS flann flann_s flann_cpp flann_cpp_s
    EXPORT flannTargets
    LIBRARY DESTINATION lib/$<CONFIGURATION>
    ARCHIVE DESTINATION lib/$<CONFIGURATION>
    RUNTIME DESTINATION lib/$<CONFIGURATION>
    INCLUDES DESTINATION include
    NAMELINK_SKIP
)

# generate and install export file
install(
    EXPORT flannTargets
    FILE flannTargets.cmake
    DESTINATION lib/cmake/flann
)

# Config
#   * <prefix>/lib/cmake/flann/flann-targets.cmake
# Include module with fuction 'write_basic_package_version_file'
include(CMakePackageConfigHelpers)

# Configure 'flann-config-version.cmake'
# Note: FLANN_VERSION is used as a VERSION
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/flannConfigVersion.cmake"
    VERSION ${FLANN_VERSION}
    COMPATIBILITY SameMajorVersion
)

# Configure 'flann-config.cmake'
# Use variables:
#   * targets_export_name
#   * PROJECT_NAME
configure_package_config_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/Config.cmake.in
    "${CMAKE_CURRENT_BINARY_DIR}/flannConfig.cmake"
    INSTALL_DESTINATION lib/cmake/flann
)

# Config
#   * <prefix>/lib/cmake/flann/flann-config.cmake
#   * <prefix>/lib/cmake/flann/flann-config-version.cmake
install(
    FILES
        "${CMAKE_CURRENT_BINARY_DIR}/flannConfig.cmake"
        "${CMAKE_CURRENT_BINARY_DIR}/flannConfigVersion.cmake"
    DESTINATION lib/cmake/flann
)

# generate the export targets for the build tree
export(EXPORT flannTargets
       FILE "${CMAKE_CURRENT_BINARY_DIR}/cmake/flannTargets.cmake"
)