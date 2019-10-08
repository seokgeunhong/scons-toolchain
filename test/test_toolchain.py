import unittest

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import toolchains


class TestToolchain(unittest.TestCase):

    @staticmethod
    def init_class(module):
        toolchains = module

    @staticmethod
    def setUpClass():
        toolchains.Toolchain(
            'x64-linux-gcc-7',
            tags=['x64-linux','gcc-7','gcc'],
            prefix='x86_64-linux-gnu-',
            env={'CC':'gcc-7',}
        )
        toolchains.Toolchain(
            'gcc-debug',
            tags=['gcc','debug'],
            env = {'CCFLAGS':'-g'}
        )
        toolchains.Toolchain(
            'gcc-warning-max',
            tags=['gcc','warning-max'],
            env = {'CCFLAGS':'-pedantic'}
        )

    def test_find_single_1(self):
        toolchain = toolchains.find('x64-linux-gcc-7')
        self.assertTrue(toolchain)
        self.assertEqual(toolchain.id, 'x64-linux-gcc-7')
        self.assertEqual(set(toolchain.tags), {'x64-linux','gcc-7','gcc'})
        self.assertEqual(toolchain.prefix, 'x86_64-linux-gnu-')
        self.assertEqual(toolchain.env('CC'), 'x86_64-linux-gnu-gcc-7')
        self.assertEqual(toolchain.env('CCFLAGS'), None)

    def test_find_single_2(self):
        toolchain = toolchains.find(['x64-linux-gcc-7'])
        self.assertTrue(toolchain)
        self.assertEqual(toolchain.id, 'x64-linux-gcc-7')
        self.assertEqual(set(toolchain.tags), {'x64-linux','gcc-7','gcc'})
        self.assertEqual(toolchain.prefix, 'x86_64-linux-gnu-')
        self.assertEqual(toolchain.env('CC'), 'x86_64-linux-gnu-gcc-7')
        self.assertEqual(toolchain.env('CCFLAGS'), None)

    def test_find_single_3(self):
        toolchain = toolchains.find(toolchain='x64-linux-gcc-7')
        self.assertTrue(toolchain)
        self.assertEqual(toolchain.id, 'x64-linux-gcc-7')
        self.assertEqual(set(toolchain.tags), {'x64-linux','gcc-7','gcc'})
        self.assertEqual(toolchain.prefix, 'x86_64-linux-gnu-')
        self.assertEqual(toolchain.env('CC'), 'x86_64-linux-gnu-gcc-7')
        self.assertEqual(toolchain.env('CCFLAGS'), None)

    def test_find_single_4(self):
        toolchain = toolchains.find(toolchain=['x64-linux-gcc-7'])
        self.assertTrue(toolchain)
        self.assertEqual(toolchain.id, 'x64-linux-gcc-7')
        self.assertEqual(set(toolchain.tags), {'x64-linux','gcc-7','gcc'})
        self.assertEqual(toolchain.prefix, 'x86_64-linux-gnu-')
        self.assertEqual(toolchain.env('CC'), 'x86_64-linux-gnu-gcc-7')
        self.assertEqual(toolchain.env('CCFLAGS'), None)

    def test_find_double_1(self):
        toolchain = toolchains.find('x64-linux-gcc-7+gcc-debug')
        self.assertTrue(toolchain)
        self.assertEqual(toolchain.id, 'x64-linux-gcc-7+gcc-debug')
        self.assertEqual(set(toolchain.tags), {'x64-linux','gcc-7','gcc','debug'})
        self.assertEqual(toolchain.prefix, 'x86_64-linux-gnu-')
        self.assertEqual(toolchain.env('CC'), 'x86_64-linux-gnu-gcc-7')
        self.assertEqual(set(toolchain.env('CCFLAGS')), {'-g'})

    def test_find_double_2(self):
        toolchain = toolchains.find(['x64-linux-gcc-7','gcc-debug'])
        self.assertTrue(toolchain)
        self.assertEqual(toolchain.id, 'x64-linux-gcc-7+gcc-debug')
        self.assertEqual(set(toolchain.tags), {'x64-linux','gcc-7','gcc','debug'})
        self.assertEqual(toolchain.prefix, 'x86_64-linux-gnu-')
        self.assertEqual(toolchain.env('CC'), 'x86_64-linux-gnu-gcc-7')
        self.assertEqual(set(toolchain.env('CCFLAGS')), {'-g'})

    def test_find_double_3(self):
        toolchain = toolchains.find(toolchain='x64-linux-gcc-7+gcc-debug')
        self.assertTrue(toolchain)
        self.assertEqual(toolchain.id, 'x64-linux-gcc-7+gcc-debug')
        self.assertEqual(set(toolchain.tags), {'x64-linux','gcc-7','gcc','debug'})
        self.assertEqual(toolchain.prefix, 'x86_64-linux-gnu-')
        self.assertEqual(toolchain.env('CC'), 'x86_64-linux-gnu-gcc-7')
        self.assertEqual(set(toolchain.env('CCFLAGS')), {'-g'})

    def test_find_double_4(self):
        toolchain = toolchains.find(toolchain=['x64-linux-gcc-7','gcc-debug'])
        self.assertTrue(toolchain)
        self.assertEqual(toolchain.id, 'x64-linux-gcc-7+gcc-debug')
        self.assertEqual(set(toolchain.tags), {'x64-linux','gcc-7','gcc','debug'})
        self.assertEqual(toolchain.prefix, 'x86_64-linux-gnu-')
        self.assertEqual(toolchain.env('CC'), 'x86_64-linux-gnu-gcc-7')
        self.assertEqual(set(toolchain.env('CCFLAGS')), {'-g'})

    def test_find_triple_1(self):
        toolchain = toolchains.find('x64-linux-gcc-7+gcc-debug+gcc-warning-max')
        self.assertTrue(toolchain)
        self.assertEqual(toolchain.id, 'x64-linux-gcc-7+gcc-debug+gcc-warning-max')
        self.assertEqual(set(toolchain.tags), {'x64-linux','gcc-7','gcc','debug','warning-max'})
        self.assertEqual(toolchain.prefix, 'x86_64-linux-gnu-')
        self.assertEqual(toolchain.env('CC'), 'x86_64-linux-gnu-gcc-7')
        self.assertEqual(set(toolchain.env('CCFLAGS')), {'-g','-pedantic'})

    def test_find_triple_2(self):
        toolchain = toolchains.find(['x64-linux-gcc-7','gcc-debug','gcc-warning-max'])
        self.assertTrue(toolchain)
        self.assertEqual(toolchain.id, 'x64-linux-gcc-7+gcc-debug+gcc-warning-max')
        self.assertEqual(set(toolchain.tags), {'x64-linux','gcc-7','gcc','debug','warning-max'})
        self.assertEqual(toolchain.prefix, 'x86_64-linux-gnu-')
        self.assertEqual(toolchain.env('CC'), 'x86_64-linux-gnu-gcc-7')
        self.assertEqual(set(toolchain.env('CCFLAGS')), {'-g','-pedantic'})

    def test_find_triple_3(self):
        toolchain = toolchains.find(toolchain='x64-linux-gcc-7+gcc-debug+gcc-warning-max')
        self.assertTrue(toolchain)
        self.assertEqual(toolchain.id, 'x64-linux-gcc-7+gcc-debug+gcc-warning-max')
        self.assertEqual(set(toolchain.tags), {'x64-linux','gcc-7','gcc','debug','warning-max'})
        self.assertEqual(toolchain.prefix, 'x86_64-linux-gnu-')
        self.assertEqual(toolchain.env('CC'), 'x86_64-linux-gnu-gcc-7')
        self.assertEqual(set(toolchain.env('CCFLAGS')), {'-g','-pedantic'})

    def test_find_triple_4(self):
        toolchain = toolchains.find(toolchain=['x64-linux-gcc-7','gcc-debug','gcc-warning-max'])
        self.assertTrue(toolchain)
        self.assertEqual(toolchain.id, 'x64-linux-gcc-7+gcc-debug+gcc-warning-max')
        self.assertEqual(set(toolchain.tags), {'x64-linux','gcc-7','gcc','debug','warning-max'})
        self.assertEqual(toolchain.prefix, 'x86_64-linux-gnu-')
        self.assertEqual(toolchain.env('CC'), 'x86_64-linux-gnu-gcc-7')
        self.assertEqual(set(toolchain.env('CCFLAGS')), {'-g','-pedantic'})

    def test_find_fail(self):
        with self.assertRaises(toolchains.NotFoundError):
            toolchains.find('x64-linux-msvc')
        with self.assertRaises(toolchains.NotFoundError):
            toolchains.find(['x64-linux-msvc'])
        with self.assertRaises(toolchains.NotFoundError):
            toolchains.find('x64-linux-gcc-7+gcc-release')
        with self.assertRaises(toolchains.NotFoundError):
            toolchains.find('x64-linux-gcc-7', 'gcc-release')
        with self.assertRaises(toolchains.NotFoundError):
            toolchains.find(['x64-linux-gcc-7', 'gcc-release'])
        with self.assertRaises(toolchains.NotFoundError):
            toolchains.find(toolchain='x64-linux-gcc-7+gcc-release')
        with self.assertRaises(toolchains.NotFoundError):
            toolchains.find(toolchain=['x64-linux-gcc-7', 'gcc-release'])


if __name__ == '__main__':
    unittest.main()
