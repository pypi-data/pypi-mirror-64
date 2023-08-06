import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autolatex",
    version="0.1.3",
    author="Benature Wang",
    author_email="wbenature@163.com",
    description="Generate LaTeX code by Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Benature/AutoLaTeX",
    packages=setuptools.find_packages(),
    install_requires=['pandas'],
    entry_points={
        'console_scripts': [
            'autolatex=autolatex:excel2table'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

'''
python setup.py sdist bdist_wheel
pip install dist/autolatex-x.x.x.whl
'''
