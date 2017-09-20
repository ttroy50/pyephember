from setuptools import setup, find_packages

setup(name='pyephember',
      version='0.0.1',
      description='Python library to work with ember from EPH Controls',
      keywords='eph ember',
      author='Thom Troy',
      author_email='ttroy50@gmail.com',
      license='MIT',
      url='https://github.com/ttroy50/PyEphEmber',
      platforms=["any"],
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          'requests',
      ],
     )