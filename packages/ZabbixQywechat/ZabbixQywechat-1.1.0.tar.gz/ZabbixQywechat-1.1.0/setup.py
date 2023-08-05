import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ZabbixQywechat", # Replace with your own username
    version="1.1.0",
    author="mike",
    author_email="441616837@qq.com",
    description="This is a package for sending messages to enterprise WeChat applications in zabbix",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikecui426/ZabbixQywechat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6',
)
