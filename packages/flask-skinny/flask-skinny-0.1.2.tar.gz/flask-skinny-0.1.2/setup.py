from os import path
from setuptools import setup


this_dir = path.abspath(path.dirname(__file__))
with open(path.join(this_dir, "README.md")) as f:
    long_description = f.read()


setup(
    name="flask-skinny",
    version="0.1.2",
    description="A Flask extension that forces extremely skinny controllers.",
    url="https://github.com/iwamot/flask-skinny/",
    license="MIT",
    author="Takashi Iwamoto",
    author_email="hello@iwamot.com",
    packages=["flask_skinny"],
    install_requires=["Flask"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
)
