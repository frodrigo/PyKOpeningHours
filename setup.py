from skbuild import setup

setup(
    name="PyKOpeningHours package",
    version="1.0.0",
    description="Validator for OSM opening_hours expressions",
    author='David Faure',
    license="AGPL",
    packages=['PyKOpeningHours'],
    package_dir={'': 'lib'},
    cmake_install_dir='.'
)
