import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.2.3'
NAME = 'URToPulseConverter'
AUTHOR = 'Ostapets Vladislav'
AUTHOR_EMAIL = 'vlad12344444@gmail.com'
LONG_DESCRIPTION_CONTEXT_TYPE = 'text/markdown'
DESCRIPTION = "UR Robot script -> 'Rozum Robotics' Pulse Robots code converter "
PACKAGES = [
    'postprocessor',
    'processedPrograms',
    'RoboDKPrograms',
    'screenshots',
    'postprocessor\converter'
]
REQUIRED = [
    'numpy==1.18.0'
]

def read_long_description():
    try:
        path = os.path.join(here, "README.md")
        with open(path, "r") as ld:
            return ld.read()
    except FileNotFoundError:
        return DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=read_long_description(),
    long_description_content_type=LONG_DESCRIPTION_CONTEXT_TYPE,
    packages=PACKAGES,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
    install_requires=REQUIRED,
    entry_points={
        "console_scripts": [
            "URToPulse=postprocessor.main:main"
        ]
    }
)