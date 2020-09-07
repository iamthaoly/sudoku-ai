from source.Sudoku.puzzle import extract_digit
from source.Sudoku.puzzle import find_puzzle
from source.Sudoku.backtracking import solve_sudoku_backtracking
from source.Sudoku.x_algo import solve_sudoku_X
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from keras.models import model_from_json
from sudoku import Sudoku
import numpy as np
import argparse
import imutils
import cv2
import os
import sys

def main():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model", default="data/MNIST_keras_CNN.h5", help="path to trained digit classifier")
    ap.add_argument("-i", "--image", default="images/1.jpg", help="path to input Sudoku puzzle image")
    ap.add_argument("-d", "--debug", type=int, default=-1, help="whether or not we are visualizing each step of the pipeline")
    args = vars(ap.parse_args())

    # load the digit classifier from disk
    print("[INFO] loading digit classifier...")
    model = load_model(args["model"])

    # load the input image from disk and resize it
    print("[INFO] processing image...")
    # try to load image
    try:
        image = cv2.imread(args["image"])
    except:
        print("Image does not exist.")
    image = imutils.resize(image, width=600)

    #find puzzle in image
    (puzzleImage, warped) = find_puzzle(image, debug=args["debug"] > 0)
    #initialize our 9x9 Sudoku board
    board = np.zeros((9, 9), dtype="int")

    # infer the location of each cell by dividing the warped image
    # into 9x9 grid
    stepX = warped.shape[1] // 9
    stepY = warped.shape[0] // 9

    # a list to store the (x, y)-coordinates of each cell location
    cellLocations = []

    for y in range(0, 9):
        row = []
        for x in range(0, 9):
            startX = x * stepX
            startY = y * stepY
            endX = (x + 1) * stepX
            endY = (y + 1) * stepY
            row.append((startX, startY, endX, endY))
            # crop the cell and extract the digit from the cell
            cell = warped[startY:endY, startX:endX]
            try: 
                digit = extract_digit(cell, debug=args["debug"] > 0)
            except:
                print("Unable to detect Sudoku puzzle in your image :(")
                return
            
            # verify digit is not empty
            if digit is not None:
                # resize to 28x28 pixels and prepare cell for classification
                roi = cv2.resize(digit, (28, 28))
                roi = roi.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
                # classify digit and update Sudoku board
                pred = model.predict(roi).argmax(axis=1)[0]
                board[y, x] = pred
        cellLocations.append(row)
    # copy for later use
    start_board = board.tolist()
    
    # Construct 
    print("[INFO] OCR'd Sudoku board: ")
    #board.tolist() => 2d list
    puzzle = Sudoku(3, 3, board=board.tolist())
    # puzzle.show()

    # Solve 
    print("[INFO] solving Sudoku puzzle...")
    size = (3, 3)
    solution = list(solve_sudoku_X(size, board.tolist()))[0]

    print(start_board)
    row_num = col_num = 0
    for (cellRow, boardRow) in zip(cellLocations, solution):
        for (box, digit) in zip(cellRow, boardRow):
            startX, startY, endX, endY = box

            textX = int((endX - startX) * 0.33)
            textY = int((endY - startY) * -0.2)
            textX += startX
            textY += endY

            #draw result only if cell is empty when initialized
            if start_board[row_num][col_num] == 0:
                cv2.putText(puzzleImage, str(digit), (textX, textY), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (16, 156, 27), 2)
            col_num += 1
        row_num += 1
        col_num = 0
    image_name = os.path.splitext(os.path.basename(args["image"]))[0]
    cv2.imshow("Sudoku result", puzzleImage)
    cv2.waitKey(0)
    cv2.imwrite("output/%s.png" % image_name, puzzleImage)
    
######## MAIN PROGRAM ########
if __name__ == "__main__":
    main()