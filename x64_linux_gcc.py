
from toolchains import Toolchain


Toolchain(
    'x64-linux-gcc',
    prefix='x86_64-linux-gnu-',
    env={
        'CC':'gcc',
        'CXX':'g++',
        'LINK':'g++',
    }
)
