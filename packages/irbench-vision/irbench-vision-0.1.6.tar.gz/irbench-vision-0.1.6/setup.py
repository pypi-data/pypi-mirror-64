from setuptools import setup

from setuptools import find_packages

setup(name='irbench-vision',
      version='0.1.6',
      description='Image Retrieval Performance Benchmark on Large-scale Dataset',
      url='',
      author='Minchul Shin',
      author_email='min.nashory@navercorp.com',
      license='INTERNER_USE_ONLY',
      packages=['irbench'],
      package_dir={'irbench': 'src'},
      zip_safe=False)
