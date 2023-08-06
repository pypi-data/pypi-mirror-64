from setuptools import setup

setup(
  name = 'redis-distributed-lock',
  version = "1.0",
  description = "Redis distributed lock for python",
  long_description = "Redis distributed lock for python, using setnx and getset, provide block and no-block funtion",
  license="MIT",
  keywords = 'redis distributed lock',
  author = 'halukshan',
  author_email = 'halukshan@gmail.com',
  url = 'http://github.com/halukshan/redis-distributed-lock',
  classifiers = ['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Natural Language :: English',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 3.7'
  ],
  packages = ['redis-lock'],
)