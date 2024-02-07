import os
import glob
import argparse
import xmltodict

from astropy.io import fits

def create_xml(xml_name, survey_name, survey_path, xml_template_path):
  xml = xmltodict.parse(open(xml_template_path, 'r').read())

  xml['Survey']['ShortName'] = xml['Survey']['Name'] = survey_name
  xml['Survey']['FITS']['Images']['SpellPrefix'] = survey_path+'/'

  fit_files = glob.glob('{}/*.fit*'.format(survey_path))

  #read first file to extract info
  hdul = fits.open( fit_files[0] )

  scale = abs(hdul[0].header['CDELT1'])
  xml['Survey']['Settings']['Scale'] = '{:.8f}'.format(scale)
  suffix = ',Sin,J2000,{},{},{:},{:}'.format(hdul[0].data.shape[-1],hdul[0].data.shape[-2],scale,scale)
  xml['Survey']['FITS']['Images']['SpellSuffix'] = suffix

  images = []

  for im in fit_files:
      im_n = im.split('/')[-1]
      hdul = fits.open(im)
      cr1 = hdul[0].header['CRVAL1']
      cr2 = hdul[0].header['CRVAL2']
      images.append('{0},{0},{1:.4f},{2:.4f} {1:.4f} {2:.4f} 2019'.format(im_n, cr1, cr2))

  xml['Survey']['FITS']['Images']['Image'] = sorted(images)

  #save XML file
  unpar = xmltodict.unparse(xml, pretty=True)
  f = open(xml_name, 'w')
  f.write(unpar)
  f.close()

if __name__ == '__main__':
  try:
    xmlroot = os.environ['SKYVIEW_XMLROOT']
    print('Detected SKYVIEW_XMLROOT')
  except:
    xmlroot = '.'

  parser = argparse.ArgumentParser()
  parser.add_argument('--xmlroot',  default=xmlroot, help='Path to save XML, default $SKYVIEW_XMLROOT')
  parser.add_argument('--template', default='survey_template.xml', help='XML template file')
  parser.add_argument('--name',   help='Name for XML file. Defaults to survey name')
  parser.add_argument('--survey', required=True, help='Survey name')
  parser.add_argument('--path',   required=True, help='Path to survey images')
  args = parser.parse_args()
  if(args.name): 
    name = args.name
  else:
    name = args.survey
  out_xml = '{}/{}.xml'.format(args.xmlroot, name)
  print('Creating XML ', out_xml)
  create_xml( out_xml, args.survey, args.path, args.template)