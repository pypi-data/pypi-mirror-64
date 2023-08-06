from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="habib-bitcoin-price",
    version="1.0.7",
    description="BITCOIN PRICE NOTIFICATION",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/md-habibullah-au7/python_project",
    author="Md Habibullah",
    author_email="habibdeoraji@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["habib_bitcoin_m"],
    include_package_data=True,
    install_requires=["requests", "datetime"],
    entry_points={
        "console_scripts": [
            "habib-bitcoin-price = habib_bitcoin_m.bitcoin_price_alert : arg_main ",
        ]
    },
)