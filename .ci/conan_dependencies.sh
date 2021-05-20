conan profile new action_build --force
conan profile update settings.os=$CONAN_OS action_build
conan profile update settings.os_build=$CONAN_OS action_build
conan profile update settings.arch=x86_64 action_build
conan profile update settings.arch_build=x86_64 action_build
conan profile update settings.compiler=$CONAN_COMPILER action_build
conan profile update settings.compiler.version=$CONAN_COMPILERVERSION action_build
conan profile update settings.compiler.libcxx=libc++ action_build
conan profile show action_build