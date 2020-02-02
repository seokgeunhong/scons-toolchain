
from SCons.Script import Environment, Builder
from os import environ as osenv


'''Global toolchain registry'''
registry = {}


class WrongKeyError(Exception):
    '''Given key is not valid'''

    def __init__(self, key):
        self.key = key
        super(Exception, self).__init__('Wrong key: {}'.format(key))

class NotFoundError(Exception):
    '''Faild to find a Toolchain or an Option with given key'''

    def __init__(self, key):
        super(Exception, self).__init__(
'''Not supported toolchain: {}

Supported toolchains are:
  {}'''.format(
            key,
            '\n  '.join(sorted(str(t) for t in registry.values()))))

class DupKeyError(Exception):
    '''Toolchain already exists'''

    def __init__(self, key):
        super(Exception, self).__init__(
            'Duplicated toolchain key: `{}`'.format(key))


def toolchain(*keys, **args):
    '''Find a toolchain with given arguments or register one if not exists.

      toolchain=<keys>  Strings or nested iterables of strings, which is
      *<keys>           a toolchain key followed optional option names.
                        Either toolchain=<keys> or *<keys> may be used.

      verbose=<bool>    If True, print progress information.

    Each string is a key or keys separated with `+`:

      toolchain('gcc')        # Toolchain `gcc`
      toolchain('gcc+debug')  # Toolchain `gcc` with Option `debug`

    Each iterable yields another strings or iterables:

      # All yield: Toolchain `gcc` with Option `debug` and `warning`
      toolchain('gcc','debug','warning')
      toolchain(['gcc','debug','warning'])
      toolchain('gcc',['debug','warning'])
      toolchain(toolchain=['gcc','debug+warning'])

      return  Toolchain found, or define one if none found.
      raise   NotFoundError   If any element is not found in the registry.
              WrongKeyError   If arguments are wrong.
    '''
    verbose = args.pop('verbose', False)

    if verbose:
        print 'toolchain: Finding ({}{})'.format(
            ','.join((str(t) for t in keys)),
            ','.join(['='.join(a) for a in args.items()]))

    toolchain_arg = args.pop('toolchain',None)
    key = keytuple(toolchain_arg if toolchain_arg else keys)
    if verbose:
        print 'toolchain: key={}'.format(key)

    toolchain = registry.get(key,None)
    if toolchain:  # Found cached
        if verbose:
            print 'toolchain: Found `{}`'.format(toolchain.key)
        return toolchain

    try:
        toolchain = registry[key[:1]]
    except KeyError as e:
        raise NotFoundError(e.args[0])

    toolchain = Toolchain(key,
        env=Toolchain.merge(toolchain.env, *(toolchain.Option(n).env for n in key[1:])))
    if verbose:
        print 'toolchain: Registered {}'.format(key)
        print 'toolchain: env={}'.format(toolchain.env)
    return toolchain


def keytuple(*keys):
    '''Get a flat and duplication-free key tuple

      keys    Strings or (possibly nested) iterables of strings
      return  A tuple of strings, duplication removed.
      raise   WrongKeyError If any of elements are in wrong format.
    '''
    t = []
    s = set()
    for key in keys:
        key = key.split('+') if isinstance(key,str) else keytuple(*key)
        for k in key:
            if k and not k in s:
                t.append(k)
                s.add(k)

    return tuple(t)


class Env:
    '''Define a set of environment variables'''

    def __init__(self, key, env={}, **envargs):
        '''
          key       A single string or an iterable.
          env       Dictionary of environment variables.
          envargs   Environment vairables in keyword arguments

          raise     WrongKeyError   If key is in wrong format.
                    DupKeyError     If key exists found.
        '''
        self.key = keytuple(key)
        self.env = env.copy()
        self.env.update(envargs)

        try:
            registry[self.key]
        except KeyError:
            registry[self.key] = self
        else:
            raise DupKeyError(self.key)

    def __str__(self):
        return '+'.join(self.key)

    @staticmethod
    def merge(*envs):
        '''Merge environment variable sets and return

        Values of variables are either dicts or iterables.
        '''

        env = {}
        for e in envs:
            for k,b in e.items():
                if isinstance(b,dict):
                    a = env.get(k,{})
                    a.update(b)
                    env[k] = a
                else:
                    a = env.get(k,set())
                    a = {a} if isinstance(a,str) else set(a)
                    b = {b} if isinstance(b,str) else set(b)
                    env[k] = list(a|b)

        return env


class Toolchain(Env):
    '''Define and register a toolchain'''

    def __init__(self, key, option={}, env={}, **envargs):
        '''
          key       A single string or an iterable.
          option    Dictionary of available options, whose keys are names,
                    and values are either Option keys or instances.
          env       Dictionary of environment variables.
          envargs   Environment vairables in keyword arguments.

          raise     WrongKeyError   If key is in wrong format.
                    DupKeyError     If key exists found.
        '''
        Env.__init__(self, key, env, **envargs)
        self.option = option.copy()

    def Join(self, *names, **args):
        '''
        Find options with names and join them to self.
        
          option=<names>    Option names or instances to add. See toolchain().
          *<names>          Either option=<names> or *<names> may be used.

          verbose=<bool>    If True, print progress information.
        '''
        verbose = args.pop('verbose', False)

        option = args.get('option',[])
        return toolchain(self.key, option if option else names, verbose=verbose)

    def Option(self, name):
        try:
            o = self.option[name]
        except KeyError:
            raise Exception('`{}` Not supports [{}]'.format(self,name))

        if isinstance(o,Option):
            return o

        try:
            o = registry[(o,)]
        except KeyError:
            raise NotFoundError(o)

        self.option[name] = o
        return o

    def Environment(self):
        '''Create an Environment with environment values defined.
        '''
        return Environment(ENV=osenv,**self.env)


class Option(Env):
    '''Define and register a toolchain'''
