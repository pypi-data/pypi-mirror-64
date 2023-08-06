import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="syncvtools",
    version="0.1.13",
    author="Aleksandr Patsekin",
    author_email="apatsekin@gmail.com",
    description="CV Tools related to Object Detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/apatsekin/cv-tools",
    #download_url='https://github.com/apatsekin/cv-tools/archive/0.1.tar.gz',
    install_requires=['opencv-python','lxml','Pillow', 'boto3','tqdm','pyyaml','scipy'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)