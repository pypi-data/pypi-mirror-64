
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bitcoinAlertWithTelegram",
    version="1.0.0",
    author="Praveen",
    author_email="praveenacchusn123@gmail.com",
    description="A package that allows to sent bitcoin alerts throgh IFTTT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules = ['bitcoinalert'],
    package_dir = {'': 'src'},
    download_url = 'https://github.com/praveenNagaraj97-au7/bitcoinAlertWithTelegram/archive/0.1.tar.gz',
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 
