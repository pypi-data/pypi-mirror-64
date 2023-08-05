from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='aiohttp_google_auth_backend',
    version='0.5.1',
    packages=['aiohttp_google_auth_backend'],
    url='https://github.com/ketanbshah/aiohttp_google_auth_backend',
    license='GPL-3.0-only',
    author='Ketan B Shah, JyotiStar Inc',
    author_email='shahketanb@gmail.com',
    description='Asyncio wrapper for verify_token method in google-auth library for backend usage',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.8',
)
