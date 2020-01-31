
from SCons.Script import Environment, Builder
from os import environ as osenv


'''Global toolchain registry'''
registry = {}


class WrongKeyError(Exception):
    '''Given key is not valid:

      - Id list is empty. i.e. None, '', or []
      - One or more id are empty. e.g. ['a','','c'], or 'a+b+'
    '''

    def __init__(self, key):
        super(Exception, self).__init__(
            'Wrong toolchain id: `{:s}`'.format('+'.join(key)))

class NotFoundError(Exception):
    '''Faild to find a toolchain with given key'''

    def __init__(self, key):
        super(Exception, self).__init__(
'''Not supported toolchain: `{:s}`

Supported toolchains are:
  {:s}'''.format(
            '+'.join(key),
            '\n  '.join(sorted(str(t) for t in set(registry.values())))))

class DupKeyError(Exception):
    '''Toolchain already exists'''

    def __init__(self, key):
        super(Exception, self).__init__(
'''Duplicated toolchain id: `{:s}`'''.format(
            '+'.join(key)))


def keyfromargs(*toolchains, **args):
    '''Get a new key, i.e. id list, with given arguments

    For argument details, see toolchain().

      return  Id list.
      raise   WrongKeyError If any of id elements are in wrong format.
    '''

    key = []

    try:
        t = args['toolchain']  # toolchain=<key>
    except KeyError:
        pass
    else:
        key += keyfromargs(t)

    for t in toolchains:
        key += t.split('+') if isinstance(t, str) else keyfromargs(*t)

    if not key or [k for k in key if not k]:
        raise WrongKeyError(tuple(key))

    return tuple(key)


def toolchain(*toolchains, **args):
    '''Find a toolchain with given arguments or create one if not exists.

      toolchain=    A single string or an iterable.
      *toolchains   Single strings and/or iterables.

    Each string is a single id or multiple ids separated with `+`:

      toolchain('x64-linux-gcc')  # Key is ('x64-linux-gcc',)
      toolchain('x64-linux-gcc+gcc-debug')  # Key is ('x64-linux-gcc','gcc-debug')

    Each iterable yields another strings or iterables:

      toolchain('x64-linux-gcc','gcc-debug','gcc-warnings')
      toolchain(['x64-linux-gcc','gcc-debug','gcc-warnings'])
      toolchain('x64-linux-gcc',['gcc-debug','gcc-warnings'])
      toolchain(toolchain=['x64-linux-gcc','gcc-debug+gcc-warnings'])
      # All yield the same key: ('x64-linux-gcc','gcc-debug','gcc-warnings')

    Each string is split with '+' into strings, nested iterables are flatten,
    and all iterables are combined into a single tuple, or a _key_.

      return  Toolchain of _key_ if one is found in registry.
              If none found, define one by combining existing toolchains
              of each ids.
      raise   NotFoundError   If any of id is not found in registry.
              WrongKeyError   If any of id is in wrong format.
    '''
    verbose = args.get('verbose', False)

    if verbose:
        print 'toolchain: Finding... {}{}'.format(
            ', '.join(toolchains),
            ', '.join(['='.join(a) for a in args.items()]))

    keys = keyfromargs(*toolchains, **args)
    try:
        t = registry[keys]  # Cached
    except KeyError:
        pass
    else:
        if verbose:
            print 'toolchain: Found `{:s}`\n'.format(t), t.log(2)
        return t

    # Combine
    id = []
    prefix = ''
    env = {}

    for k in keys:
        try:
            t = registry[(k,)]  # Single
        except KeyError:
            raise NotFoundError((k,))

        id += t._id  # Append
        prefix = prefix if prefix else t._prefix  # Replace if None

        # Union
        for k, b in t._env.items():
            a = env.get(k, [])
            if isinstance(b,dict):
                if not a:
                    a = {}
                a.update(b)
            else:
                a = {a} if isinstance(a,str) else set(a)
                b = {b} if isinstance(b,str) else set(b)
                a = list(a|b)

            env[k] = a

    t = Toolchain(id,prefix=prefix,env=env)
    if verbose:
        print 'toolchain: Registered `{:s}`\n'.format(t), t.log(2)

    return t


class Toolchain:
    '''Define a toolchain'''

    def __init__(self, id, prefix='', env={}, **envargs):
        '''
          id        A single string or an iterable. For details, see toolchain().
          prefix    A string.
          env       Dictionary of environment variables.

          raise   WrongKeyError If any of id is in wrong format.
                  DupKeyError   If id exists found.
        '''

        self._id = keyfromargs(toolchain=id)
        self._prefix = prefix
        self._env = env.copy()
        self._env.update(envargs)

        try:
            registry[self._id]
        except KeyError:
            registry[self._id] = self
        else:
            raise DupKeyError(self._id)

    def __str__(self):
        '''String form of id list, combined with '+'.
        
          e.g. 'x64_linux_gcc+gcc_debug'
        '''
        return '+'.join(self._id)

    def log(self, indent=0):
        '''Return log string'''
        return '{i}id={id}\n{i}prefix=\'{prefix}\'\n{i}env={env}'.format(
            i=' '*indent,
            id='+'.join(self._id), prefix=self._prefix, env=self._env)

    @property
    def id(self):
        '''Immutable iterable of ids

        e.g. ('x64_linux_gcc','gcc_debug')
        '''
        return self._id

    # @property
    # def prefix(self):
    #     '''Binary prefix'''
    #     return str(self._prefix)

    def env(self):
        '''Create an Environment with environment values defined.

        Values of variable ['CC', 'CXX', 'LINK'] are prefixed with `.prefix`.
        '''
        return Environment(
            ENV=osenv,
            **{k:self._prefixed(k,v) for k,v in self._env.items()})

    def _prefixed(self, key, val):
        if key in ('CC', 'CXX', 'LINK'):
            v = val if isinstance(val,str) else '-'.join(val) 
            return str(self._prefix) + v if v else ''
        else:
            return val
