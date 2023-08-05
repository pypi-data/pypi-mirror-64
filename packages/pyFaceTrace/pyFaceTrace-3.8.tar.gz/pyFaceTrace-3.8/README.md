# Author:KuoYuan Li

[![N|Solid](https://images2.imgbox.com/8f/03/gv0QnOdH_o.png)](https://sites.google.com/ms2.ccsh.tn.edu.tw/pclearn0915)


���{��²��a���Xdlib,opencv
�����������ǲߪ��B�ͥi�H�n²��a�ާ@�H�y����,
�{���ݥt�~�w�� dlib
dlib whl �w�˥]�U�������G (https://reurl.cc/Y1OvEX)
  - �ѩ�windows��dlib��whl�ɥu�U���o��p36����
  - �G���M�u��u��bpython3.6���B��
  - dlib whl �w�˥]�U���ᥲ�ݥ��ɮ����u�w�� (pip install ...)

##### Download the samples to 'train' folder(�U���U�طӤ��˥���train��Ƨ�)

```
downloadImageSamples()
```

##### ���ثewebcam�^���쪺�H�y�M���w�v���ɮרíp�⥦�̤������Z��

```
im = captureImageFromCam()
VTest = getFeatureVector(im)
Vtrain = loadFeatureFromPic('train\\���귽.jpg')
```

##### ���Jtrain��Ƨ����Ҧ�jpg�ɤ��S�x��tag�ê����w���ثewebcam�^���쪺�H�y������TAG
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
