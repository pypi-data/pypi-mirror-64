import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='svdawg',
     version='0.1',
     author="Simone Longo",
     author_email="s.longo@utah.edu",
     description="SVD accessories, widgets, and graphics",
     install_requires=[
          'pandas',
          'numpy',
          'seaborn',
          'matplotlib',
          'sklearn'
      ],
     url="https://github.com/SpacemanSpiff7/svdawg",
     packages=['svdawg'],
     license='MIT',
     zip_safe=False
 )
