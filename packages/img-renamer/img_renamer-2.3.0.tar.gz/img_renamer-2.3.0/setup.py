import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="img_renamer",
    version="2.3.0",
    author="Miika Launiainen",
    author_email="miika.launiainen@gmail.com",
    description="Script to rename images in numberic order",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/miicat/img_renamer",
    scripts=['img_renamer/img_renamer'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
)
