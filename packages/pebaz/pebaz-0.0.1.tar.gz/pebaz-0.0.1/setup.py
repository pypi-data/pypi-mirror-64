from setuptools import setup
import nimporter

setup(
    name='pebaz',
    version='0.0.1',
    author='https://github.com/Pebaz',
    packages=['pebaz'],
    ext_modules=nimporter.build_nim_extensions()
)
