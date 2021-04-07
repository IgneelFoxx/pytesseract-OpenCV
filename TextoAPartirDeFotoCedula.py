import cv2
import pytesseract
import re
import matplotlib.pyplot as plt

def ocr(image):
    custom_config = r'-l spa - psm 11'
    text = pytesseract.image_to_string(image, config=custom_config )
    return text

def main_process(path):
    img_color=cv2.imread(path) 
    img_gris=cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY) 
    thresh = cv2.threshold(img_gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,2)) 
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel,iterations=1) 
    invert = 255 - opening
    text=ocr(invert)
    frontal=re.findall('\w{2}-\w{3}-\w{4}', text)

    if len(frontal)>0: 
        try: 
            output={
                'Fecha de nacimiento': frontal[0],
                'Fecha expedicion': frontal[1]}
        except:  #En el caso que no logre identificar la fecha 
            output={
                'Fecha de nacimiento': 'DD-MMM-YYYY',
                'Fecha expedicion': 'DD-MMM-YYYY'         
            }
    else: 
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4)) 
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel,iterations=1) 
        invert = 255 - opening
        text=ocr(invert)
        number=re.findall('([0-9])',text)
        number_out=''.join(number)
        number_lines=text.splitlines()
        nombres=number_lines[8]
        apellidos=number_lines[5]
        output={
        'CC': number_out,
        'Nombres': nombres,
        'Apellidos': apellidos 
        }

    return output

path= str(input("nombres del archivo: (EJEMPLO: cedula.jpeg): "))
print(main_process(path))
