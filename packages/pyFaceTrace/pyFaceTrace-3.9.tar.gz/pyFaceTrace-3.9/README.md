# Author:KuoYuan Li

[![N|Solid](https://images2.imgbox.com/8f/03/gv0QnOdH_o.png)](https://sites.google.com/ms2.ccsh.tn.edu.tw/pclearn0915)


本程式簡單地結合dlib,opencv
讓不懂機器學習的朋友可以軟簡單地操作人臉辨識,
程式需另外安裝 dlib
dlib whl 安裝包下載網站： (https://reurl.cc/Y1OvEX)
  - 由於windows中dlib的whl檔只下載得到p36版本
  - 故本套工具只能在python3.6中運行
  - dlib whl 安裝包下載後必需由檔案離線安裝 (pip install ...)

##### Download the samples to 'train' folder(下載各種照片樣本至train資料夾)

```
downloadImageSamples()
```

##### 比對目前webcam擷取到的人臉和指定影像檔案並計算它們之間的距離

```
im = captureImageFromCam()
VTest = getFeatureVector(im)
Vtrain = loadFeatureFromPic('train\\李國源.jpg')
```

##### 載入train資料夾中所有jpg檔之特徵及tag並直接預測目前webcam擷取到的人臉對應的TAG
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

License
----

MIT


**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
