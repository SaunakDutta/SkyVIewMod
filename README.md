# skyviewmods

This repo contains a new ImageFactory class for [skyview-in-a-Jar](https://skyview.gsfc.nasa.gov/jar/jar.html) and a Python3 script for creating XML survey files for Skyview.

## How to Use

### Modifying skyview-in-a-Jar

```bash
mkdir -p skyview/skyview/survey/                    # make directory for skyview_jar
cp LocalImageFactory.class skyview/skyview/survey/  # copy file
jar uf path_to_skyview/skyview.jar -C skyview/   skyview/survey/LocalImageFactory.class
```

### Running the Python script

You'll fisrt need to intall some dependencies using either `pip` , `conda` or some other Python package manager.

***
#### PIP

```
pip3 install --user astropy xmltodict
```

#### Conda
```
conda install astropy xmltodict

```
***

You can run `python3 sky_xml.py -h` to view all the available options or just run :

```
python3 sky_xml.py --survey=survey_name --path=/path_to_survey_images
```
to create a simple XML.
