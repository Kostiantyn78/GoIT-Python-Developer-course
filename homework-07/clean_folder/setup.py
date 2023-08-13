from setuptools import setup, find_namespace_packages


setup(
    name='clean',
    version='1.0.1',
    description='Sorts files by type (extension) by moving them to the associated folders',
    url='https://github.com/',
    author='Kostiantyn Horishnii',
    author_email='ksgorishniy@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['clean-folder=clean_folder.clean:main']}
)
