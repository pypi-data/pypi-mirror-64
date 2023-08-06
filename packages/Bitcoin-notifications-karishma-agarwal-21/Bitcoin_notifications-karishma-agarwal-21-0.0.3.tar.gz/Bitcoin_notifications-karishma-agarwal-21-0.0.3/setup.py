import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Bitcoin_notifications-karishma-agarwal-21", # Replace with your own username
    version="0.0.3",
    author="Karishma Agarwal",
    author_email="karishmaag21@gmail.com",
    description="A small project for bitcoin price notifications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karishma-garg-au7/bitcoin_notification",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
