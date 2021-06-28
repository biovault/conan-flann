if [ $# -eq 0 ] ; then
    project=.
else
    project=$1
fi
pip3 install --upgrade conan
conan user
cd $project && .ci/pemsetup.sh
conan remote add lkeb-artifactory $CONAN_UPLOAD
conan remote list

if [[ $TRAVIS_OS_NAME == osx ]] ; then
    CONAN_OS=Macos
    CONAN_COMPILER=apple-clang
    CONAN_CPP_LIB=libc++
else
    CONAN_OS=Linux
    CONAN_COMPILER=gcc
    CONAN_CPP_LIB=libstdc++
fi

conan profile new action_build --force
conan profile update settings.os=$CONAN_OS action_build
conan profile update settings.os_build=$CONAN_OS action_build
conan profile update settings.arch=x86_64 action_build
conan profile update settings.arch_build=x86_64 action_build
conan profile update settings.compiler=$CONAN_COMPILER action_build
conan profile update settings.compiler.version=$CONAN_COMPILERVERSION action_build
conan profile update settings.compiler.libcxx=$CONAN_CPP_LIB action_build
conan profile show action_build