from setuptools import setup, find_packages

setup(
    name='ossfuzz-tooling',
    version='0.1.0',
    author='Davide Ferretti',
    author_email='davide.ferretti8498@gmail.com',
    description='Python utilities for exploring OSS-Fuzz project metadata and fuzzing results',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
    ],
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'ossfuzz-tools=cli:main',
        ],
    },
)