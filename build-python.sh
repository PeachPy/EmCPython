#!/usr/bin/env bash

set -ue

EMSCRIPTEN_USR_DIR=$PWD/emscripten
PYTHON_DIR=$PWD/Python-2.7
BUILD_TRIPPLE=$(${PYTHON_DIR}/config.guess)

pushd "${PYTHON_DIR}"
./configure
make python Parser/pgen
mv python hostpython
mv Parser/pgen Parser/hostpgen
make distclean

CONFIG_SITE=./config.site emconfigure ./configure --without-threads --without-pymalloc --disable-shared --disable-ipv6 --without-gcc --host=asmjs-unknown-emscripten --build=${BUILD_TRIPPLE} --prefix=${EMSCRIPTEN_USR_DIR}
emmake make HOSTPYTHON=./hostpython HOSTPGEN=./Parser/hostpgen CROSS_COMPILE=yes
emmake make install
make distclean
popd

