from codecs import open as codecs_open
from setuptools import setup, find_packages


setup(name='dcos-shakedown',
      version='1.1.5',
      description=u"DC/OS testing harness and library",
      long_description=u"A tool and library to abstract common DC/OS-related tasks.",
      classifiers=[],
      keywords='',
      author=u"Mesosphere QE",
      author_email='qe-team@mesosphere.com',
      url='https://github.com/dcos/shakedown',
      license='Apache 2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'dcoscli==0.4.13',
          'paramiko',
          'pytest',
          'scp'
      ],
      entry_points="""
      [console_scripts]
      shakedown=shakedown.cli.main:cli
      dcos-shakedown=shakedown.cli.main:cli
      """
      )
