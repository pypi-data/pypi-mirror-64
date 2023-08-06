from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

with open("requirements.txt", "r") as _requirements:
    requirements = list(map(str.strip, _requirements.read().split("\n")))

setup(
    name="btmhdw",
    version="2.2.2",
    description="The implementation of Hierarchical Deterministic (HD) wallets generator for Bytom blockchain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Meheret Tesfaye",
    author_email="meherett@zoho.com",
    url="https://github.com/meherett/btmhdw",
    packages=find_packages(),
    python_requires=">=3.5,<4",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
)
