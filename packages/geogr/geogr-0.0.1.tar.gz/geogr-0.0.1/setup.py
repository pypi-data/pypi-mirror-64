import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='geogr',
    version='0.0.1',
    author='Zac Thiel',
    author_email='digitalservices@grcity.us',
    description='Packages for geographical analysis using the City of Grand Rapids infrastructure',
    long_description_content_type='text/markdown',
    url='https://github.com/GRInnovation/geogr',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.4',
)