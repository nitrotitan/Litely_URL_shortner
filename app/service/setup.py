from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "key_generator",
        ["key_generator.pyx"],
    )
]

setup(
    ext_modules=cythonize(extensions),
)
