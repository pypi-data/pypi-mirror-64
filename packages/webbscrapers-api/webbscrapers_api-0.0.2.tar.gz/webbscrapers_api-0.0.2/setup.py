import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webbscrapers_api", # Replace with your own username
    version="0.0.2",
    author="Example Author",
    author_email="author@example.com",
    description="Python module to access Webbscrapers API - https://webbscrapers.live",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edwudw/webbscrapers_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
