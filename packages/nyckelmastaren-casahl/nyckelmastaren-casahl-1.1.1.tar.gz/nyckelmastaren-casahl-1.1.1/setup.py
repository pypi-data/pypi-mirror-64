import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nyckelmastaren-casahl", # Replace with your own username
    version="1.1.1",
    author="Caspian Ahlberg",
    author_email="caspianahlberg@gmail.com",
    description="A fun retro adventure game.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CaspianA1/Nyckelmastaren",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent", # because of colors on the screen, and refresh rates (for the terminal) (or maybe just on bash)
    ],
    python_requires='>=3.7',
)
