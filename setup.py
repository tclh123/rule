# coding: utf-8

from setuptools import setup, find_packages

version = '0.1.0'


requirements = [
    'setuptools',
    'six',
    'pyyaml',
]


entry_points = """
      [console_scripts]
      # rule = rule_engine.cli:main
      """

scripts = [
]

setup(name='rule-engine',
      version=version,
      description="Rule engine",
      long_description=open("README.md").read(),
      # Get more strings from
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords='',
      author='Harry Lee',
      author_email='tclh123@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['examples*', 'tests*']),
      include_package_data=True,
      zip_safe=False,
      entry_points=entry_points,
      scripts=scripts,

      install_requires=requirements,
)  # NOQA
