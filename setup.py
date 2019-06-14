# coding: utf-8

from setuptools import setup, find_packages

version = '0.1.1'


requirements = [
    'setuptools',
    'six',
    'pyyaml',
]


entry_points = """
      [console_scripts]
      # rule = rule.cli:main
      """

scripts = [
]

setup(name='rule',
      version=version,
      description="A rule engine written in python.",
      long_description=open("README.md").read(),
      long_description_content_type='text/markdown',
      # Get more strings from
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      url="https://github.com/tclh123/rule",
      keywords=['rule'],
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
