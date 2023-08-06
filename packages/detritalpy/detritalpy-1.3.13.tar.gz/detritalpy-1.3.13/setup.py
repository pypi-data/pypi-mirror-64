import setuptools

with open('C:/Users/gsharman/Box/detritalPy/pip_installation/README.md', "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="detritalpy",
    packages=['detritalpy'],    
    version="1.3.13",
    author="Glenn Sharman",
    author_email="gsharman@uark.edu",
    description="A Python-based toolset for visualizing and analyzing detrital geo-thermochronologic data",
    keywords = 'detrital, zircon, provenance, stratigraphy, geochronology, thermochronology',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grsharman/detritalpy",
    scripts=['C:/Users/gsharman/Box/detritalPy/detritalPy/detritalPy.py',
            'C:/Users/gsharman/Box/detritalPy/detritalPy/detritalPy.py',
            'C:/Users/gsharman/Box/detritalPy/detritalPy/detritalPy.py'],
    install_requires=['numpy','matplotlib','pandas','xlrd','folium','vincent','simplekml',
        'scipy','sklearn','statsmodels','peakutils'],
    classifiers=[
        "Programming Language :: Python :: 3",
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
