本程式簡單地結合
dlib
opencv
讓不懂機器學習的朋友可以軟簡單地操作人臉辨識
Note:
由於windows 中dlib的whl檔只下載得到 p36版本
故本套工具只能在 python3.6中運行
==============================================
以下為簡單的使用方法：

    #download the samples to 'train' folder
    downloadImageSamples()
#==================================================    
    # 比對目前webcam擷取到的人臉和指定影像檔案並計算它們之間的距離
    im = captureImageFromCam()
    VTest = getFeatureVector(im)
    Vtrain = loadFeatureFromPic('train\\李國源.jpg')
    print(dist(VTest,Vtrain))
#==================================================    
    #載入train資料夾中所有jpg檔之特徵及tag
    #並直接預測目前webcam擷取到的人臉對應的TAG
    loadDB(folder='train')
    result = predictFromDB(VTest)
    print(result)
#==================================================    
    # Demo with webcam
    loadDB(folder='train')
    predictCam()