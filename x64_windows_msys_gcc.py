
from toolchains import Toolchain


Toolchain(
    'x64-windows-msys-gcc',
    prefix='x86_64-pc-msys-',
    CC='gcc',CXX='g++',LINK='g++',
)
