import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dynamixel_python",
    version="0.0.1",
    packages=["dynamixel_python", "dynamixel_python.web_scraper"],
    package_dir={'': '.'},
    author="Rocco DiVerdi",
    description="python wrapper for the dynamixel sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3",
    install_requires=[
        'dynamixel_sdk',
    ],
    package_data={'dynamixel_python': ['control_tables', 'control_tables/*.json']},
    include_package_data=True,
)
