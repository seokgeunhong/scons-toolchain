# x86_64, windows/mingw, clang
from toolchains import Toolchain


Toolchain('x64-windows-mingw-clang',
    CC='clang',
    CXX='clang++',
    LINK='clang++',
    CCFLAGS=[
        '--target=x86_64-w64-mingw32',
        '-fno-exceptions',
        '-fstandalone-debug',
        '--debug',
    ],
    CXXFLAGS=[
        '-std=c++17',
    ],
    LINKFLAGS=[
        '--target=x86_64-w64-mingw32',
        '--debug',
    ],
)

Toolchain('x64-windows-mingw-clang-8',
    CC='clang-8',
    CXX='clang++-8',
    LINK='clang++-8',
    CCFLAGS=[
        '--target=x86_64-w64-mingw32',
        '-fno-exceptions',
        '-fstandalone-debug',
        '--debug',
    ],
    CXXFLAGS=[
        '-std=c++17',
    ],
    LINKFLAGS=[
        '--target=x86_64-w64-mingw32',
        '--debug',
    ],
)
