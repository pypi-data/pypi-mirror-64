from setuptools import setup

# reading long description from file
with open('README.md') as file:
    long_description = file.read()


# specify requirements of your package here
REQUIREMENTS = ['docopt==0.6.2']

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: GNU Affero General Public License v3',
    'Programming Language :: Python :: 3'
]

# calling the setup function
setup(name='scalegrid_cli',
    version='1.0.7',
    description='ScaleGrid CLI',
    long_description=long_description,
    license='GPL',
    packages=['cli'],
    include_package_data=True,
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    python_requires='>=3.6',
    keywords='scalegrid database mongo redis mysql postgresql',
    entry_points={
        "console_scripts": [
            "sg-cli=cli.sg:main"
        ]
    }
)

