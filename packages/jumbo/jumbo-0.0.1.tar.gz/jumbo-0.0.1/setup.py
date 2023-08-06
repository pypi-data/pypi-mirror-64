import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jumbo",  # Replace with your own username
    version="0.0.1",
    author="Alvise Vianello",
    author_email="alvise.vianello13@gmail.com",
    description="A psycopg2 PostgreSQL wrapper for scientists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
