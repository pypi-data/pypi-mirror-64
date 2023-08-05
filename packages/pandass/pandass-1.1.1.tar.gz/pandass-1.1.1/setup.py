import setuptools
import os
'''
f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
long_description = f.read()
f.close()
'''
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pandass", # Replace with your own username
    version="1.1.1",
    author="Aditya Kumar",
    author_email="Adityakumarec@gmail.com",
    description="This is a simple example package",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
