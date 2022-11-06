# WNI-2022
slace-capture.pyがRaspberry Pi上で継続的に動かしていたプログラムです。
picture-*.pyが適宜分析のために動かすプログラムです。
上記分析プログラムで1000枚おきにcsvファイルに保存し、merge-csvdata.pyで外れ値の削除と合成を行います。

### scale-capture.py
Raspberry Pi上でのカメラ認識にcv2、画像のアップロードにPyDrive2を使用しました。
指定秒数(10秒)おきにカメラの映像を.jpgに保存し、その保存した画像をGoogleDriveにアップロードするようにしています。
1枚撮影するごとにアップロードするので、安定動作のために撮影頻度を10秒としています。
実測値読みで、1サイクルが3-4秒程度で残りが待機時間です。
