from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'neoricalex',
    version = '0.0.1',
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages = ['nfdos'],
    entry_points = {
        'console_scripts': [
            'nfdos = nfdos.__main__:main'
        ]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Win32 (MS Windows)",
        "Framework :: Django CMS",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: Portuguese",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3.8",
        "Topic :: Education",
    ],
    )