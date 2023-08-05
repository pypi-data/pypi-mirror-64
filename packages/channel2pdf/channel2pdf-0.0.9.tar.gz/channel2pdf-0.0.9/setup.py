import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="channel2pdf",
    version="0.0.9",
    author="Yunzhi Gao",
    author_email="gaoyunzhi@gmail.com",
    description="Export Telegram Channel to PDF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaoyunzhi/channel2pdf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'bs4',
        'telegram_util>=0.0.30',
        'cached_url>=0.0.1',
        'pyyaml',
        'readee>=0.0.14'
    ],
    python_requires='>=3.0',
)