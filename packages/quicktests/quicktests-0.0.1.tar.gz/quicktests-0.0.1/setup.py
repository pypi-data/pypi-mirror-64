import setuptools

setuptools.setup(
    name='quicktests',
    version='0.0.1',
    url='https://gitlab.com/Raspilot/quicktests',
    author='Fabian Becker',
    author_email='fab.becker@outlook.de',
    description='A library for python for easy testing.',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
