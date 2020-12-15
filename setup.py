from skbuild import setup

setup(
    name="PyKOpeningHours package",
    version="1.2.0",
    description="Validator for OSM opening_hours expressions",
    author='David Faure',
    license="AGPL",
    packages=['PyKOpeningHours'],
    package_dir={'': 'src'},
    cmake_install_dir='lib/PyKOpeningHours'
)
