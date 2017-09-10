import tkinter as tk
from Version1 import Task
from Version1 import *
from PIL import Image,ImageTk
import numpy as np
from tkinter.colorchooser import askcolor 
LARGE_FONT= ("Verdana", 12)
position_var =(0,100)
color_var = (250,0,0)
Obj = Task()
flag=0
Filters = {"Median":1,"Average":2,"Gaussian":3,"Median_Sharpen":4,"Canny":5,"AdaptiveThr":6}
class Photoshop(tk.Tk):
    def __init__(self, *args, **kwargs):  
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self, width="1324" , height="768",bd="5",bg="red")
        container.pack(side="top", fill="both", expand = True )
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (Load,test):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Load) 
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    
     
class Load(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        Left_frame = tk.Frame(self,width="1024",height="768",bd="5",bg="black")
        right_frame = tk.Frame(self,width="300",height="768",bd="5",bg="blue")
        Left_frame.pack(side="left",fill="both",expand=True)
        Left_frame.bind("Motion", self.OnMouseDown)
        right_frame.pack(side="right",fill="both")
        load_button = tk.Button(right_frame, text="Load Image",command=lambda:self.load(parent, controller,Left_frame,right_frame))
        self.put_image(load_button,0,1,"load.png")
        img = cv2.imread("p.png")
        img = cv2.resize(img,(1024,768))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(Left_frame,image=img)
        panel.img = img
        panel.grid(column=0,row=0,sticky="nsew") 
        #load_button.grid(row=0,column=1,sticky="nsew")
        
        
 
    def load(self, parent, controller,left_frame,right_frame):
        global Obj,Filters
        global flag
        Obj.Load()
        brightness_var = tk.IntVar()
        
        if  flag==0:
            fvar = tk.StringVar()
            kvar = tk.IntVar()
            
            fvar.set("Median")
            kvar.set(3)

            select_filter = tk.Label(right_frame,text="select Filter :").grid(row=1,column=0)
            filter_list = tk.OptionMenu(right_frame,fvar,*("Median","Average","Gaussian","Median_Sharpen","Canny","AdaptiveThr"))
            filter_list.grid(row=1,column=1)
            select_filter = tk.Label(right_frame,text="select Kernel :").grid(row=2,column=0)
            kernel = tk.OptionMenu(right_frame,kvar,*(3,5,9))
            kernel.grid(row=2,column=1)
            apply_filter = tk.Button(right_frame,width=10, text="apply",command=lambda:self.Do_Filters(parent, controller,left_frame,Filters[fvar.get()],kvar.get()))
            apply_filter.grid(row = 3 ,column=1)
            
            

            label1 = tk.Label(right_frame, text="Brightness : ")
            label1.grid(row=4,column=0)
            spin = tk.Scale(right_frame,variable=brightness_var)
            spin.grid(row=4,column=1)
            brightness_var.set(50)
            spin_b = tk.Button(right_frame,width=10, text="brightness",command=lambda:self.brightness(parent,controller,left_frame,brightness_var.get()))
            spin_b.grid(row=5,column=1)


            
            label2 = tk.Label(right_frame, text="Font size : ")
            label2.grid(row=6,column=0)
            spinbox = tk.Spinbox(right_frame, from_=1, to=12 )
            spinbox.grid(row=6,column=1)
            label3 = tk.Label(right_frame, text="Font Color : ").grid(row=7,column=0)
            tk.Button(right_frame,text='Select Color', command=lambda:self.getColor()).grid(row=7,column=1)
            write_label = tk.Label(right_frame, text="Write Text")
            write_label.grid(row=8,column=0)
            text_entry = tk.Entry(right_frame,bd =5)
            text_entry.grid(row=8,column=1)
            color_b = tk.Button(right_frame,text="write",width=10,command=lambda:self.write(parent,controller,left_frame,text_entry.get(),spinbox.get(),color_var))
            color_b.grid(row=9,column=1)


            label3 = tk.Label(right_frame, text="Threshold :"  )
            label3.grid(row=10,column=0)
            thresh_value = tk.Entry(right_frame,bd=5)
            thresh_value.grid(row=10,column=1)
            thresh_button = tk.Button(right_frame,text="Threshold",width=10,command=lambda:self.Threshold_img(parent,controller,left_frame,thresh_value.get()))
            thresh_button.grid(row=11,column=1)


            label3 = tk.Label(right_frame, text="Other Features" ,fg="black" ,bd="1" )
            label3.grid(row=12,column=1)
            stretch_button =  tk.Button(right_frame,text="stretch",command=lambda:self.stretch(parent,controller,left_frame))
            stretch_button.grid(row=13,column=1)
            undo_button = tk.Button(right_frame, text="Back",command=lambda:self.undoChanges(parent,controller,left_frame,right_frame))
            image = ImageTk.PhotoImage(file="0.png")
            undo_button.config(image=image)
            undo_button.image = image
            undo_button.grid(row=15,column=0,sticky="e",columnspan=2)
            forward_button = tk.Button(right_frame, text="forward",command=lambda:self.Forward(parent,controller,left_frame))
            image = ImageTk.PhotoImage(file="1.png",width=48,height=48)
            forward_button.config(image=image)
            forward_button.image = image
            forward_button.grid(row=15,column=1,columnspan=2,sticky="w")
           
            save_button = tk.Button(right_frame, text="Save",command=lambda:self.Save(parent,controller))
            save_button.grid(row=16,column=1)
            img = self.convert_array2image(Obj.IMAGE())
            Panel = tk.Label(left_frame ,image=img)
            Panel.img = img
            Panel.grid(column=0,row=0,sticky="nsew")
            Panel.bind("<1>", self.OnMouseDown)
            flag=1
        elif  flag > 0:
            for widget in left_frame.winfo_children():
                widget.destroy()
            img = Obj.IMAGE()
            img = self.convert_array2image(img)
            Panel = tk.Label(left_frame ,image=img)
            Panel.img = img
            Panel.grid(column=0,row=0,sticky="nsew")
            Panel.bind("<1>", self.OnMouseDown)

    def Do_Filters(self,parent,controller,left_frame,ftype,ksize):
        global Obj,new_image
        if  Obj.Filters(ftype,ksize):
            for widget in left_frame.winfo_children():
                widget.destroy()
            
        
            new_image = Obj.IMAGE()
            new_image = self.convert_array2image(new_image)
            panel = tk.Label(left_frame,image=new_image)
            panel.new_image = new_image
            panel.grid(column=0,row=0,sticky="nsew")
            panel.bind("<1>", self.OnMouseDown)
        

    def write(self, parent, controller,left_frame,text,size,color):
        global position_var,Obj,new_image
        if Obj.writing(text,size,color,position_var):
            for widget in left_frame.winfo_children():
                widget.destroy() 
            new_image = Obj.IMAGE()
            new_image = self.convert_array2image(new_image)
            panel = tk.Label(left_frame,image=new_image)
            panel.new_image = new_image
            panel.grid(column=0,row=0,sticky="nsew")
            panel.bind("<1>", self.OnMouseDown)


    def undoChanges(self, parent, controller,left_frame,right_frame):
        for widget in left_frame.winfo_children():
            widget.destroy()
        global Obj,flag
        if Obj.Size()>0:
            Obj.Undo()
            if Obj.Size()>0:
                new_image = Obj.IMAGE()
                new_image = self.convert_array2image(new_image)
                panel = tk.Label(left_frame,image=new_image)
                panel.new_image = new_image
                panel.grid(column=0,row=0,sticky="nsew")
                panel.bind("<1>", self.OnMouseDown)
            else:
                for widget in right_frame.winfo_children():
                    widget.destroy()
                load_button = tk.Button(right_frame, text="Load Image",command=lambda:self.load(parent, controller,left_frame,right_frame))
                self.put_image(load_button,0,1,"load.png")    
                img = cv2.imread("p.png")
                img = cv2.resize(img,(1024,768))
                img = self.convert_array2image(img)
                panel = tk.Label(left_frame,image=img)
                panel.img = img
                panel.grid(column=0,row=0,sticky="nsew")           
                flag=0
    def Forward(self,parent,controller,left_frame):
        for widget in left_frame.winfo_children():
            widget.destroy()
        global Obj,new_image
        Obj.Forward()
        new_image = Obj.IMAGE()
        new_image = self.convert_array2image(new_image)
        panel = tk.Label(left_frame,image=new_image)
        panel.new_image = new_image
        panel.grid(column=0,row=0,sticky="nsew")
        panel.bind("<1>", self.OnMouseDown)
                
           
    def brightness(self, parent, controller,left_frame,brightness):
        for widget in left_frame.winfo_children():
            widget.destroy()
        global Obj,new_image
        Obj.Brightness(brightness)
        new_image = Obj.IMAGE()
        new_image = self.convert_array2image(new_image)
        panel = tk.Label(left_frame,image=new_image)
        panel.new_image = new_image
        panel.grid(column=0,row=0,sticky="nsew")    
        panel.bind("<1>", self.OnMouseDown)
    
    def Save(self,parent,controller):
        global position_var
        global Obj
        chk=Obj.save()
        if chk:
            Obj.print_mssg('Notify','Save Succeded ^_^')
        
     
    def convert_array2image(self,image):
        height, width = image.shape[:2]
        if(height>768 and width>1024):
            image = cv2.resize(image,(1024,768))    
        elif(height > 768):
            image = cv2.resize(image,(width,768))
        elif(width > 1024):
            image = cv2.resize(image,(1024,height))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        return image    

    def Threshold_img(self,parent,controller,left_frame,value):
        if value.isdigit() and (float(value)>=0 and float(value)<=255):
            for widget in left_frame.winfo_children():
                widget.destroy()
            global Obj,new_image
            Obj.Threshold(float(value))
            new_image = Obj.IMAGE()
            new_image = self.convert_array2image(new_image)
            panel = tk.Label(left_frame,image=new_image)
            panel.new_image = new_image
            panel.grid(column=0,row=0,sticky="nsew")    
            panel.bind("<1>", self.OnMouseDown)
        else:
            Obj.print_mssg("Value Erroe","Threshold value must be integer value [0-255]")

    def stretch(self,parent,controller,left_frame):
        for widget in left_frame.winfo_children():
            widget.destroy()
        global Obj,new_image
        Obj.strech()
        new_image = Obj.IMAGE()
        new_image = self.convert_array2image(new_image)
        panel = tk.Label(left_frame,image=new_image)
        panel.new_image = new_image
        panel.grid(column=0,row=0,sticky="nsew") 
        panel.bind("<1>", self.OnMouseDown)
    def OnMouseDown(self, event):
        global position_var
        position_var = (event.x,event.y)


    def getColor(self):
        global color_var
        color = askcolor() 
        color_var =  color[0]

    def put_image(self,tkobject,row,col,path):
        image = ImageTk.PhotoImage(file=path)
        tkobject.config(image=image)
        tkobject.image = image
        tkobject.grid(row=row,column=col,sticky="ew",columnspan=1)


        

class test(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
    

app = Photoshop()
app.mainloop()