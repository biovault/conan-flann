#!/usr/bin/env bash
REGEX_TESTING='^testing/(.*)_dual$'
REGEX_STABLE='^stable/(.*)_dual$'
REGEX_TAG='^(.*)_dual'
if [ "$#" -ne 1 ] ; then
    echo Error in set_travis_reference - not enough arguments
    echo "Usage: set_travis_reference <package_name>  "
    echo sets the environment variable CONAN_REFERENCE with 
    echo package_name/version@user/channel
    echo Where version is derived from the TRAVIS_BRANCH/TRAVIS_TAG
elif [ ${#TRAVIS_TAG} -gt 0 ] && [ $TRAVIS_TAG =~ $REGEX_TAG ] ; then
    export CONAN_REFERENCE=$1/${BASH_REMATCH[1]}@lkeb/stable
elif [[ $TRAVIS_BRANCH =~ $REGEX_STABLE ]] ; then
    export CONAN_REFERENCE=$1/${BASH_REMATCH[1]}@lkeb/stable
elif [[ $TRAVIS_BRANCH =~ $REGEX_FEATURE ]] ; then
    export CONAN_REFERENCE=$1/${BASH_REMATCH[1]}@lkeb/testing;
else
    echo Error in set_travis_reference
    echo Expected either:
    echo 1:  a TRAVIS_TAG with a version number
    echo 2:  a TRAVIS_BRANCH with "feature/.*" or "master"
fi