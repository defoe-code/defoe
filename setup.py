import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="defoe",
    version="0.0.2",
    author="ATI-SE",
    description="Analysis of historical books and newspapers data",
    keywords="text mining, historical, defoe, workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/defoe-code/defoe",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'defoe-submit = defoe-submit:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    python_requires = '>=3.6',
)


