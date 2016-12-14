"""The setup for our http-server project."""

from setuptools import setup

setup(
    name="Http-server",
    description="Implementations of an http-server",
    version=0.2,
    author="Maelle Vance, Ford Fowler",
    author_email="maellevance@gmail.com, fordjfowler@gmail.com",
    license="MIT",
    py_modules=[
        'server', 'client'
    ],
    package_dir={'': 'src'},
    install_requires=[],
    extras_require={
        "test": ["tox", "pytest", "pytest-watch", "pytest-cov"]
    },
    entry_points={
        'console_scripts': [
            'client = client:main',
            'server = server:server'
        ]
    }
)
