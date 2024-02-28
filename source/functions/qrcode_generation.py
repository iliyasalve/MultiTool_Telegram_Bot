import qrcode
 
def qrcode_generation(data: str):
    '''
    Returns an image format qrcode.image.pil.PilImage
    '''
    
    return qrcode.make(data) #img.save('MyQRCode1.png')

