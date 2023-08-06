from setuptools import setup

setup(name='pomegranate-mathematica',
      version='0.1',
      description='Wolfram Mathematica distributions parser for pomegranate',
      url='https://github.com/d-lowl/pomegranate-mathematica',
      author='D. Lowl',
      author_email='dlowl@sihvi.com',
      license='MIT',
      packages=['pomegranate_mathematica'],
      install_requires=[
          'pomegranate==0.11',
          'lark-parser'
      ],
      zip_safe=False)