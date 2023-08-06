import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastTF", # Replace with your own username
    version="1.0.3",
    author="Azfar Mohamed",
    author_email="azfarmah@outlook.com",
    description="Converts Pandas Dataframe to Tensorflow TFRecord",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/azfar154/fastTF",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
   'pandas',
   'tensorflow>=2.0.0'
]
)

