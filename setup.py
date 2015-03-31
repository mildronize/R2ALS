import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()

requires = [
    'mongoengine',
    'rainbow_logging_handler',
    'pyramid',
    'pyramid_mako',
    'pyramid_debugtoolbar',
    'pyramid_beaker',
    'waitress',
    'wsgicors'
    ]


setup(name='r2als',
      version='0.2.0',
      description='r2als',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        ],
      author='Thada Wangthammang',
      author_email='mildronize@gmail.com',
      url='http://blog.mildronize.com',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="r2als",
      entry_points = """\
      [paste.app_factory]
      main = r2als:main
      [console_scripts]
      initialize_r2als_db = r2als.scripts.initial_db:main
      initialize_test_case = r2als.scripts.initial_test_case:main
      """,
      )
