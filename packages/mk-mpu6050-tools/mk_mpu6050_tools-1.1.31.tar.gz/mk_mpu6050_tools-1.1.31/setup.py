import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mk_mpu6050_tools",
    version="1.1.31",
    author="Mark Cartagena",
    author_email="mark@mknxgn.com",
    description="Mk MPU6050 Tool Kit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mknxgn.com/",
    install_requires=['mknxgn_essentials', 'requests'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
