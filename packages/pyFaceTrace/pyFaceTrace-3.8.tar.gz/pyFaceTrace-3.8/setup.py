# coding:utf-8

from setuptools import setup
# or
# from distutils.core import setup  
foruser = '''本程式簡單地結合dlib,opencv
讓不懂機器學習的朋友可以軟簡單地操作人臉辨識
由於windows中dlib的whl檔只下載得到p36版本
故本套工具只能在python3.6中運行
'''
setup(
        name='pyFaceTrace',   
        version='3.8',   
        description='easy Face Recognition fo python',
        long_description=foruser,
        author='KuoYuan Li',  
        author_email='funny4875@gmail.com',  
        url='https://pypi.org/project/pyFaceTrace',      
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
