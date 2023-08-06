from setuptools import setup

setup(name='asterism',
      version='0.5',
      description='Helpers for Project Electron infrastructure',
      url='http://github.com/RockefellerArchiveCenter/asterism',
      author='Rockefeller Archive Center',
      author_email='archive@rockarch.org',
      install_requires=[
          'bagit',
          'django',
          'djangorestframework',
          'psycopg2',
          'odin'],
      license='MIT',
      packages=['asterism', 'asterism.resources'],
      test_suite='nose.collector',
      tests_require=[
          'nose',
          'bagit',
          'django',
          'djangorestframework',
          'psycopg2'],
      zip_safe=False)
