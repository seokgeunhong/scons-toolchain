# x86_64, linux, gcc
from toolchains import Toolchain


Toolchain('x64-linux-gcc',
    option={'warning':'gcc-warning','debug':'gcc-debug'},
    CC='x86_64-linux-gnu-gcc',
    CXX='x86_64-linux-gnu-g++',
    LINK='x86_64-linux-gnu-g++',
)

Toolchain('x64-linux-gcc-7',
    option={'warning':'gcc-warning','debug':'gcc-debug'},
    CC='x86_64-linux-gnu-gcc-7',
    CXX='x86_64-linux-gnu-g++-7',
    LINK='x86_64-linux-gnu-g++-7',
)

Toolchain('x64-linux-gcc-8',
    option={'warning':'gcc-warning','debug':'gcc-debug'},
    CC='x86_64-linux-gnu-gcc-8',
    CXX='x86_64-linux-gnu-g++-8',
    LINK='x86_64-linux-gnu-g++-8',
)
