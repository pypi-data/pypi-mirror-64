import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytholenium",
    version="1.0.0",
    author="Dario Argies",
    author_email="argiesdario@gmail.com",
    description="Python-Selenium selector to improve your Automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArgiesDario/pytholenium",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)