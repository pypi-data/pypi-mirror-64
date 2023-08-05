import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crsmongo",
    version="1.0.6",
    author="Chris Chen",
    author_email="wsywddr@163.com",
    description="This is my personal mongo toolkit.",
    longe_description=long_description,
    longe_description_content_type="text/markdown",
    url="https://github.com/wsywddr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'pymongo==3.10.0'
    ]
)