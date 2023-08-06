import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="dicto-pkg",
    version="0.0.2",
    author="Nathanael Tehilla",
    author_email="nathanael.tehilla@gmail.com",
    description="Looks up definition of words you highlight/select",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/narasaka/dicto",
    packages=setuptools.find_packages(),
    scripts=['bin/dicto', 'bin/dictocaller.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.3',
)
