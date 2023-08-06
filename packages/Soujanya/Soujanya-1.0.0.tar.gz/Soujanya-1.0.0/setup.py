from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="Soujanya",
    version="1.0.0",
    description="A Python package to add two numbers.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    #url="",
    author="Soujany",
    author_email="hamsu8977@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Soujanya"],
    include_package_data=True,
    install_requires=["json"],
    entry_points={
        "console_scripts": [
            "Soujanya=Soujanya.addTwoNumbers:main",
        ]
    },
)