import setuptools
setuptools.setup(
        name = "CommandWinPy",
        version ="0.0.1.0",
        author = "Kudokuro",
        author_email="nguyentranphucbao@gmail.com",
        descryption = "Excute shell commands with python",
        long_descryption = "CommandWinPy :)",
        long_descryption_content_type = "text/markdown",
        url = "https://github.com/nguyentranphucbao/CommandWinPy",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.7.1',
)
