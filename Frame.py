'''
Created on Mar 30, 2019

@author: Jiaming
'''
import tkinter as tk
from PIL import Image
from WordCard import WordCard
import numpy as np
from pynput.mouse import Controller, Button
from trained_model import CNN
import threading





        
def to_drawing_board(frame):
    object_list = {0:"Apple", 1:"Banana", 2:"Bus", 3:"Fish"}
    for widget in frame.winfo_children():
        widget.destroy()
    lines_info = []
    frame_canvas = tk.Frame(frame)
    frame_buttons = tk.Frame(frame)

        

    def draw_line(event):
        
        canvas.create_oval(event.x-LINE_LENTH, event.y-LINE_LENTH, event.x+LINE_LENTH, event.y+LINE_LENTH, fill="black")
        if event.x<400 and event.x>=0 and event.y<400 and event.y>=0:
            
            lines_info.append((event.x, event.y))
    
    
        
        
    def clear_canvas(canvas):
        canvas.delete("all")
        lines_info.clear()
        
    
    LINE_LENTH = 2
    exp = None
    pre = None
    def creat_label():       
        obj_index = np.random.randint(0, 4)
        obj = object_list[obj_index]
        
        text = """
        Could You Draw a(an) %s 
        """%(obj)
        global exp
        exp = obj
        lb = tk.Label(frame_canvas, text=text)
        lb.pack(side="top")
        return lb
    
    lb = creat_label()
    canvas = tk.Canvas(frame_canvas, bg="white", cursor="circle", width=400, height=400)
    canvas.pack(side="bottom")
    canvas.bind("<B1-Motion>", draw_line)
    
    frame_canvas.pack(side="top")
    frame_buttons.pack(side="bottom")
    

    tk.Button(frame_buttons, text="Submit!", command= lambda: create_image_matrix(lines_info, lb)).pack(side="right", padx=100)
    tk.Button(frame_buttons, text="Clear Canvas", command= lambda: clear_canvas(canvas)).pack(side="left", padx=100)
   
    def create_image_matrix(lines_info, lb):
        
        def renew_label(lb, predic_name):
            global pre
            pre = predic_name
            global exp
            flag = pre == exp
            obj_index = np.random.randint(0, 4)
            obj = object_list[obj_index]
            while obj == predic_name:
                obj_index = np.random.randint(0, 4)
                obj = object_list[obj_index]
            if flag:    
                text = """
                You Got the Correct Answer! %s,  Could You Draw a(an) %s? 
                """%(predic_name, obj)
            else:
                text = """
                Sadly, Your Paint More Likes, %s, Try It Again, Could You Draw a(an) %s? 
                """%(predic_name, obj)
            lb.configure(text=text)
            lb.update()
            exp = obj
        out_put = np.zeros((400, 400))
        
        def fill_out(point):
            x = point[1]
            y = point[0]
            out_put[x, y] = 255
            r = 3
            for i in range(x-r, x+r+1):
                for j in range(y-r, y+r+1):
                    if i>0 and i<400 and j>0 and j<400:
                        out_put[i, j] = 255
                
        for point in lines_info:
            fill_out(point)
            
        for i in range(out_put.shape[0]):
            for j in range(out_put.shape[1]):
                if out_put[i, j]==0:
                    out_put[i, j]=255
                else:
                    out_put[i, j]=0
            
        out_put = Image.fromarray(out_put).convert("L")
        out_put.resize((256, 256), Image.ANTIALIAS)
        n = np.random.randint(0, 1000)
        image_name = "Images/output"+str(n)+".png"
        out_put.save(image_name)
        global modelrre
        predic_name = CNN(image_name,model)
        
        renew_label(lb, predic_name)
        clear_canvas(canvas)
        
        
        
def mimic_mouse():
    import serial
    serialport = serial.Serial("/dev/serial0", 115200, timeout=1)
    def get_v(x, y, v=3):
        dx=0
        dy=0
        if x>700:
            dy=v
        if x<300:
            dy = -v
        if y>700:
            dx=-v
        if y<300:
            dx=+v
        return (dx, dy)
    
    def parse_info(str):
        #print(str)
        try:
            info = str.split(" ")
            x = eval(info[0].split("'")[1].split(',')[0])
            y = eval(info[1].split(",")[0])
            button = eval(info[2][0])
            return (x, y, button)
        except:
            return None
                 
    mouse = Controller()
    
    while True:
        info = parse_info(str(serialport.readline()))
        if info!=None:
            c_p= (info[0], info[1])
            button = info[2]
            if button == 1:
                mouse.press(Button.left)
            else:
                mouse.release(Button.left)
            v=get_v(c_p[0], c_p[1])
            dx = v[0]
            dy = v[1]
            mouse.move(dx, dy)
            
        else:
            pass    
        
    
def destroy_win(t, root):
    t.join()
    root.destroy()
    
if __name__ == "__main__":
    from keras.models import load_model
    model = load_model("mymodel.h5")
    t=threading.Thread(target = mimic_mouse)
    t.start()
    root = tk.Tk()
    root.title("Drawing and Learning")
    root.geometry("600x500")
    
    cards_frame = tk.Frame(root)
    
    app = WordCard("apple", "Images/apple.jpg", 0)
    ban = WordCard("banana", "Images/banana.jpg", 1)
    bus = WordCard("bus", "Images/bus.jpg", 2)
    fis = WordCard("fish", "Images/fish.jpg", 3)
    
    frame_pictures = tk.Frame(cards_frame)
    frame_button = tk.Frame(cards_frame)
    frame_left = tk.Frame(frame_pictures)
    tk.Label(frame_left, image = app.image).pack(side="top", ipadx = 30)
    tk.Label(frame_left, text= app.name).pack(side="top")
    tk.Label(frame_left, image = bus.image).pack(side="top", ipadx = 30)
    tk.Label(frame_left, text= bus.name).pack(side="top")
    frame_left.pack(side="left")
    
    frame_right = tk.Frame(frame_pictures)
    tk.Label(frame_right, image = ban.image).pack(side="top", ipadx = 30)
    tk.Label(frame_right, text= ban.name).pack(side="top")
    tk.Label(frame_right, image = fis.image).pack(side="top", ipadx = 30)
    tk.Label(frame_right, text= fis.name).pack(side="top")
    frame_right.pack(side="right")
    frame_pictures.pack(side="top")
    frame_button.pack(side="bottom")
    tk.Button(frame_button, text="Ready to draw", command=lambda:to_drawing_board(cards_frame)).pack(side="bottom")
    cards_frame.pack()
    root.protocol('WM_DELETE_WINDOW', lambda:destroy_win(t, root))
    root.mainloop()

    