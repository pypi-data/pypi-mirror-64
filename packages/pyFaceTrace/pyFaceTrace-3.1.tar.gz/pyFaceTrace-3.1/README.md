���{��²��a���X
dllib
opencv
�����������ǲߪ��B�ͥi�H
�n²��a�ާ@�H�y����

    # ���ثewebcam�^���쪺�H�y�M���w�v���ɮרíp�⥦�̤������Z��
    im = captureImageFromCam()
    VTest = getFeatureVector(im)
    Vtrain = loadFeatureFromPic('train\\���귽.jpg')
    print(dist(VTest,Vtrain))
    
    #���Jtrain��Ƨ����Ҧ�jpg�ɤ��S�x��tag
    #�ê����w���ثewebcam�^���쪺�H�y������TAG
    loadDB(folder='train')
    result = predictFromDB(VTest)
    print(result)
    
    #vedio Demo
    loadDB(folder='train')
    predictCam()