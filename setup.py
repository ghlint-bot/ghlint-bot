from setuptools import setup

setup(name = "ghlinter",
    version = "0.1",
    packages = ['ghlinter'],
    package_dir={'ghlinter':'src/ghlinter'},
    package_data = {
        # If any package contains *.json files, include them:
        '': ['*.json']
    }
)