import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Complex-Number_Encryptor-Janderion", # Replace with your own username
    version="1.0.0",
    author="Jadenpaul M. Albay",
    author_email="Janderion369@gmail.com",
    description="Package that can encrypt messages using various math equations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Janderion47/Complex-Number-Encryptor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

