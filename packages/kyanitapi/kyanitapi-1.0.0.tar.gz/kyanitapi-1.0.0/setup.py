import setuptools

import kyanitapi

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='kyanitapi',
    version=kyanitapi.__version__,
    author='Zsolt Nagy',
    author_email='zsolt@kyanit.eu',
    description='Python API for Kyanit',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kyanit-project/kyanitapi',
    packages=setuptools.find_packages(),
    install_requires=[
        'psutil',
        'pythonping'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
