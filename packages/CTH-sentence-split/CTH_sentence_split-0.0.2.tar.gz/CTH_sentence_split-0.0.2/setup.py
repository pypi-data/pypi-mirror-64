import setuptools

with open("CTH_sentence_split/README.md", "r") as fh:
    long_description = fh.read()
print(long_description)
setuptools.setup(
    name="CTH_sentence_split",  # Replace with your own username
    version="0.0.2",
    author="Eran Hsu",
    author_email="eran0926@gmail.com",
    description="Chinese (Traditional), Taiwanese and Hakka's sentence split tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Traditional)",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.6',
)
