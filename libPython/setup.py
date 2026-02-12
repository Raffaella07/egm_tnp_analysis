from distutils.core import setup
from distutils.extension import Extension
import os
import sys

if '--use-cython' in sys.argv:
	USE_CYTHON = True
	sys.argv.remove('--use-cython')
else:
	USE_CYTHON = False
ext = '.pyx' if USE_CYTHON else '.cpp'

sourcefiles = ["histUtils" + ext]

# Prendi flags dall'ambiente (se presenti)
cxxflags = os.environ.get("CXXFLAGS", "")
cflags = os.environ.get("CFLAGS", "")
ldflags = os.environ.get("LDFLAGS", "")

extra_compile = (cxxflags + " " + cflags).split()
extra_link = ldflags.split()

extensions = [Extension(
	"histUtils",
	sourcefiles,
	language="c++",
	extra_compile_args=extra_compile,
	extra_link_args=extra_link,
)]

if USE_CYTHON:
	from Cython.Build import cythonize
	extensions = cythonize(extensions)

setup(ext_modules=extensions)

