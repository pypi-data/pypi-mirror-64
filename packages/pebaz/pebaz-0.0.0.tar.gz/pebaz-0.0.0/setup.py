from setuptools import setup
import nimporter

setup(
    name='pebaz',
    author='https://github.com/Pebaz',
    packages=['pebaz'],
    ext_modules=nimporter.build_nim_extensions()
)
