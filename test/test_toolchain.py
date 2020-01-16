import unittest

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import toolchains


class TestToolchain(unittest.TestCase):

    @staticmethod
    def setUpClass():
        toolchains.Toolchain(
            'gcc',
            prefix='gnu-',
            env={'CC':'g++-7',}
        )
        toolchains.Toolchain(
            'debug',
            env = {'CCFLAGS':'-g'}
        )
        toolchains.Toolchain(
            'warning',
            env = {'CCFLAGS':'-pedantic'}
        )

    single = {
        'id':('gcc',),
        'str':'gcc',
        'prefix':'gnu-',
        'env':{'CC':'gnu-g++-7','CCFLAGS':None},
    }
    double = {
        'id':('gcc','debug'),
        'str':'gcc+debug',
        'prefix':'gnu-',
        'env':{'CC':'gnu-g++-7','CCFLAGS':{'-g'}},
    }
    triple = {
        'id':('gcc','debug','warning'),
        'str':'gcc+debug+warning',
        'prefix':'gnu-',
        'env':{'CC':'gnu-g++-7','CCFLAGS':{'-g','-pedantic'}},
    }

    def assertEnvSet(self, a, b):
        a = set() if a is None else set(a)
        b = set() if b is None else set(b)
        self.assertEqual(a, b)

    def assertToolchain(self, t, d):
        self.assertEqual(t.id, d['id'])
        self.assertEqual(str(t), d['str'])
        self.assertEqual(t.prefix, d['prefix'])
        self.assertEqual(t.env('CC'), d['env']['CC'])
        self.assertEnvSet(t.env('CCFLAGS'), d['env']['CCFLAGS'])

    def test_find_single(self):
        self.assertToolchain(toolchains.find('gcc'), self.single)
        self.assertToolchain(toolchains.find(['gcc']), self.single)
        self.assertToolchain(toolchains.find(toolchain='gcc'), self.single)
        self.assertToolchain(toolchains.find(toolchain=['gcc']), self.single)

    def test_find_double_string(self):
        self.assertToolchain(toolchains.find('gcc+debug'), self.double)
        self.assertToolchain(toolchains.find(['gcc','debug']), self.double)
        self.assertToolchain(toolchains.find(['gcc+debug']), self.double)
        self.assertToolchain(toolchains.find('gcc','debug'), self.double)
        self.assertToolchain(toolchains.find('gcc',['debug']), self.double)
        self.assertToolchain(toolchains.find(toolchain='gcc+debug'), self.double)
        self.assertToolchain(toolchains.find(toolchain=['gcc','debug']), self.double)
        self.assertToolchain(toolchains.find(toolchain=['gcc+debug']), self.double)
        self.assertToolchain(toolchains.find(toolchain=['gcc',['debug']]), self.double)

    def test_find_triple_string(self):
        self.assertToolchain(toolchains.find('gcc+debug+warning'), self.triple)
        self.assertToolchain(toolchains.find(['gcc','debug','warning']), self.triple)
        self.assertToolchain(toolchains.find(['gcc+debug+warning']), self.triple)
        self.assertToolchain(toolchains.find('gcc','debug+warning'), self.triple)
        self.assertToolchain(toolchains.find(['gcc','debug+warning']), self.triple)
        self.assertToolchain(toolchains.find('gcc',['debug+warning']), self.triple)
        self.assertToolchain(toolchains.find(['gcc','debug'],'warning'), self.triple)
        self.assertToolchain(toolchains.find(toolchain='gcc+debug+warning'), self.triple)
        self.assertToolchain(toolchains.find(toolchain=['gcc','debug','warning']), self.triple)
        self.assertToolchain(toolchains.find(toolchain=['gcc+debug+warning']), self.triple)
        self.assertToolchain(toolchains.find(toolchain=['gcc','debug+warning']), self.triple)
        self.assertToolchain(toolchains.find(toolchain=['gcc',['debug+warning']]), self.triple)
        self.assertToolchain(toolchains.find(toolchain=[['gcc','debug'],'warning']), self.triple)

    def test_find_wrong(self):
        with self.assertRaises(toolchains.WrongKeyError):
            toolchains.find('')
        with self.assertRaises(toolchains.WrongKeyError):
            toolchains.find('+')
        with self.assertRaises(toolchains.WrongKeyError):
            toolchains.find('gcc+')
        with self.assertRaises(toolchains.WrongKeyError):
            toolchains.find('+debug')
        with self.assertRaises(toolchains.WrongKeyError):
            toolchains.find()
        with self.assertRaises(toolchains.WrongKeyError):
            toolchains.find('gcc','','debug')
        with self.assertRaises(toolchains.WrongKeyError):
            toolchains.find([])
        with self.assertRaises(toolchains.WrongKeyError):
            toolchains.find(['gcc',''])
        with self.assertRaises(toolchains.WrongKeyError):
            toolchains.find(toolchain='')
        with self.assertRaises(toolchains.WrongKeyError):
            toolchains.find(toolchain='+')
        with self.assertRaises(toolchains.WrongKeyError):
            toolchains.find(toolchain='gcc+')
        with self.assertRaises(toolchains.WrongKeyError):
            toolchains.find(toolchain='+debug')
        with self.assertRaises(toolchains.WrongKeyError):
            toolchains.find(toolchain=[])
        with self.assertRaises(toolchains.WrongKeyError):
            toolchains.find(toolchain=['gcc',''])

    def test_find_fail(self):
        with self.assertRaises(toolchains.NotFoundError):
            toolchains.find('vc')
        with self.assertRaises(toolchains.NotFoundError):
            toolchains.find(['vc'])
        with self.assertRaises(toolchains.NotFoundError):
            toolchains.find('gcc+release')
        with self.assertRaises(toolchains.NotFoundError):
            toolchains.find('gcc','release')
        with self.assertRaises(toolchains.NotFoundError):
            toolchains.find(['gcc','release'])
        with self.assertRaises(toolchains.NotFoundError):
            toolchains.find(toolchain='gcc+release')
        with self.assertRaises(toolchains.NotFoundError):
            toolchains.find(toolchain=['gcc','release'])

    def test_def_dup(self):
        toolchains.find('gcc','debug')
        with self.assertRaises(toolchains.DupKeyError):
            toolchains.Toolchain('gcc')
        with self.assertRaises(toolchains.DupKeyError):
            toolchains.Toolchain('gcc+debug')
        with self.assertRaises(toolchains.DupKeyError):
            toolchains.Toolchain(['gcc','debug'])


if __name__ == '__main__':
    unittest.main()
