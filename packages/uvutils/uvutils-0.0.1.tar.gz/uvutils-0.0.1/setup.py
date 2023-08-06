from setuptools import setup, find_packages

setup(
   name='uvutils',
   version='0.0.1',
   author='Jerry Duncan',
   author_email='mikeynjerry@gmail.com',
   packages=find_packages(),
   description='Utility functions for various Uvulab projects',
   long_description=open('README.md').read(),
   install_requires=[
     'numpy',
     'opencv-python',
     'pillow'
   ],
   python_requires='>3.6'
)