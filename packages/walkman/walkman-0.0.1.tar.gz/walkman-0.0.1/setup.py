import setuptools


def read_content(file: str) -> str:
    with open(file, 'r') as f:
        return f.read().strip()


setuptools.setup(
    name='walkman',
    version=read_content('version.txt'),
    author='Sergio Pedraza',
    author_email='sergio.uriel.ph@gmail.com',
    description='Walkman parsing utilities',
    long_description=read_content('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/bakasoft/walkman',
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    license='MIT',
    # See: https://pypi.org/classifiers/
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
