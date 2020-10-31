import cv2 as cv
import sys

class Output:
    row = 48
    column = 128
    pixel_per_row = 0
    pixel_per_column = 0
    pixel_square_size = 0

class Frame:
    data = []
    w = 0
    h = 0

class Symbols:
    def __init__(self, category):
        symbols = ""
        if category == 'raw':
            symbols = ' .:-=+*#%@'
        elif category == 'reversed':
            symbols = '@%#*+=-:. '

        self.data = [char for char in symbols]
        self.step = 255/len(self.data)

output = Output()
frame = Frame()
symbols = Symbols('raw')

def frameToGray(frame_data):
    return cv.cvtColor(frame_data, cv.COLOR_BGR2GRAY)

def getSymbolFromGray(gray_amount):
    return symbols.data[int(gray_amount/symbols.step)]

def getAvgGray(x, y, w, h):
    total_gray = 0
    gray = frame.data
    for i in range(y, y + h):
        gray_line = gray[i]
        for j in range(x, x + w):
            total_gray += gray_line[j]
    return int(total_gray/output.pixel_square_size)

def toASCII():
    ascii_frame = ""
    for i in range(0, output.row):
        y = i*output.pixel_per_row
        for j in range(0, output.column):
            x = j*output.pixel_per_column
            ascii_frame += getSymbolFromGray(
                getAvgGray(x, y, output.pixel_per_column, output.pixel_per_row)
            )
        ascii_frame += '\n'

    print(ascii_frame)

    for _ in range(output.row + 1):
        sys.stdout.write("\x1b[A")

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame.data = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame.data = frameToGray(frame.data)

    # cv.flip(gray, 1)
    # cv.imshow('frame', gray) # Display the webcam frames

    frame.w = len(frame.data[0])
    frame.h = len(frame.data)

    output.pixel_per_row = int(frame.h/output.row)
    output.pixel_per_column = int(frame.w/output.column)
    output.pixel_square_size = output.pixel_per_row*output.pixel_per_column

    toASCII()

    if cv.waitKey(20) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()