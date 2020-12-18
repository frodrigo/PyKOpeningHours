from skbuild import setup

setup(
    name="PyKOpeningHours package",
    version="1.3.0",
    description="Validator for OSM opening_hours expressions",
    author='David Faure',
    license="AGPL",
    package_data={'PyKOpeningHours': ['py.typed', 'PyKOpeningHours.pyi']},
    packages=['PyKOpeningHours'],
)
