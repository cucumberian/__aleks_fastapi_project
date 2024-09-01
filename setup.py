from setuptools import find_packages, setup

setup(
    name='to_sqlalchemy',  # This is the name of your package
    version='1.0',
    packages=find_packages(where='src'),  # This finds all packages under the 'src' directory
    package_dir={'': 'src'},  # This tells setuptools that packages are under the 'src' directory
)
