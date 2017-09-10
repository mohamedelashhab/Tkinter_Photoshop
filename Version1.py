from PIL import Image
from PIL import ImageTk
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox
import cv2
import numpy as np
import re
class Task():
    def __init__(self):
        self.img = []
        self.trash=[]
        self.brightness = []
        self.bright_trash =[]
        

    def Load(self):
        r_image = re.compile(r".*\.(jpg|png|gif|JPG|PNG|GIF|tiff|TIFF)$")
        while True:
            try:
                path = tkFileDialog.askopenfilename(initialdir = "/home/ashhab/.images")
                if not path:
                    break
                elif not r_image.match(path):
                    raise Exception("Select An Image") 
                image = cv2.imread(path)
                self.img.append(image)
                self.brightness.append(50)
                return True
            except Exception as error:
                self.print_mssg("File Type Error",error)
                
                


            


    def Filters(self,FilterType,Kernel):
        newImage = np.array(self.img[len(self.img)-1])
        if FilterType is 1:
            newImage = cv2.medianBlur(newImage,Kernel)
        elif FilterType is 2:
            Kernel = (Kernel,Kernel)
            newImage = cv2.blur(newImage,Kernel)
        elif FilterType is 3:
            newImage = cv2.GaussianBlur(newImage,(Kernel,Kernel),0)
        elif FilterType is 4:
            try:
                if Kernel is not 9:
                    raise Exception("Select 9 for Median sharpen")
            except Exception as error:
                    self.print_mssg("input",error)
                    return False
            else:
                sharp_kernel = np.array([[-1, -1, -1], [-1, Kernel, -1], [-1, -1, -1]])
                newImage = cv2.filter2D(newImage, -1, sharp_kernel)
                
        elif FilterType is 5:
            newImage = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
            newImage = cv2.Canny(newImage,100,200)
            newImage = cv2.cvtColor(newImage, cv2.COLOR_GRAY2BGR)
        elif FilterType is 6:
            newImage = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
            newImage = cv2.adaptiveThreshold(newImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
            newImage = cv2.cvtColor(newImage, cv2.COLOR_GRAY2BGR)

        self.img.append(newImage)
        self.brightness.append(self.brightness[len(self.brightness)-1])
        return True
  


    def Brightness(self,beta):
        if beta >= 0:
            newImage = np.array(self.img[len(self.img)-1])
            b,g,r = cv2.split(newImage)
            if beta > self.brightness[len(self.brightness)-1]:
                
                b,g,r = cv2.add(b,beta-self.brightness[len(self.brightness)-1]),cv2.add(g,beta-self.brightness[len(self.brightness)-1]),cv2.add(r,beta-self.brightness[len(self.brightness)-1])
            elif beta < self.brightness[len(self.brightness)-1]:
                
                
                b,g,r = cv2.subtract(b,self.brightness[len(self.brightness)-1] - beta),cv2.subtract(g,self.brightness[len(self.brightness)-1] - beta),cv2.subtract(r,self.brightness[len(self.brightness)-1] - beta)
            else:return
            newImage = cv2.merge((b,g,r)) 
            self.brightness.append(beta)    
            self.img.append(newImage)



    def writing(self,text,size,color,position):
        newImage = np.array(self.img[len(self.img)-1])
        try:
            size = int(size)
            if size > 12:
                size = 12
            font_thickness = 3
            cv2.putText(newImage,text,position,cv2.FONT_HERSHEY_SIMPLEX,size,color,font_thickness)
        except:
            self.print_mssg("Error","Write English alphabit or Select Write Font")
            return False
        else:
            self.img.append(newImage)
            self.brightness.append(self.brightness[len(self.brightness)-1])
            return True

        
    
    def save(self):
        chk = False
        while True:
            try:
                filename =  tkFileDialog.asksaveasfilename(initialdir = "/home/ashhab",title = "Select file",filetypes = (("jpg / png files",("*.jpg","*.png")),("all files","*.[jpeg tiff png jpg]"),("PNG","*.png"),("JPG","*.jpg")))
                expression = re.compile(r".*\.(jpg|png|gif|JPG|PNG|GIF|tiff|TIFF)$")
                if expression.match(filename):
                    image = self.img[self.Size()-1]
                    cv2.imwrite(filename, image)
                    chk=True
                    break
                else:
                    if not filename:
                        break
                    tkMessageBox.showinfo("error", "Not match with regular expression")  
            except:
                pass
                tkMessageBox.showinfo("error", "Not match with regular expression")
        return chk            


    def Threshold(self,value):
        newImage = np.array(self.img[len(self.img)-1])
        newImage = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
        newImage = cv2.cvtColor(newImage, cv2.COLOR_GRAY2BGR)
        retval, newImage = cv2.threshold(newImage, value, 255, cv2.THRESH_BINARY)  
        self.img.append(newImage)
        self.brightness.append(self.brightness[len(self.brightness)-1]) 


    def strech(self):
        newImage = self.img[self.Size()-1]
        newImage = cv2.resize(newImage,(1024,768))
        self.img.append(newImage)
        self.brightness.append(self.brightness[len(self.brightness)-1])
        
    def print_mssg(self,error,error_type):
        tkMessageBox.showinfo(error, error_type)
    
    def IMAGE(self):
        return self.img[len(self.img)-1]
    
    def Undo(self):
        image=self.img.pop()
        bright = self.brightness.pop()
        self.trash.append(image)
        self.bright_trash.append(bright)
    def Size(self):
        return len(self.img)
    def Forward(self):
        if len(self.trash)>0:
            image = self.trash.pop()
            bright = self.bright_trash.pop()
            self.img.append(image)
            self.brightness.append(bright)

