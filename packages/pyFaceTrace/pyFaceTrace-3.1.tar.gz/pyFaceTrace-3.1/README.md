本程式簡單地結合
dllib
opencv
讓不懂機器學習的朋友可以
軟簡單地操作人臉辨識

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