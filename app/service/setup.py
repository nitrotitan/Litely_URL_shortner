from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "app.service.key_generator",
        ["app/service/key_generator.pyx"],
    )
]

setup(
    ext_modules=cythonize(extensions),
)
