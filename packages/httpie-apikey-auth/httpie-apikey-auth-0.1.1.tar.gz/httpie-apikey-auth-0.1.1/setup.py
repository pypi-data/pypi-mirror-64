from httpie_apikey_auth import __version__
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='httpie-apikey-auth',
    description='Elastic ApiKey plugin for HTTPie.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=__version__,
    author='Derek Ditch',
    author_email='dcode@rocknsm.io',
    license='MIT',
    url='https://github.com/dcode/httpie-apikey-auth',
    download_url='https://github.com/dcode/httpie-apikey-auth',
    py_modules=['httpie_apikey_auth'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_apikey_auth = httpie_apikey_auth:ApiKeyPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.7.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
