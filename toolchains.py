
import os
from itertools import product


registry = {}


class ArgMissingError(Exception):
    def __init__(self, **args):
        super(Exception, self).__init__('`%s` is missing.' % ' '.join(args.keys()))

class ArgNotFoundError(Exception):
    def __init__(self, **args):
        super(Exception, self).__init__('''`%s` not supported.

Supported toolchains are:
  %s''' %
            (' '.join('%s=%s' % a for a in args.items()),
             '\n  '.join(sorted(t.id for t in set(registry.values()))))
        )


class Toolchain:

    def __init__(self, id, target_os, compiler,
                 alt_id = [], alt_target_os = [], alt_compiler = [],
                 prefix = '',
                 **env):

        if not id:
            raise TypeError('Toolchain() takes `%s` as mandatory.' % 'id')
        if not target_os:
            raise TypeError('Toolchain() takes `%s` as mandatory.' % 'target_os')
        if not compiler:
            raise TypeError('Toolchain() takes `%s` as mandatory.' % 'compiler')

        self._id = (id,)+tuple(alt_id)
        self._target_os = (target_os,)+tuple(alt_target_os)
        self._compiler = (compiler,)+tuple(alt_compiler)
        self.prefix = prefix
        self._env = env

        # Check duplication
        for k in self._id+tuple(product(self._target_os, self._compiler)):
            if registry.get(k, None):
                raise ValueError('Toolchain() key `%s` duplicated.' % str(k))
            else:
                registry[k] = self


    def __str__(self):
        return self._id[0]

    def log(self):
        return (
            'toolchain=%s' % self._id,
            'target-os=%s' % self._target_os,
            'compiler=%s' % self._compiler,
            'prefix=%s' % self.prefix,
            'env=%s' % self._env,
        )

    @property
    def id(self):
        return self._id[0]

    # @property
    # def target_os(self):
    #     return self._target_os[0]

    # @property
    # def compiler(self):
    #     return self._compiler[0]

    def envargs(self):
        return {
            'ENV': os.environ,
            'CC': self.prefix+self._env.get('CC', ''),
            'CXX': self.prefix+self._env.get('CXX', ''),
            'LINK': self.prefix+self._env.get('LINK', ''),
            'CPPPATH': self._env.get('CPPPATH', ''),
            'CCFLAGS': self._env.get('CCFLAGS', ''),
            'LINKFLAGS': self._env.get('LINKFLAGS', ''),
        }

    @staticmethod
    def from_args(**args):
        id = args.get('toolchain', '')
        if id:
            toolchain = registry.get(id, None)
            if toolchain:
                return toolchain
            else:
                raise ArgNotFoundError(toolchain=id)
        
        target_os = args.get('target-os', '')
        compiler = args.get('compiler', '')
        if target_os and compiler:
            toolchain = registry.get((target_os,compiler), None)
            if toolchain:
                return toolchain
            else:
                raise ArgNotFoundError(target_os=target_os, compiler=compiler)

        if target_os:
            raise ArgMissingError(compiler='')
        elif compiler:
            raise ArgMissingError(target_os='')
        else:
            raise ArgMissingError(toolchain='')
