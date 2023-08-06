from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="Soujanya2",
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
    packages=["Soujanya2"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "Soujanya2=Soujanya2.addTwoNumbers:main",
        ]
    },
)