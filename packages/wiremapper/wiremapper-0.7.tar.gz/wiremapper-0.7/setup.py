from setuptools import setup

setup(
    name='wiremapper',
    version='0.7',
    packages=['wiremapper', 'wiremapper.block'],
    url='https://gitlab.com/MartijnBraam/wiremapper',
    license='MIT',
    author='Martijn Braam',
    author_email='martijn@brixit.nl',
    description='Library and command line client for the Pockethernet network tester',
    long_description=open("README.rst").read(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX :: Linux',
    ],
    install_requires=[
        'pockethernet>=0.5.0',
        'pycairo'
    ],
    zip_safe=True,
    include_package_data=True,
    entry_points={
        'gui_scripts': [
            'wiremapper=wiremapper.__main__:main'
        ]
    }
)
