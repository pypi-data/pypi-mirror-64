import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='hue-snek-channel42',
    version='0.3',
    author="Channel 42",
    author_email="",
    description="A library for the Philips Hue API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/channel-42/hue-snek",
    packages=setuptools.find_packages(),
    install_requires=['urllib3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
