import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xtproductjson", # Replace with your own username
    version="0.0.1",
    author="sg",
    author_email="swatigupta01998@gmail.com",
    description="Can be used to convert product excel sheet to list",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nkman/xt-product-template-lib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)