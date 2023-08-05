import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="secure-aiohttp",
    version="0.0.22",
    author="Danil Pekarchuk",
    author_email="danilopekarchuk321@gmail.com",
    description="aiohttp additional security layer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pinlast/secure-aiohttp",
    packages=setuptools.find_packages(),
    classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: AsyncIO',
      ],
    python_requires='>=3.5',
    license='Apache 2',
)
