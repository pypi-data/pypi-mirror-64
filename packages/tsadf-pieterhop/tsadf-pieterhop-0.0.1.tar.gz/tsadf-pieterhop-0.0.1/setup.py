import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tsadf-pieterhop", 
    version="0.0.1",
    author="Pieter Hoppenbrouwers",
    author_email="pieterhoppenbrouwers@hotmail.com",
    description="A framework for detecting anomalies in time-series",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/rakibulmdalam/time-series-anomaly-detection-framework/src/master/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)