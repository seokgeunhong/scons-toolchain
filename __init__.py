
name = 'scons-toolchain'

version = {
    'major' : 0,
    'minor' : 1,
    'patch' : 0,
    'state' : 'a',
    'rev' : 5,
}

package = {
    'name' : 'scons-toolchain',
    'type' : 'site_scons',
    'version' : version,
}

__version__ = '{major}.{minor}.{patch}{state}{rev}'.format(**version)

package_str = '{name}-{ver}'.format(ver=__version__,**package)
