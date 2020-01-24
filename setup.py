from setuptools import setup, find_packages
setup(
    name = "ghlinter",
    version = "0.1",
    package_dir={'':'src'},
    packages = find_packages(where='src'),
    package_data = {
        # If any package contains *.json files, include them:
        '': ['*.json']
    }
)