# x86_64, windows/msys, gcc
from .toolchains import Toolchain


Toolchain('x64-windows-msys-gcc',
    option={'warning':'gcc-warning','debug':'gcc-debug'},
    CC='x86_64-pc-msys-gcc',
    CXX='x86_64-pc-msys-g++',
    LINK='x86_64-pc-msys-g++',
)
