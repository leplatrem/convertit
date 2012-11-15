import os
from setuptools import setup, find_packages
requires = [
    'Paste',
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'sqlalchemy',
    'repoze.tm2',
    'cryptacular',
    'WebOb',
    'WebError',
    'repoze.vhm',
    'ipython',
    'bpython',
    ]

test_requires = requires + [
    'webtest',
    'plone.testing',
    'mock',
    'coverage',
    'nose',
    ]


def read(*rnames):
    return open(
        os.path.join('.', *rnames)
    ).read()


long_description = "\n\n".join(
    [read('README.rst'),
     read('CHANGES.rst'),
    ]
)


version = '1.0dev0'

setup(name='convertit',
      version=version,
      description='convertit',
      long_description=long_description,
      license='AGPLV3',
      classifiers=[
          "License :: OSI Approved :: GNU Affero General Public License v3",
          "Programming Language :: Python",
          "Framework :: Pylons",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Makina Corpus',
      author_email='python@makina-corpus.org',
      url='https://github.com/makinacorpus/convertit',
      keywords='web pyramid webservice convert',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=test_requires,
      extras_require = {
          'test': test_requires,
      },
      test_suite="convertit",
      entry_points="""\
      [paste.app_factory]
      main = convertit:main
      """,
     )
