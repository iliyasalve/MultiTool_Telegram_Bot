import cv2

def read_qr_code(filename) -> str:
    '''
    The function receives and reads the image
    If there is a QR code on it, then the function returns the value encrypted in the QR code. 
    Otherwise the function returns -1
    '''
    
    img = cv2.imread(filename)
    detect = cv2.QRCodeDetector()
    retval, value, points, straight_qrcode = detect.detectAndDecodeMulti(img)
        
    if retval:
        return value[0]
    else:
        return "-1"
    

            
    '''
    try:
    
    except:
        return
    '''
