from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(packages=find_packages(),
    name="pharmpy",
    version="0.0.1",
    description="pharmpy is an umbrella library for searching the FDA NDC directory, Established Pharmacologic Class (EPC), Anatomical Therapeutic Chemical (ATC) through RxNav, and some other APIs on RxNav.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yubin Park",
    author_email="yubin.park@gmail.com",
    url="https://github.com/yubin-park/pharmpy",
    license="Apaceh 2.0", 
    install_requires = [],
    include_package_data=True,
    package_data={"": ["*.txt", "*.csv"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ])


