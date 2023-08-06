__version__ = '0.0.1'

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='robogercontrib.android',
                 version=__version__,
                 author='altertech',
                 author_email='div@altertech.com',
                 description='A small example package',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 url='https://github.com/pypa/sampleproject',
                 packages=setuptools.find_packages(),
                 classifiers=[
                     'Programming Language :: Python :: 3',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: OS Independent',
                 ],
                 python_requires='>=3.6',
                 install_requires=['filetype', 'pyfcm', 'roboger'])
