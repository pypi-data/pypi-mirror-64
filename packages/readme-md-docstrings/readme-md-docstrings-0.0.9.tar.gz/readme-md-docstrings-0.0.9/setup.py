from setuptools import setup

setup(
    name='readme-md-docstrings',
    version="0.0.9",
    description=(
        'Update README.md from Docstrings'
    ),
    author='David Belais',
    author_email='david@belais.me',
    python_requires='>=3.6',
    py_modules=['readme_md_docstrings'],
    install_requires=[],
    extras_require={
        "dev": [
            "wheel>=0.34.2",
            "setuptools>=40.8.0",
            "setuptools-setup-versions>=0.0.29",
            "pytest>=5.4.1",
            "twine>=3.1.1",
            "tox>=3.14.5"
        ],
        "test": [
            "pytest>=5.4.1",
            "tox>=3.14.5"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)