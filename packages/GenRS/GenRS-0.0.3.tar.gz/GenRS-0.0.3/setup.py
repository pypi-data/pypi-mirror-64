import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GenRS", # Replace with your project name
    version="0.0.3",
    author="Roberto Cedolin",
    author_email="roberto.cedo@gmail.com",
    description="A State-Of-Art framework for Recommendation Systems algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cedo1995/GenRS",   # Replace it with the github link to repository
    packages=setuptools.find_packages(),  # Find the packages used in the code
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
