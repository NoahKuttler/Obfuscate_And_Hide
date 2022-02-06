import cv2
import subprocess
from steganography import encode

def obfuscate(hide_file, in_file, out_file):
    _ = subprocess.run(f'pyminifier {hide_file} > tmp1.py', shell=True)
    _ = subprocess.run(f'pyminifier --obfuscate tmp1.py > tmp2.py', shell=True)

    with open('tmp2.py', 'r') as f:
        secret_data = f.read()
    steg_image = encode(image_name=in_file, secret_data=secret_data)
    cv2.imwrite(out_file, steg_image)

    _ = subprocess.run('rm tmp2.py; rm tmp1.py', shell=True)

if __name__ == '__main__':
    pycode = input("What python code are we hiding? ")
    im_file_in = input("What image are we hiding it in? ")
    im_file_out = input("Where do you want the output saved? ")

    obfuscate(pycode, im_file_in, im_file_out)