���{��²��a���X
dlib
opencv
�����������ǲߪ��B�ͥi�H�n²��a�ާ@�H�y����
Note:
�ѩ�windows ��dlib��whl�ɥu�U���o�� p36����
�G���M�u��u��b python3.6���B��
==============================================
�H�U��²�檺�ϥΤ�k�G

    #download the samples to 'train' folder
    downloadImageSamples()
#==================================================    
    # ���ثewebcam�^���쪺�H�y�M���w�v���ɮרíp�⥦�̤������Z��
    im = captureImageFromCam()
    VTest = getFeatureVector(im)
    Vtrain = loadFeatureFromPic('train\\���귽.jpg')
    print(dist(VTest,Vtrain))
#==================================================    
    #���Jtrain��Ƨ����Ҧ�jpg�ɤ��S�x��tag
    #�ê����w���ثewebcam�^���쪺�H�y������TAG
    loadDB(folder='train')
    result = predictFromDB(VTest)
    print(result)
#==================================================    
    # Demo with webcam
    loadDB(folder='train')
    predictCam()