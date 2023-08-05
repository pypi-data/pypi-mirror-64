# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

VERSION = '1.0.0'

tests_require = []

install_requires = []

setup(name='dict2object',
      url='https://github.com/',
      author="Emory Yan",
      author_email='huaqiangyan@163.com',
      keywords='python dict2obj dict obj',
      description='Automatically register models in the admin interface in a smart way.',
      license='MIT',
      classifiers=[
          'Operating System :: OS Independent',
          'Topic :: Software Development',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: Implementation :: PyPy'
      ],

      version=VERSION,
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='',
      extras_require={},

      entry_points={'nose.plugins': []},
      packages=find_packages(),
      )
