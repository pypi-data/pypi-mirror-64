#!/usr/bin/env python

try:
    # from setuptools import setup
    from setuptools import find_packages, setup, Command
    import io
    import os
    import sys
    from shutil import rmtree
except ImportError:
    from distutils.core import setup


# Package meta-data.
NAME = 'wd-crawler-client'
DESCRIPTION = 'spider framework for winndoo.'
URL = 'http://git.winndoo.cn:82/python/download_center/downloader_client.git'
EMAIL = 'baozhu.zhang@winndoo.com'
AUTHOR = 'Welcome#1'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '6.0.1'


here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION



class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


setup(
      name=NAME,
      version=about['__version__'],
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type='text/markdown',
      author=AUTHOR,
      author_email=EMAIL,
      python_requires=REQUIRES_PYTHON,
      url=URL,
      keywords=['crawler', 'wendao'],
      packages=['wd_crawler_client', 'wd_crawler_client.crawler', 'wd_crawler_client.lib'],
      install_requires=[
          'mysqlclient>=1.4.6',
          'Twisted>=18.9.0',
          'treq>=18.6.0',
      ],
      # $ setup.py publish support.
      cmdclass={
          'upload': UploadCommand,
      },
)

