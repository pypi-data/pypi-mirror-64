import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='loggerly',
    version='0.0.1',
    author='Parker Duckworth',
    description='Logger superclass with Loggly integration',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    license='Proprietary',
    install_requires=[
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'schedule'
    ],
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False
)
