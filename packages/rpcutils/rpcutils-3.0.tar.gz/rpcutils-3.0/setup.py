from setuptools import setup

setup(name='rpcutils',
      description = 'RPC Utilities',
      long_description = """A set of utilities for using VistA's RPC Broker Interface""",
      version='3.0',
      python_requires='>=3.3, <4',
      classifiers = ["Development Status :: 4 - Beta", "Programming Language :: Python :: 3"],
      url='http://github.com/Caregraf/rpcutils',
      license='Apache License, Version 2.0',
      keywords='VistA,RPC',
      package_dir = {'rpcutils': ''},
      packages = ['rpcutils']
)
