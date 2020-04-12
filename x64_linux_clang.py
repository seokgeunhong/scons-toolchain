# x86_64, linux, clang
from .toolchains import Toolchain


Toolchain('x64-linux-clang',
    CC='clang',
    CXX='clang++',
    LINK='clang++',
    CCFLAGS=[
        '--target=x86_64-pc-linux-',
        '-fno-exceptions',
        '-fstandalone-debug',
        '--debug',
    ],
    CXXFLAGS=[
        '-std=c++17',
    ],
    LINKFLAGS=[
        '--target=x86_64-pc-linux-',
        '--debug',
    ],
)

Toolchain('x64-linux-clang-8',
    CC='clang-8',
    CXX='clang++-8',
    LINK='clang++-8',
    CCFLAGS=[
        '--target=x86_64-pc-linux-',
        '-fno-exceptions',
        '-fstandalone-debug',
        '--debug',
    ],
    CXXFLAGS=[
        '-std=c++17',
    ],
    LINKFLAGS=[
        '--target=x86_64-pc-linux-',
        '--debug',
    ],
)
