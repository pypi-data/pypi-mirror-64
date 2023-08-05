import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_trix-fork",
    version='0.3.2.0',
    packages=["trix"],
    include_package_data=True,
    description="Trix rich text editor widget for Django (Fork of https://github.com/tortillagroup/django-trix)",
    url="https://github.com/adityatelange/django-trix-fork",
    author="Jeremy Carbaugh, Aditya Telange",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms=["any"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
