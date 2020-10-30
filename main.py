# import numpy as np
import cv2 as cv
import time
import sys

output = []
output_scale = 10
output_row = 48
output_column = 128
output_pixel_per_row = 0
output_pixel_per_column = 0

# symbols = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
symbols_short_raw = ' .:-=+*#%@'
symbols_short_reversed = [char for char in '@%#*+=-:. ']
symbols_short = [char for char in symbols_short_raw]

symbols = symbols_short

symbols_len = len(symbols)
symbols_range = []
for i in range(0, symbols_len):
    symbols_range.append(int((255/symbols_len)*(i+1)))

frame_width = 0
frame_height = 0

def adjustSymbolsRange():
    min_gray = 255
    max_gray = 0
    for i in range(0, frame_height):
        for j in range(0, frame_width):
            current = gray[i][j]
            if current < min_gray:
                min_gray = current
            if current > max_gray:
                max_gray = current

    gray_factor = (max_gray - min_gray + 1)/256

    symbols_range.clear()
    max_split = 255/symbols_len
    for i in range(0, symbols_len):
        factor = (i+1)*gray_factor + min_gray
        symbols_range.append(int(max_split*factor))


def getSymbolFromGray(gray_amount): # to change
    for i in range(0, symbols_len):
        if gray_amount <= symbols_range[i]:
            return symbols[i]

def getAvgGray(x, y, w, h):
    total_gray = 0
    for i in range(y, y + h):
        gray_line = gray[i]
        for j in range(x, x + w):
            total_gray += gray_line[j]
    return int(total_gray/output_pixel_square_size) # w*h ?

def toASCIIArt():
    adjustSymbolsRange()
    output = ""
    for i in range(0, output_row):
        y = i*output_pixel_per_row
        for j in range(0, output_column):
            output += getSymbolFromGray(
                getAvgGray(j*output_pixel_per_column, y, output_pixel_per_column, output_pixel_per_row)
            )
        output += '\n'

    print(output)

    for _ in range(output_row + 1):
        sys.stdout.write("\x1b[A")
    # print(output)



cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Frame to gray scale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # cv.flip(gray, 1)

    # Display the resulting frame
    # cv.imshow('frame', gray)

    frame_width = len(gray[0])
    frame_height = len(gray)
    output_pixel_per_row = int(frame_height/output_row)
    output_pixel_per_column = int(frame_width/output_column)
    output_pixel_square_size = output_pixel_per_row*output_pixel_per_column

    toASCIIArt()

    if cv.waitKey(20) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()