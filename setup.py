from codecs import open as codecs_open
from setuptools import setup, find_packages


setup(name='shakedown',
      version='0.0.1',
      description=u"shakedown",
      long_description=u"ssshhhaaakkkeeedddooowwwnnn",
      classifiers=[],
      keywords='',
      author=u"Mesosphere QE",
      author_email='qe-team@mesosphere.com',
      url='https://...',
      license='Apache 2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'dcoscli==0.4.4',
          'paramiko',
          'pytest',
      ],
      entry_points="""
      [console_scripts]
      shakedown=shakedown.cli.main:cli
      dcos-shakedown=shakedown.cli:cli
      """
      )
