""" Installer
"""
import os
from os.path import join
from setuptools import setup, find_packages

NAME = 'eea.converter'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(join(*PATH)).read().strip()

setup(name=NAME,
      version=VERSION,
      description=("SVG, PNG, PDF converters using external "
                   "tools as ImageMagick"),
      long_description_content_type="text/x-rst",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Zope2",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Zope",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
      ],
      keywords='EEA converter imagemagick utility Add-ons Plone Zope',
      author='European Environment Agency: IDM2 A-Team',
      author_email="eea-edw-a-team-alerts@googlegroups.com",
      download_url="https://pypi.python.org/pypi/eea.converter",
      url='https://github.com/collective/eea.converter',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'kv',
          'PyPDF2',
          'Pillow',
          'Products.statusmessages',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              ],
          'yum': [
              'xorg-x11-server-Xvfb',
              'wkhtmltox',
              'ImageMagick'
              ],
          'apt': [
              'xvfb',
              'wkhtmltopdf',
              'ImageMagick',
              ],
          'zope2': [
          ]
      },
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
