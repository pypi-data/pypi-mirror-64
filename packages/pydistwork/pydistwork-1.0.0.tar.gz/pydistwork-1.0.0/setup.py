from setuptools import setup, find_packages

long_description = 'Sample Package made for a demo to see how to use resource files in python dists'

setup(
    name='pydistwork',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pydistwork = package.mymodule1:main'
        ]
    },
    zip_safe=False,
    include_package_data=True
)