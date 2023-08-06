import os
from setuptools import setup, find_packages, Command


__version__ = None
exec(open('chess/version.py').read())

class CleanCommand(Command):
    """
    Custom clean command to tidy up the project root.
    """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info ./htmlcov')

setup(
    name='chess-hic',
    version=__version__,
    description='Quantitative comparison and automatic feature extraction for chromatin contact data.',
    # long_description_content_type="text/markdown",
    url='https://github.com/vaquerizaslab/chess',
    download_url='https://github.com/vaquerizaslab/chess/archive/v0.0.2.tar.gz',
    setup_requires=[
        'setuptools>=18.0',
    ],
    packages=find_packages(),
    install_requires=[
        'cython',
        'numpy>=1.8.0',
        'scikit-image',
        'future',
        'pathos',
        'pandas',
        'scipy',
        'intervaltree',
        'pybedtools',
        'tqdm',
        'kneed',
    ],
    scripts=['bin/chess'],
    cmdclass={
        'clean': CleanCommand
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
