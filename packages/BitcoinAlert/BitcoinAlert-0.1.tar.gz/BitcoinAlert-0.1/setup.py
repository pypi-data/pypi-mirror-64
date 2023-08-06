from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'BitcoinAlert',
    version = '0.01',
    author="Praveen",
    author_email="praveenacchusn123@gmail.com",
    description = 'Sends bitcoin alerts !',
    py_modules = ['bitcoinInitialize'],
    package_dir = {'': 'src'},
    url="https://github.com/praveenNagaraj97-au7/bitcoinAlertWithTelegram",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[            # I get to this in a second
          'tqdm',
      ],
)