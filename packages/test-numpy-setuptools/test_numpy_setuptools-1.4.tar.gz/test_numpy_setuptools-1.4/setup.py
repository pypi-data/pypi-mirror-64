# -*- coding: utf-8 -*-


# coding: utf-8

from distutils.core import setup
from setuptools import setup

setup(name='test_numpy_setuptools',  # 打包后的包文件名
      version='1.4',
      description='test_numpy_setuptools backpack',  # 说明
      author='smilencezq',
      author_email='smilencezq@163.com',
      url='',
      py_modules=['test_numpy_setuptools.test_numpy_setuptools_main',
                  'test_numpy_setuptools.test_numpy_setuptools_multi'],
      requires=['numpy']  # 你要打包的文件
      )
