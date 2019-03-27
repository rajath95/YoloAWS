
def send():
    import base64
    import cv2
    image=open("captioned_image.png",'rb')
    image_read=image.read()
    enc_img=base64.encodestring(image_read)
    print(enc_img)
    return enc_img
