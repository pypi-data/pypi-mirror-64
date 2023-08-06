from setuptools import setup

setup(name='inisync',
      version='1.0',
      description='Sync value from one INI file to others',
      author='Constantin Gruber',
      author_email='constantin.gruber@sixsentix.com',
      packages=['inisync'],
      entry_points = {
        "console_scripts": ['inisync = inisync.inisync:main']
      },
      python_requires='>=3.6',
     )
