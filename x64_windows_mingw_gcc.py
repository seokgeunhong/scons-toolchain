# x86_64, windows/mingw, gcc
from toolchains import Toolchain


Toolchain('x64-windows-mingw-gcc',
    option={'warning':'gcc-warning','debug':'gcc-debug'},
    CC='x86_64-w64-mingw32-gcc',
    CXX='x86_64-w64-mingw32-g++',
    LINK='x86_64-w64-mingw32-g++',
)
