
from toolchains import Toolchain

# gcc-mingw-w64-x86-64
# g++-mingw-w64-x86-64
#
Toolchain(
    id='x64-windows-mingw-gcc',
    tags=['x64-windows','mingw','gcc'],
    prefix='x86_64-w64-mingw32-',
    env={
        'CC':'gcc',
        'CXX':'g++',
        'LINK':'g++',
    },
)
