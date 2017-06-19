from setuptools import find_packages, setup


setup(name='dcos-shakedown',
      version='1.4.4',
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
          'dcoscli==0.4.16',
          'paramiko',
          'pytest',
          'pytest-timeout',
          'retrying',
          'scp'
      ],
      entry_points="""
      [console_scripts]
      shakedown=shakedown.cli.main:cli
      dcos-shakedown=shakedown.cli.main:cli
      """
      )
