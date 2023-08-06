"""gpustat-web"""

import sys

from setuptools import setup

IS_PY_2 = (sys.version_info[0] <= 2)

install_requires = [
  # 'gpustat>=0.5.0',
  'six>=1.7',
  'termcolor',
  'ansi2html',
  'asyncssh',
  'aiohttp>=3.0.0',
  'aiohttp_jinja2',
  'aiohttp-devtools>=0.8',

  ]

tests_requires = [
  'pytest',
  ]

setup(
  name='gpustat-web',
  version='0.1.0',
  license='MIT',
  description='A web interface of gpustat --- consolidate status across your cluster.',
  url='https://github.com/wookayin/gpustat-web',
  author='Jongwook Choi',
  author_email='wookayin@gmail.com',
  keywords='nvidia-smi gpu cuda monitoring gpustat',
  classifiers=[
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3',
    'Topic :: System :: Monitoring',
    ],
  packages=['gpustat_web'],
  install_requires=install_requires,
  extras_require={'test':tests_requires},
  setup_requires=['pytest-runner'],
  tests_require=tests_requires,
  include_package_data=True,
  zip_safe=False,
  )
