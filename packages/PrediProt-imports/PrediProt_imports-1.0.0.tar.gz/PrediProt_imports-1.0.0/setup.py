from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name = 'PrediProt_imports',
    version = '1.0.0',
    description = 'Additional files for PrediProt',
    long_description = readme(),
    long_description_content_type = 'text/markdown',
    author = 'The Dream Team',
    license = 'GPL',
    packages = ['prediprot_imports'],
    install_requires = ['Bio'],
    include_package_data=True,
    zip_safe=False)
