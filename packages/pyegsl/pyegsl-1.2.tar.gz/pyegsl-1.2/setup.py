import setuptools
from distutils.core import setup, Extension

def main():
    setup(name="pyegsl",
          version="1.2",
          description="Python easy interface to gsl",
          author="Heitor L. Werneck",
          author_email="heitorwerneck@hotmail.com",
          url='https://github.com/heitor57/pyegsl',
          license="MIT",
          packages=setuptools.find_packages(),
          ext_modules=[Extension(
              "binomial", ["pyegsl/binomial.cpp"],
              libraries = ['gsl','gslcblas'])])

if __name__ == "__main__":
    main()

