#!/usr/bin/env bash -e

##
##  python setup.py  sdist bdist_wheel
##  python setup.py  register --repository pypi
##  python setup.py  sdist bdist_wheel bdist_egg
##  python setup.py  sdist bdist_wheel upload --repository pypi --sign
##  python setup.py  sdist bdist_wheel upload --repository pypi

##  twine register dist/nimbus_captcha-0.1.1.tar.gz
##  twine register dist/nimbus_captcha-0.1.1-py2-none-any.whl
##  python setup.py  sdist bdist_wheel
##  twine upload dist/nimbus_captcha-0.1.1*
##
##
#"""
#vim ~/.pypirc
#
#[distutils]
#index-servers =
#    pypi
#    test
#
#[pypi]
#repository: https://pypi.python.org/pypi
#username: ****
#password: ****
#
#[test]
#repository: https://testpypi.python.org/pypi
#username: ****
#password: ****
#"""

REPOSITORY="pypi"
#REPOSITORY="https://pypi.python.org/pypi"
#REPOSITORY="https://upload.pypi.org/legacy"

REPOSITORY_URL="https://pypi.python.org/pypi"
USER="william2017"
PASSWORD="87654321abcdeABCDE"

###########################################
#  公共方法
###########################################

CUR_DIR=$(cd $(dirname "$0") && pwd)
CUR_PWD=$(pwd)

function uppercase() {
    # 小写转换成大写
    local VAR="$@"
    echo "$(echo ${VAR} | tr '[a-z]' '[A-Z]')" | sed 's/^ //;s/ $//'
    return $?
}

function lowercase() {
    # 大写转换成小写
    local VAR="$@"
    echo "$(echo ${VAR} | tr '[A-Z]' '[a-z]') " | sed 's/^ //;s/ $//'
    return $?
}

function trim() {
    local str=$(echo ${1} | sed "s/'//g")
    local re=$?
    echo ${str}
    return ${re}
}

function get_os() {
    local _os=$(uname -s)
    local _re=$?
    echo "${_os}"
    return ${_re}
}

function get_distributor_id() {
    local _id=""
    local _re=$?
    _cmd=$(which lsb_release)
    if [ -n "${_cmd}" ] ; then
        _id=$(lsb_release -si)
        _re=$?
    fi
    if [ -z "${_id}" ] ; then
        _id=$(awk '/DISTRIB_ID=/' /etc/*-release | sed 's/DISTRIB_ID=//')
        _re=$?
    fi
    echo "${_id}"
    return ${_re}
}

function get_version() {
    local _version=""
    local _re=$?
    _cmd=$(which lsb_release)
    if [ -n "${_cmd}" ] ; then
        _version=$(lsb_release -si)
        _re=$?
    fi
    if [ -z "${_version}" ] ; then
        _version=$(awk '/DISTRIB_RELEASE=/' /etc/*-release | sed 's/DISTRIB_RELEASE=//' | sed 's/[.]/./')
        _re=$?
    fi
    echo "${_version}"
    return ${_re}
}


function do_auto() {
    echo "auto"
    echo "$@"
    twine upload --username ${USER} --password ${PASSWORD} --repository-url ${REPOSITORY_URL} $@
}

function do_clean() {
    echo "clean"
    python setup.py clean
    rm  -rf build dist *.egg-info
}

function do_build() {
    echo "build"
    python setup.py bdist_wheel --universal
}

function do_install() {
    echo "install"
    echo "$@"
    pip install -U $@
}

function do_dist() {
    echo "dist"
    OS=$(get_os)
    python setup.py sdist bdist bdist_wheel bdist_egg
    case "$OS" in
    Linux*)
        ID=$(get_distributor_id)
        VERSION=$(get_version)
        echo "OS: ${OS}|ID: ${ID}|VERSION: ${VERSION}"
        case "${ID}" in
        Ubuntu*)
            python setup.py --command-packages=stdeb.command sdist_dsc bdist_deb
            ;;
        Redhat*)
            python setup.py bdist_rpm
            ;;
        esac
        ;;
    Darwin*)
        echo "OS: ${OS}"
        python setup.py bdist_mpkg
        ;;
    Window*)
        echo "OS: ${OS}"
        python setup.py bdist_wininst
        ;;
    esac
}

function do_upload() {
    echo "upload"
    #python setup.py sdist bdist_wheel upload --repository ${REPOSITORY}
    python setup.py bdist_wheel upload --repository ${REPOSITORY}
}


function do_help() {
    echo "Usage: $0 auto|clean|build|dist|upload " >&2
    exit 0
}

function main() {
    ACTION=$1
    case ${ACTION} in
    auto)
        shift 1
        do_auto $@
        ;;
    clean)
        do_clean
        ;;
    build)
        do_clean
        do_build
        ;;
    dist)
        do_clean
        do_dist
        ;;
    install)
        shift 1
        do_install $@
        ;;
    upload)
        do_upload
        ;;
    *)
        do_help
        ;;
    esac
}

main $@