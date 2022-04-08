from setuptools import find_packages, setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name="bettersteamapi",
    version="0.0.3",
    description="""bettersteamapi is a python package with functions that helps with requesting data of games from steam.""",
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    author="Wiktor Wolarz ",
    author_email="",
    license="",
    py_modules=["steamfunctions"],
    url="https://github.com/netW3k/BetterSteamAPI",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    python_requires = '>= 3.8',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
