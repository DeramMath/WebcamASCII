import cv2 as cv
import sys
import signal
from os import system, name

def clear():
    # for windows
    if name == 'nt':
        system('cls')
    # for mac & linux
    else:
        system('clear')

# called on ctrl+c
def signal_handler(signal, frame):
    clear()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class Output:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.pixel_per_row = 0
        self.pixel_per_column = 0
        self.pixel_square_size = 0

class Frame:
    data = []
    w = 0
    h = 0

class Symbols:
    def __init__(self, reverse):
        self.data = [char for char in ' .:-=+*#%@']
        if reverse:
            self.data.reverse()

        self.step = 255/len(self.data)

class Args:
    row = 48
    column = 128
    reverse = False
    flip = False

args = Args()

for i in range(1, len(sys.argv)):
    arg = sys.argv[i]
    try:
        arg = int(arg)

        # Get next arg
        i += 1
        arg2 = int(sys.argv[i])

        args.row = arg
        args.column = arg2
    except:
        if arg == 'reverse':
            args.reverse = True
        elif arg == 'flip':
            args.flip = True

output = Output(args.row, args.column)
frame = Frame()
symbols = Symbols(args.reverse)

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

    # Move the console cursor up to rewrite on the output
    for _ in range(output.row + 1):
        sys.stdout.write("\x1b[A")

def setValues():
    frame.w = len(frame.data[0])
    frame.h = len(frame.data)

    output.pixel_per_row = int(frame.h/output.row)
    output.pixel_per_column = int(frame.w/output.column)
    output.pixel_square_size = output.pixel_per_row*output.pixel_per_column

capture = cv.VideoCapture(0)
if not capture.isOpened():
    print("Cannot open camera")
    exit()
    
clear()

first_iteration = True

while True:
    # Capture frame-by-frame
    ret, frame.data = capture.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame.data = frameToGray(frame.data)

    if args.flip:
        frame.data = cv.flip(frame.data, 1)
        
    # Display the webcam frames
    # cv.imshow('frame', gray)

    # Webcam dimensions will never change
    if first_iteration:
        setValues()
        first_iteration = False

    toASCII()

clear()
capture.release()
cv.destroyAllWindows()