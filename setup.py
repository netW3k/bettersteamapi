from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name="bettersteamapi",
    version="0.1.4",
    description="""bettersteamapi is a python package with a set of functions to easily access data of steam games via steam API""",
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    author="Wiktor Wolarz",
    author_email="wektor.networking@gmail.com",
    license="MIT",
    py_modules=["bettersteamapi.steamfunctions", "bettersteamapi.config"],
    url="https://github.com/netW3k/BetterSteamAPI",
    python_requires = '>= 3.9',
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
