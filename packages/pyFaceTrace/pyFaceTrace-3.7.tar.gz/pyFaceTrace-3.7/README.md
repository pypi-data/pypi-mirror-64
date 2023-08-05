# Introduction

本程式簡單地結合 dlib 與 opencv,讓不懂機器學習的朋友可以軟簡單地操作人臉辨識,
由於windows中dlib的whl檔只下載得到p36版本,故本套工具只能在python3.6中運行

```
pip install pyFaceTrace
```

### download the samples to 'train' folder

```
downloadImageSamples()
```

### 比對目前webcam擷取到的人臉和指定影像檔案並計算它們之間的距離

```
im = captureImageFromCam()
VTest = getFeatureVector(im)
Vtrain = loadFeatureFromPic('train\\李國源.jpg')
print(dist(VTest,Vtrain))
```

### 載入train資料夾中所有jpg檔之特徵及tag並直接預測目前webcam擷取到的人臉對應的TAG

```
loadDB(folder='train')
result = predictFromDB(VTest)
print(result)
```

### Demo with webcam

```
loadDB(folder='train')
predictCam()
```

