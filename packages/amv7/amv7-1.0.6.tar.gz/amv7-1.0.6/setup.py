from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="amv7",
    version="1.0.6",
    description="A Python package for bypassing the security of PUBGM.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/abhiman-alt/amv7",
    author="Abhiman Varya",
    author_email="contact@abhiman.co",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["amv7"],
    install_requires=["lolcat"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "amv7=amv7.cli:main",
        ]
    },
)