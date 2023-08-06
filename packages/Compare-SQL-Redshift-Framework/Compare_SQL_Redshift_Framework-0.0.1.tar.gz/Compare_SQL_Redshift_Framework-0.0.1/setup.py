from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Compare_SQL_Redshift_Framework',
    version='0.0.1',
    description='Compare_SQL_Redshift_Framework Test Upload',
    py_modules=["Compare_SQL_RedShift", "DaskUtil", "MasterClass"],
    package_dir={'': 'src'},
    author="Rajnish",
    author_email="rajnish.kumar@acacceptance.com",
    include_package_data=True,
    url="https://acapgit.acacceptance.com/projects/AWA/repos/libraries/browse",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[

    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
        ],
    },
)
