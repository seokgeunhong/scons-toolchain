
from toolchains import Toolchain


Toolchain(
    id='x64-windows-msys-gcc',
    tags=['x64-windows','msys-gcc','gcc'],
    prefix='x86_64-pc-msys-',
    CC='gcc',
    CXX='g++',
    LINK='g++',
)
