from setuptools import setup, setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='FHIR Patient Summary',
      version='0.9.6',
      install_requires=['datetime', 'FHIR-Parser==0.1.5', "docxtpl"],
      description='Create a FHIR patient summary document in docx or pdf format.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/nicford/FHIR-Patient-Summary',
      author='Nicolas Ford',
      author_email='zcabnjf@ucl.ac.uk',
      license='MIT',
      packages=setuptools.find_packages(),
      python_requires='>=3.7',
      zip_safe=False)