from setuptools import setup, find_packages

setup(
    name="audioprocess",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pydub",
        "tqdm",
        "audioop-lts; python_version >= '3.13'",
    ],
    entry_points={
        'console_scripts': [
            'audioprocess=audioprocess.cli:main_menu',
        ],
    },
    author="CeleroLab",
    description="A reusable audio processing library",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
