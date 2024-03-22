import streamlit as st
import os
import glob
import xmltodict
from astropy.io import fits

def create_xml(xml_name, survey_name, survey_path, xml_template_path):
    xml = xmltodict.parse(open(xml_template_path, 'r').read())

    xml['Survey']['ShortName'] = xml['Survey']['Name'] = survey_name
    xml['Survey']['FITS']['Images']['SpellPrefix'] = survey_path+'/'

    fit_files = glob.glob('{}/*.fit*'.format(survey_path))

    # Read first file to extract info
    hdul = fits.open(fit_files[0])

    scale = abs(hdul[0].header['CDELT1'])
    xml['Survey']['Settings']['Scale'] = '{:.8f}'.format(scale)
    suffix = ',Sin,J2000,{},{},{:},{:}'.format(hdul[0].data.shape[-1], hdul[0].data.shape[-2], scale, scale)
    xml['Survey']['FITS']['Images']['SpellSuffix'] = suffix

    images = []

    for im in fit_files:
        im_n = im.split('/')[-1]
        hdul = fits.open(im)
        cr1 = hdul[0].header['CRVAL1']
        cr2 = hdul[0].header['CRVAL2']
        images.append('{0},{0},{1:.4f},{2:.4f} {1:.4f} {2:.4f} 2019'.format(im_n, cr1, cr2))

    xml['Survey']['FITS']['Images']['Image'] = sorted(images)

    # Save XML file
    unpar = xmltodict.unparse(xml, pretty=True)
    f = open(xml_name, 'w')
    f.write(unpar)
    f.close()

def main():
    st.title("Sky XML Generator")

    survey_name = st.text_input("Survey Name")
    survey_path = st.text_input("Path to Survey Images")
    xml_template_path = "survey_template.xml"  # You can modify this if your template path is different

    if st.button("Generate XML"):
        if survey_name and survey_path:
            xml_name = os.path.join('.', f"{survey_name}.xml")
            create_xml(xml_name, survey_name, survey_path, xml_template_path)
            st.success(f"XML generated successfully: {xml_name}")
        else:
            st.error("Please provide both survey name and path to continue.")

if __name__ == "__main__":
    main()
