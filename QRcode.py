import pyqrcode

qr = pyqrcode.create('scanner')
qr.png('scanner.png',scale=7)
