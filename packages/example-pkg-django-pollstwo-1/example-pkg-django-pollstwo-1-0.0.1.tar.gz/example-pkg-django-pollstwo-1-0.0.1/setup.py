import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-django-pollstwo-1",  # Replace with your own username
    version="0.0.1",
    author="Lin Hai",
    author_email="177060606@qq.com",
    description="A Django app to conduct Web-based polls.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bbsddn2020/django-pollstwo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)