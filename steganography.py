import cv2
import numpy as np

def to_bin(data):
    # Convert 'data' to binary format as string
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def encode(image_name, secret_data):
    # Read image
    image = cv2.imread(image_name)
    # Maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print(f'[*] Maximum bytes to encode: {n_bytes}')

    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need a bigger image.")
    
    print('[*] Encoding data...')

    # Add stopping delimiter
    secret_data += 'cru4g'
    data_index = 0

    # Covert data to binary
    binary_secret_data = to_bin(secret_data)
    # Size of data to hide
    data_len = len(binary_secret_data)

    for row in image:
        for pixel in row:
            # Convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # Modify LSB if there is still data
            if data_index < data_len:
                # LSB Red pixel
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # LSB Green pixel
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # LSB Blue pixel
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            # If data is encoded, break
            if data_index >= data_len:
                break
    
    return image

def decode(image_name):
    print('[+] Decoding...')
    # Read image
    image = cv2.imread(image_name)
    binary_data = ''

    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]

    # Split by 8-bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # Convert from bits to chars
    decoded_data = ''
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == 'cru4g':
            break
    
    return decoded_data[:-5]

if __name__ == '__main__':
    input_image = 'safe.png'
    output_image = 'steg.png'
    with open('encoded.py', 'r') as f:
        secret_data = f.read()
    
    # Encode the data into the image
    encoded_image = encode(image_name=input_image, secret_data=secret_data)
    # Save output image
    cv2.imwrite(output_image, encoded_image)

    # Decode the secret data from the image
    decoded_data = decode(output_image)
    print(f'[+] Decoded data: {decoded_data}')