import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Django CustomUser Model',
    version='1.0.5',
    author="Anthony C. Emmanuel",
    author_email="mymi14s@hotmail.com",
    description="Django custom user model app and django allauth for authentication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.ghorz.com/blog/Apps/2020-03-20/21/django-custom-user-model-app-and-django-allauth/",
    packages=["user_app"],
    # include_additional_files=True,
    # entry_points = {
    #     "console_scripts": ['aogl = aogl.aogl:main']
    # },
    install_requires=[
        "django-allauth",
        "django-bootstrap4"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
