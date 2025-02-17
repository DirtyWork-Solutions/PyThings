from setuptools import setup, find_packages

setup(
    name='pythings',
    version='0.1.0',
    description='abstraction, interaction, and management of anything and everything',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='DirtyWork Solutions Limited',
    author_email='pythings@open.dirtywork.solutions',
    url='https://github.com/DirtyWork-Solutions/PyThings',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pip~=25.0',
        'setuptools~=75.8.0',
        'wheel~=0.45.1',
        'configparser~=7.1.0',
        'loguru~=0.7.3',
        'pyyaml~=6.0.2',
        'pyutil~=0.1.0',
        'pyextend~=0.1.0',
        'pythings~=0.1.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)