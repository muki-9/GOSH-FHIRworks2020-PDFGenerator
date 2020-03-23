import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='GOSH-FHIRworks2020-PDFGenerator',
    version='0.0.1',
    author='Mukilan Bakeerathan',
    author_email='zcabmba@ucl.ac.uk',
    description='A PDF Letter Generator for Doctors',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/muki-9/GOSH-FHIRworks2020-PDFGenerator',
    license='Apache License 2.0',
    install_requires=['requests>=2.23.0', 'FHIR-Parser>=-0.1.5'],
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)