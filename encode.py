from cv2 import cv2
import base64
import numpy as np


"""

def send():
    import cv2
    file=cv2.imread("cup2.jpeg")
    return file



img=send()
#print(img)
im1=base64.b64encode(img)

im2=base64.b64decode(im1)
decoded_img = np.fromstring(im2, dtype=np.uint8)
#decoded_img = decoded_img.reshape(img.shape)

print("decoded=",decoded_img)

with open('newpic.png', 'wb') as f:
    f.write(decoded_img)



image = open('cup2.jpeg', 'rb')
image_read = image.read()
image_64_encode = base64.encodestring(image_read)
image_64_decode = base64.decodestring(image_64_encode)
image_result = open('deer_decode.jpeg', 'wb')
image_result.write(image_64_decode)
image_result.close()
 # create a writable image and write the decoding result image_result.write(image_64_decode)
"""



def send():
    import base64
    import cv2
    image=open("captioned_image.png",'rb')
    image_read=image.read()
    enc_img=base64.encodestring(image_read)
    print(enc_img)
    return 


if __name__=='__main__':
    send()
