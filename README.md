# SUDOKU AI
Sudoku solver using OpenCV, Tensorflow/Keras and algorithm X.

## Demo
Want to impress your friends? You came to the right place ;)
![Demo](image.jpg)

## How to use?
### First clone this repo
```

git clone https://github.com/iamthaoly/sudoku-ai.git
```
- **Open the directory you had cloned in command line** 
 
### Install requirements
```
pip install -r requirements.txt
```

### Quick start with a sample image
```
python solve.py
```
### Solve your own puzzle
- **Copy your image to images folder**
```
python solve.py --image images/image_file_name.jpg
```
Tada! Solved puzzle has been saved at output folder.
## Todo
- [x] Save solved puzzle with custom name
- [x] No puzzle bug fix
- [ ] Webcam support

## References
- OpenCV Sudoku Solver and OCR: https://www.pyimagesearch.com/2020/08/10/opencv-sudoku-solver-and-ocr/
- Knuth's Dancing Links paper: https://arxiv.org/pdf/cs/0011047.pdf
- Algorithm X using dictionaries in Python: https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
- Analysis of Sudoku Solving Algorithms: http://www.enggjournals.com/ijet/docs/IJET17-09-03-043.pdf