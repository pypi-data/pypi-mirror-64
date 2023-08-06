from setuptools import setup, find_packages

setup(name='deadsimplekv',
      version='0.3.0',
      description='Very simple key-value store for Python',
      author='Kevin Froman',
      author_email='beardog@mailbox.org',
      url='https://github.com/beardog108/deadsimplekv',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=[],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
      ],
     )
