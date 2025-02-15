import setuptools

def main():
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()

    setuptools.setup(
        name="xena-rfc-converter",
        description="Xena Python RFC Converter is a library for converting Xena's Windows desktop RFC test configurations to Xena Python RFC test configurations.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Leonard Yu",
        author_email="leonard.yu@teledyne.com",
        maintainer="Teledyne LeCroy Xena",
        maintainer_email="support@xenanetworks.com",
        url="https://github.com/xenanetworks/xena-python-rfc-converter",
        packages=setuptools.find_packages(),
        license='Apache 2.0',
        install_requires=["pydantic>=1.8.2", "datamodel-code-generator", "xena-driver"],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
        ],
        python_requires=">=3.8.9",
        include_package_data=True,
    )

if __name__ == '__main__':
    main()

