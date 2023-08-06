# type: ignore
import setuptools

setuptools.setup(
    name="pyring",
    version="0.0.11",
    author="Jacob Richter",
    author_email="jaycorichter@gmail.com",
    description="A ring buffer implemented in pure python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jaycosaur/pyring",
    packages=setuptools.find_packages(),
    package_data={"pyring": ["py.typed"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
