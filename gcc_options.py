# gcc options
from toolchains import Option


# Enable debug option
Option('gcc-debug',
    CCFLAGS='-g',
)

# Turn on warnings
Option(
    'gcc-warning',
    CFLAGS=[
        '-Wjump-misses-init',
        '-Wnested-externs',
        '-Wbad-function-cast',
    ],
    CCFLAGS=[
        '-W','-Wall','-Wextra','-pedantic',
        '-Wconversion','-Wsign-conversion',
        '-Wwrite-strings',
        '-Wpacked',
        '-Wpointer-arith',
        #'-Wfloat-equal',
        '-Wcast-align',
        '-Wdisabled-optimization',
        '-Wformat=2',
        '-Winit-self',
        '-Wlogical-op',
        '-Wmissing-include-dirs',
        '-Wredundant-decls',
        '-Wshadow',
        '-Wstrict-overflow=5',
        # '-Wno-unused',
        # '-Wno-variadic-macros',
        # '-Wno-parentheses',
        '-fdiagnostics-show-option', 
    ],
    CXXFLAGS=[
        '-Wnoexcept',
        '-Wcast-qual',
        '-Wold-style-cast',
        '-Wstrict-null-sentinel',
        '-Woverloaded-virtual',
        '-Wsign-promo',
        #'-Wundef',
        #'-Wctor-dtor-privacy',  # GoogleTest
    ],
)
