import os

import setuptools

version = os.environ.get('CI_COMMIT_TAG')
if version is None:
    raise ValueError('CI_COMMIT_TAG variable is not set')

setuptools.setup(
    name='json-datetime-noamfisher',  # fill this
    version=version,
    description='My awesome package',
    author='Me',
    author_email='info@python-private-package-index.com',
    license='MIT',
    packages=setuptools.find_packages()
)
