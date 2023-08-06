import os
from setuptools import setup

SETUP_PTH = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(SETUP_PTH, 'requirements.txt')) as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mpcontribs-client',
    author='Patrick Huck',
    author_email='phuck@lbl.gov',
    description="client library for MPContribs API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/materialsproject/MPContribs/tree/master/mpcontribs-client',
    packages=['mpcontribs.client'],
    install_requires=required,
    license='MIT',
    zip_safe=False,
    include_package_data=True,
    use_scm_version={"root": "..", "relative_to": __file__},
    setup_requires=['setuptools_scm'],
)
