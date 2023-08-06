from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="bitcoin-notification-f",
    version="1.0.3",
    description="BITCOIN PRICE NOTIFICATION",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/fariya-banu234-au7/python_project",
    author="Fariya Banu",
    author_email="fariyabanu234@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["bitcoin_notification_f"],
    include_package_data=True,
    install_requires=["requests", "datetime"],
    entry_points={
        "console_scripts": [
            "bitcoin-notification-f = bitcoin_notification_f.bitcoin_price_notification:cli",
        ]
    },
)