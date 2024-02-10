import string
from secrets import choice

import pyperclip
# PIL module is used to extract
# pixels of image and modify it
from PIL import Image

from fetchImage import fetchImage


def generatePassword(max_length=16):
    # Contains A-Z, a-z, 0-9, and !"#$%&\'()*+,-./;<=>?@[\\]^_`{|}~
    # We remove colon since we use that as our username separator
    char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation.replace(":","")
    # use secrets.choice to make generated password cryptographically secure
    # requires python 3.6 +
    return ''.join([choice(char_set) for _ in range(max_length)])

# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):
    # list of binary codes
    # of given data
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd


# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(starting_x, starting_y, w, img, data):
    # Get our data to store as a list of binary values
    # Default password generation becomes a list of 16 binary numbers
    datalist = genData(data)
    lendata = len(datalist)
    (x, y) = (starting_x, starting_y)
    (x1, y1) = update_x_y_coords(x, y, w)
    (x2, y2) = update_x_y_coords(x1, y1, w)


    for i in range(lendata):
        # 'i' references the current letter of our password
        # Extracting 3 pixels at a time
        # This gives us 9 values (3 rgb per pixel) to alter to mask our transmission
        # The 9th pixel will determine whether we keep reading data in the decode function
        pix = list(img.getpixel((x, y)) + img.getpixel((x1, y1)) + img.getpixel((x2, y2)))
        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            # 'j' references the bit location
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                # data_bit = 0, encoded bit must be an even number
                # pix[j] % 2 != 0 implies that the pixel value isn't even
                # subtracting 1 will make it an even number as well as maintain almost no perceptual difference
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                # data_bit = 1, encoded bit must be an odd number
                # pix[j] % 2 ==0 implies that the pixel value isn't odd or is 0 (0 % 2 = 0)
                if (pix[j] != 0):
                    pix[j] -= 1
                else:
                    # if the pixel RGB value is 0, add don't subtract (no negative numbers)
                    pix[j] += 1

        # Last pixel of every set tells
        # whether to stop or read further.
        # 0 means keep reading; 1 means the
        # message is over.
        if (i == lendata - 1):
            # We have encoded all our data
            if (pix[-1] % 2 == 0):
                if (pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    if pix[-1] == 255:
                        pix[-1] -= 2
                    else:
                        pix[-1] += 1

        else:
            # We have finished this letter
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        (x, y) = update_x_y_coords(x2, y2, w)
        (x1, y1) = update_x_y_coords(x, y, w)
        (x2, y2) = update_x_y_coords(x1, y1, w)
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode_enc(newimg, data, starting_pos):
    w = newimg.size[0]
    (x, y) = (starting_pos, starting_pos)
    for pixel in modPix(x, y, w, newimg, data):
        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        (x, y) = update_x_y_coords(x, y, w)


# Encode data into image
def encode():
    file_name = input("What app/site is this password for: ")
    user_name = input("Enter your login username for this app/site: ")
    password = generatePassword(16)
    print(f"Generated Password: {password}")
    remake_password = input("Do you want to use this password? y/n: ")
    while not remake_password.lower() == "y":
        password = generatePassword(8)
        print(f"Generated Password: {password}")
        remake_password = input("Do you want to use this password? y/n: ")
    pyperclip.copy(password)
    print(f"\n\nPassword copied to clipboard!\n\n")
    starting_pos = int(input("Input the starting coordinate for the data: "))
    print(f"Fetching Random Image...")
    image = fetchImage(return_in_memory=True)
    print(f"Encoding username/password into image...")
    data = f"{user_name}:{password}"
    encode_enc(image, data, starting_pos)
    # jpeg's are lossy and compression messes with decoding. Default to pngs
    new_img_extension = "png"
    new_img_path = f"passwords/{file_name}.{new_img_extension}"

    image.save(new_img_path, "PNG")

    print(f"You're password has been saved: {new_img_path}")
    print("Displaying you're password!")
    image.show()


def update_x_y_coords(x, y, w):
    if (x == w - 1):
        return [0, y+1]
    else:
        return [x+1, y]

# Decode the data in the image
def decode():
    # ['00110001', '00110010', '00110011', '00110100', '00110101', '00110110', '00110111', '00111000']
    img = input("Enter the website/app to retrieve the password: ")
    img_path = f"passwords/{img}.png"
    image = Image.open(img_path, 'r')
    w = image.size[0]
    starting_pos = int(input("Input the starting coordinate for the data: "))

    (x, y) = (starting_pos, starting_pos)
    (x1, y1) = update_x_y_coords(x, y, w)
    (x2, y2) = update_x_y_coords(x1, y1, w)

    data = ''

    while (True):
        pixels = list(
            image.getpixel((x, y)) +
            image.getpixel((x1, y1)) +
            image.getpixel((x2, y2))
        )
        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

        # Update to use new coords
        (x, y) = update_x_y_coords(x2, y2, w)
        (x1, y1) = update_x_y_coords(x, y, w)
        (x2, y2) = update_x_y_coords(x1, y1, w)


# Main Function
def main():
    a = int(input("Plum's Password Steganography\n"
                  "1. Encode\n2. Decode\n"))
    if (a == 1):
        encode()

    elif (a == 2):
        result_info = decode()
        username, password = result_info.split(":")
        print(f"Username: {username}")
        print(f"Password: {password}")
        pyperclip.copy(password)
        print(f"\n\nPassword copied to clipboard!\n\n")
    else:
        raise Exception("Enter correct input")


if __name__ == '__main__':
    main()