import cv2
import subprocess
from io import BytesIO

def obfuscate(hide_file, in_file, out_file):
    _ = subprocess.run(f'pyminifier {hide_file} > tmp1.py', shell=True)
    _ = subprocess.run('pyminifier --obfuscate tmp1.py > tmp2.py', shell=True)
    _ = subprocess.run('cython -3 --embed -o tmp2.c tmp2.py', shell=True)
    _ = subprocess.run('gcc -v -Os -I /usr/include/python3.8 -L /usr/lib/python3.8 -o tmp2 tmp2.c -lpython3.8 -lpthread -lm -lutil -ldl', shell=True)
    _ = subprocess.run('zip tmp2.zip tmp2', shell=True)

    with open('tmp2.zip', 'rb') as f:
        secret_data = f.read()
    steg_image = encode(imgfile=in_file, data=secret_data, outfile=out_file)
    # cv2.imwrite(out_file, steg_image)

    _ = subprocess.run('rm tmp2.zip; rm tmp2; rm tmp2.c; rm tmp2.py; rm tmp1.py', shell=True)

def encode(imgfile, data, outfile):
    img_file = open(imgfile, 'rb')
    img_data = img_file.read()
    img_file.close()

    new_file = open(outfile, 'wb')
    new_file.write(img_data)
    new_file.write(data)
    new_file.close()

if __name__ == '__main__':
    pycode = input("What python code are we hiding? ")
    im_file_in = input("What image are we hiding it in? ")
    im_file_out = input("Where do you want the output saved? ")

    obfuscate(pycode, im_file_in, im_file_out)