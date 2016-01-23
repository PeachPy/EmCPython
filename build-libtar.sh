#!/usr/bin/env bash

set -ue

EMSCRIPTEN_USR_DIR=$PWD/emscripten
LIBTAR_DIR=$PWD/libtar
BUILD_TRIPPLE=$(${LIBTAR_DIR}/autoconf/config.guess)

pushd "${LIBTAR_DIR}"
emconfigure ./configure --disable-shared --enable-static --host=asmjs-unknown-emscripten --build=${BUILD_TRIPPLE} --prefix=${EMSCRIPTEN_USR_DIR}
emmake make
emmake make -C lib install
make distclean
rm -f a.out a.out.js
popd

