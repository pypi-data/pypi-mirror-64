import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CanvasPlus",
    version="1.1.0-a",
    author="Luke Zhang",
    author_email="luke.zhang2004@gmail.com",
    description="Improved Canvas widget for tkinter with more functionality to display graphical elements like lines or text. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Luke-zhang-04/CanvasPlus",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Tcl",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.3',
)