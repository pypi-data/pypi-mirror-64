from setuptools import setup, find_packages

readme = open('README.rst').read() + open('CHANGELOG.rst').read()

setup(name='service_factory',
      version='0.1.6',
      url='https://github.com/proofit404/service-factory',
      description='JSON RPC service factory for Python.',
      long_description=readme,
      platforms='any',
      license='GPL3',
      author='Artem Malyshev',
      author_email='proofit404@gmail.com',
      maintainer='Artem Malyshev',
      maintainer_email='proofit404@gmail.com',
      packages=find_packages(),
      zip_safe=False,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Software Development',
      ])
