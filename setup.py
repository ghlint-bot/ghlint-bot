from setuptools import setup, find_packages
setup(
    name = "ghlinter",
    version = "0.1",
    packages = find_packages('ghlinter/__init__.py'),
    package_dir={'ghlinter':'ghlinter'},
    package_data = {
        # If any package contains *.json files, include them:
        '': ['*.json']
    }
)