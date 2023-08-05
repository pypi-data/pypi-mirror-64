# coding:utf-8

from setuptools import setup
# or
# from distutils.core import setup  

setup(
        name='pyFaceTrace',   
        version='3.3',   
        description='easy Face Recognition fo python',   
        author='KuoYuan Li',  
        author_email='funny4875@gmail.com',  
        url='https://github.com/funny4875/pyFaceTrace.git',      
        packages=['pyFaceTrace'],   
        include_package_data=True,
        keywords = ['Face recognition', 'Face Trace'],   # Keywords that define your package best
          install_requires=[            # I get to this in a second
          'numpy',
          'scikit-image',
          'opencv-python',
          'request',
          'zipfile36',
          'bz2file'
          ],
      classifiers=[
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3.6',
      ],
)
