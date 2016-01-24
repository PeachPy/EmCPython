# EmCPython
A working Emscripten port of CPython.

# Build

- Install [Emscripten SDK](https://kripken.github.io/emscripten-site/docs/tools_reference/emsdk.html), make sure `emcc`, `emmake`, and setup environment variables.

- Clone EmCPython repository with submodules: `git clone --recursive https://github.com/PeachPy/EmCPython.git`

- Switch to EmCPython directory: `cd EmCPython`.

- Run `./build-python.sh`. It will cross-compile CPython 2.7 and install it into `EmCPython/emscripten`.

- Run `./build-libtar.sh`. It will cross-compile libtar and install it into `EmCPython/emscripten`.

- Run `./pack-modules.py -p emscripten -o pydata.tar`. It will create a TAR with Python modules from `EmCPython/emscripten/lib/python2.7/`.

- Switch to EmCPython/test directory: `cd test`.

- Run [`ninja`](https://ninja-build.org/) to build the test. It will create `python.asm.js` and `python.asm.js.mem` files.

- Execute `python.asm.js` with Node.js: `node python.asm.js`
