from setuptools import setup
import versioneer




setup(
    license="BSD",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    scripts = ['bin/gbmgeo_make_images']
)
