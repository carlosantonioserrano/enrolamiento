
from tkinter import *
from ventana import *


def main():
    root = Tk() #declaro la ventana
    root.wm_title("Sistema de Enrolamiento")
    app = Ventana(root) 
    app.mainloop()
    

if __name__ == "__main__":
    main()