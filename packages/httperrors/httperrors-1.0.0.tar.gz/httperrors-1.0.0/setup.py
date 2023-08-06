import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="httperrors",
    version="1.0.0",
    author="Lautaro Navarro",
    author_email="navarro_lautaro@hotmail.com",
    description='Library that provides a easy to use set of http errors along with useful descriptions',  # noqa
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/LautaroNavarro/httperrors',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
  ],
    python_requires='>=3.0',
)
