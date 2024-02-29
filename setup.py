from setuptools import setup, find_packages

setup(
    name='k8sh',
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "prompt_toolkit==3.0.39"
    ],
    entry_points={
        'console_scripts': [
            'k8sh=bootstrap.main:main',
        ],
    },
)
