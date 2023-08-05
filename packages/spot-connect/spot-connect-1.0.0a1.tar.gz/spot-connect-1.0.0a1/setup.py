from setuptools import setup, find_packages 
from os import path 

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f: 
	long_description = f.read()

setup( 
	name='spot-connect',
	version='1.0.0a1',
	description='A package to create and manage AWS resources, centered around EC2 spot-instances',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/losDaniel/spot-connect.git',
	author='Carlos Valcarcel',
	author_email='carlos.d.valcarcel.w@gmail.com',
	license='MIT',
	keywords='aws ec2 cloud ssh machinelearning virtualmachine',
	package_dir={'':'spot-connect'},
	packages=find_packages(where='spot-connect'),
	install_requires=['boto3','netaddr','paramiko',],
	python_requires='>=3.7',
)