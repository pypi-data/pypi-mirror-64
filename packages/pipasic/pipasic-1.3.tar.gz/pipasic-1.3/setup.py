import setuptools

setuptools.setup(
    name="pipasic",
    version="1.3",
    author="Martin S. Lindner, LindnerM@rki.de, and Anke Penzlin, Robert Koch-Institut, Germany",
    author_email="LindnerM@rki.de",
    description="pipasic - peptide intensity-weighted proteome abundance similarity correction",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/wangxuesong29/pipasic/-/tree/master",
    packages=setuptools.find_packages(),
    install_requires=['Biopython==1.76', 'Numpy==1.16.6', 'matplotlib==1.4.3', 'scipy==1.2.3', 'six==1.14.0'],
    entry_points={
        'console_scripts': [
            'pipasic=src:main'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 2"
    ]
)