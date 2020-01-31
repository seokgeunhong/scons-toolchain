# re2c

from SCons.Script import Builder
from toolchains import Toolchain


Toolchain(
    're2c',
    BUILDERS={
        're2c':Builder(action='re2c $SOURCE -o $TARGET',
                       suffix='.c',
                       src_suffix='.re')
    }
)
