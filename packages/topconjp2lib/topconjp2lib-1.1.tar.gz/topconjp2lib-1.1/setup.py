from setuptools import setup
from setuptools.dist import Distribution

DISTNAME = 'topconjp2lib'
DESCRIPTION = 'topcon openjp2 library'
MAINTAINER = ""
MAINTAINER_EMAIL = ""
URL = ""
LICENSE = ""
DOWNLOAD_URL = ""
VERSION = '1.1'
PYTHON_VERSION = (3, 6)

class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

setup(
    name=DISTNAME,
    version=VERSION,
    description=DESCRIPTION,
    packages=[DISTNAME],
    package_data={
        DISTNAME: ['topconopenjp2.dll'],
    },
    distclass=BinaryDistribution,
    python_requires='>=3.6',
)