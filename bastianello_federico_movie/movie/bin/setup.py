from Cython.Build       import cythonize
from distutils.core     import setup


setup(
    ext_modules = cythonize("converter.pyx")
)

