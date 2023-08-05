# coding:utf-8
from setuptools import setup
# or
# from distutils.core import setup
userguide = '''
    # 比對目前webcam擷取到的人臉和指定影像檔案並計算它們之間的距離
    im = captureImageFromCam()
    VTest = getFeatureVector(im)
    Vtrain = loadFeatureFromPic('train\\李國源.jpg')
    print(dist(VTest,Vtrain))
    
    #載入train資料夾中所有jpg檔之特徵及tag
    #並直接預測目前webcam擷取到的人臉對應的TAG
    loadDB(folder='train')
    result = predictFromDB(VTest)
    print(result)
    
    #vedio Demo
    loadDB(folder='train')
    predictCam()
'''
#print(userguide)
setup(
        name='pyFaceTrace',   
        version='3.1',   
        license='MIT',
        description='easy Face Recognition fo python',
        long_description=userguide,
        author='KuoYuan Li',  
        author_email='funny4875@gmail.com',  
        url='https://github.com/funny4875/pyFaceTrace.git',      
        packages=['pyFaceTrace'],
        install_requires=['numpy','scikit-image'], #opencv-python and dlib should install by user individually
        keywords = ['face recognition', 'face trace', 'face feature extraction'],
        include_package_data=True,
        classifiers = [
                # 发展时期,常见的如下
                #   3 - Alpha
                #   4 - Beta
                #   5 - Production/Stable
                'Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',# 开发的目标用户
                'Topic :: Software Development :: Build Tools',# 属于什么类型
                'License :: OSI Approved :: MIT License',# 许可证信息
                # 目标 Python 版本
                'Programming Language :: Python :: 3.6'
            ]
)

