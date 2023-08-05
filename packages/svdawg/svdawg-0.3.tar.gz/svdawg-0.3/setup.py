import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='svdawg',
     version='0.3',
     author="Simone Longo",
     author_email="s.longo@utah.edu",
     description="SVD accessories, widgets, and graphics",
     long_description=long_description,
     long_description_content_type='text/markdown',
     install_requires=[
          'pandas',
          'numpy',
          'seaborn',
          'matplotlib',
          'sklearn'
      ],
     url="https://github.com/SpacemanSpiff7/svdawg",
     packages=setuptools.find_packages(),
     license='MIT',
     python_requires='>=3.6',
     zip_safe=False
 )
