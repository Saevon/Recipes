''' Setup.py '''
import os
import re

import setuptools


def recursive_find(path, regex):
    ''' Recursively searches a directory for all files that have a filename '''
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            # Check that it matches our search
            if not re.match(regex, filename):
                continue

            yield os.path.join(dirpath, filename)


def load_text(file):
    ''' Load the readme file from disk '''
    with open(file, "r") as readme_file:
        long_description = readme_file.read()
    return long_description


# Load the requirements file from disk
def load_requirements(file):
    ''' Loads a requirement.txt file (which may have comments '''
    install_requirements = []
    with open(file, "r") as requirements_file:
        install_requirements = requirements_file.read().split('\n')

    install_requirements = [
        require for require in install_requirements
        # Don't include empty requires
        if require.strip() != ''
        # Also remove commented out requirements
        and not require.strip().startswith('#')
    ]

    return install_requirements


# setup.py --version
__version__ = FILL____VERSION


setuptools.setup(
    name=FILL____PACKAGE,
    version=__version__,

    author=FILL____AUTHOR,
    author_email=FILL____EMAIL,

    url=FILL____HOME_URL,
    description=FILL____SHORT_DESC,

    long_description=load_text('README.md'),
    long_description_content_type="text/markdown",
    license=load_text('LICENSE'),

    # You can specify python files directly (these are importable directly by name)
    # py_modules=[
    #     'module.py',
    # ],
    packages=setuptools.find_packages(
        exclude=['contrib', 'docs', 'tests', 'alembic'],
    ),
    # package_data={
    #     # Adds templates and such
    #     FILL____MODULE: recursive_find(FILL____DATA_DIR, r'.*\.j2'),
    # },

    scripts=[
        # 'scripts/my_script',
    ],

    # If you're an application, lock all your dependencies
    # Warning! you will need to have a MANIFEST.ini with `include requirements.txt`
    # install_requires=load_requirements('requirements.txt'),

    # if you're a library: use less strict versions
    # install_requires=[
    #     # e.g. Allow hotfixes
    #     # 'request ~= 3.5',
    # ],

    extras_require={
        # You can add
        # 'test': [
        #     'pytest',
        # ],
    },

    # Can we run this code from a zip? or does it need to real files inside itself
    # zip_save=False,

    classifiers=(
        # Python Versions Supported
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',

        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        # 'Topic :: Software Development :: Build Tools',
        # 'Topic :: Software Development :: Security',


        "Operating System :: OS Independent",

        # License
        'License :: OSI Approved :: MIT License',
        #'Public Domain',
    ),

)
