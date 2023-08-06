import os

import setuptools

setuptools.setup(
    name=f'json-datetime-noamfisher',
    version=os.environ.get('CI_COMMIT_TAG'),
    description='allows you to dump / load jsons that contain date / datetime objects',
    author=os.environ.get('GITLAB_USER_NAME'),
    author_email=os.environ.get('GITLAB_USER_EMAIL'),
    extras_require={
        'test': ['pytest']
    },
    packages=setuptools.find_packages()
)
