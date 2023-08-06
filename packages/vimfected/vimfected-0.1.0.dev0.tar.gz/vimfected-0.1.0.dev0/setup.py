import codecs
import os

from setuptools import setup, find_packages


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version():
    for line in read("src/vimfected/__init__.py").splitlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="vimfected",
    version=get_version(),
    author="Brian Smith",
    author_email="brian.e.smith@gmail.com",
    description="Tile-based adventure game driven by vim key bindings",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/Lytol/vimfected",
    license="GPLv3",
    packages=find_packages(where='src'),  # Required
    package_dir={'': 'src'},  # Optional
    package_data={'vimfected': ['assets/**/*']},
    install_requires=["pygame"],
    extras_require={
        'dev': ['pytest', 'coverage', 'flake8', 'twine'],
    },
    entry_points={
        'console_scripts': [
            'vimfected=vimfected:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='game pygame',  # Optional
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
)
