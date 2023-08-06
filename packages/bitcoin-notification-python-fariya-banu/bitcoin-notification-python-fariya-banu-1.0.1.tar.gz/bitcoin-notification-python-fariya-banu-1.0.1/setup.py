import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bitcoin-notification-python-fariya-banu", # Replace with your own username
    version="1.0.1",
    author="FARIYA BANU",
    author_email="fariyabanu234@gmail.com",
    description="BITCOIN PRICE NOTIFICATION PROJECT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fariya-banu234-au7/python_project",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_reeuires= ['requests','datetime']
)