from PyQt5 import QtWidgets
import sys,os
import base64
import hashlib
import urllib.parse
import time,datetime
import qrcode
from PIL import Image

import Ui_untitled

class encryption(QtWidgets.QMainWindow,Ui_untitled.Ui_MainWindow):
    def __init__(self):
        super(encryption,self).__init__()
        self.setupUi(self)

    #加密/解密
    def encr_base64(self):
        if self.radioButton.isChecked():
            print('选中了base64加密')
            str_source = self.textBrowser.toPlainText()
            str_encr = base64.b64encode(str_source.encode('utf-8'))
            self.textBrowser_2.setHtml(str(str_encr,'utf-8'))
        elif self.radioButton_2.isChecked():
            print('选中了base64解密')
            str_source = self.textBrowser.toPlainText()
            str_encr = base64.b64decode(str_source)
            self.textBrowser_2.setHtml(str(str_encr,'utf-8'))
        elif self.radioButton_3.isChecked():
            print('选中了md5加密')
            str_source = self.textBrowser.toPlainText()
            str_encr = hashlib.md5(str_source.encode(encoding='UTF-8')).hexdigest()
            self.textBrowser_2.setHtml(str(str_encr))
        elif self.radioButton_4.isChecked():
            print('选中了urlencode')
            str_source = self.textBrowser.toPlainText()
            str_encr = urllib.parse.quote_plus(str(str_source))
            self.textBrowser_2.setHtml(str(str_encr))
        elif self.radioButton_5.isChecked():
            print('选中了urldecode')
            str_source = self.textBrowser.toPlainText()
            str_encr = urllib.parse.unquote(str(str_source))
            self.textBrowser_2.setHtml(str(str_encr))
        elif self.radioButton_6.isChecked():
            print('选中了日期转化时间戳')
            str_source = self.textBrowser.toPlainText()
            #检查有无时间
            try:
                timeArray = time.strptime(str_source, "%Y-%m-%d %H:%M:%S")
                timeStamp = int(time.mktime(timeArray))
                str_encr = urllib.parse.unquote(str(timeStamp))
                self.textBrowser_2.setHtml(str(str_encr))
            except Exception:
                self.textBrowser_2.setHtml("时间格式失败")
        elif self.radioButton_7.isChecked():
            print('选中了时间戳转化日期')
            str_source = self.textBrowser.toPlainText()
            timeArray = time.localtime(int(str_source))
            str_encr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            self.textBrowser_2.setHtml(str(str_encr))

    def tool(self):
        str_source = self.textBrowser_3.toPlainText()
        #获取二维码背景路径
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )
        qr.add_data(str_source)
        qr.make(fit=True)
        str_source5 = self.textBrowser_5.toPlainText()
        print(str_source5)
        #img = qr.make()
        img = qr.make_image(fill_color="green", back_color="white")
        img = img.convert("RGBA")
        if str_source5:
            try:
                icon = Image.open(str_source5)
                # 获取图片的宽高
                img_w, img_h = img.size
                # 参数设置logo的大小
                factor = 6
                size_w = int(img_w / factor)
                size_h = int(img_h / factor)
                icon_w, icon_h = icon.size
                if icon_w > size_w:
                    icon_w = size_w
                if icon_h > size_h:
                    icon_h = size_h
                # 重新设置logo的尺寸
                icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
                # 得到画图的x，y坐标，居中显示
                w = int((img_w - icon_w) / 2)
                h = int((img_h - icon_h) / 2)
                # 黏贴logo照
                img.paste(icon, (w, h), mask=None)
            except IOError:
                print("图片打开失败")
                # fo = open("log.txt","w")
                # fo.write("图片打开失败")
                # fo.close()
        #生成路径
        curpath = os.path.realpath(__file__)
        dirpath = os.path.dirname(curpath)
        png_name = int(time.time())
        isExists=os.path.exists(dirpath+"/img/")
        if not isExists:
            os.makedirs(dirpath+"/img/")
        img.save(str(dirpath)+"/img/"+str(png_name)+".png")
        path_img = "<img src=\""+str(str(dirpath)+"/img/"+str(png_name)+".png")+"\" height=\"200\" width=\"200\" text-align=\"center\" vertical-align=\"middle\" /> "
        self.textBrowser_4.setHtml(str(path_img))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_untitled.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    window = encryption()
    window.show()
    sys.exit(app.exec_())