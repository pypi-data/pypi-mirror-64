from setuptools import setup
import os

DIRECTORY = os.path.dirname(__file__)
READ_ME = open(os.path.join(DIRECTORY, "README.rst")).read()


setup(name='flaskscaffold',
      version='0.8',
      url='https://github.com/karolosk/flask-scaffold',
      author='KarolosK',
      author_email='karolos.koutsoulelos@gmail.com',
      license='MIT',
      description=("Initializing project structure for flask applications."),
      long_description=READ_ME,
      long_description_content_type="text/x-rst",
      packages=['flaskscaffold'],
      zip_safe=False,
      include_package_data=True,
      scripts=['bin/flaskscaffold-create'])