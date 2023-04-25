from setuptools import setup, Extension
from Cython.Distutils import build_ext

import numpy

ext = Extension("mandel", ["mandelbrot.pyx"], include_dirs=[numpy.get_include()])

setup(ext_modules=[ext], cmdclass={'build_ext': build_ext})
