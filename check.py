import pytesseract
path='media/images/a.jpeg'
print(pytesseract.image_to_string(path,lang='kan'))