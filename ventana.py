
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image #formatos de archivo JPG, JPEG o BMP
from countries import *
from tkinter import messagebox
import cv2
import mediapipe as mp # el "as" es un sobrenombre para no escribir el nombre largo
import os
import tkinter
import numpy as np # permite hacer operacione matemáticas
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN


class Ventana(Frame):
    
    paises = Countries()
        
    def __init__(self, master=None):
        super().__init__(master,width=810, height=560)
        self.master = master
        self.pack()
        self.create_widgets()
        self.llenaDatos()
        self.habilitarCajas("disabled")  
        self.habilitarBtnOper("normal")
        self.habilitarBtnGuardar("disabled")  
        self.id=-1
        self.abrir_imagen1()
        self.registro_facial()
        #self.limpiando_foto()

    def abrir_imagen1(self):
        #llama la imagen (solo para imagenes png en el mismo formulario)
        #img1 = PhotoImage(file="uees.png") # se carga la imagen png
        #lbl_img1=Label(self,image=img1).place(x=650, y=10, width=257, height=257) #incluir la imagen en la ventana
        
        # Para redimensionar
        img1=Image.open("uees.png")
        img1=img1.resize((150,150), Image.ANTIALIAS)
        
        img1=ImageTk.PhotoImage(img1)
        lbl_img1=Label(self,image=img1).place(x=650, y=10)
        
        mainloop()

    def llamando_foto(self):
        # declaracion de carpeta fotos almacenadas
        ruta = self.txtCapital.get()
        direccion = 'D:/Python/enrolamiento' # cambiamos la inclinacion de las plecas
        carpeta = direccion + '/' + ruta
                
        #llamando la foto del empleado
        img2=Image.open(carpeta + '/rostro_10.png')
        img2=img2.resize((250,230), Image.ANTIALIAS)
        
        img2=ImageTk.PhotoImage(img2)
        lbl_img2=Label(self,image=img2)
        lbl_img2.place(x=250, y=270)
        
        mainloop()

    #def limpiando_foto(self):
        #lbl_img2.place_forget()
        #lbl_img2.destroy()
        #mainloop()

    def habilitarCajas(self,estado):
        self.txtISO3.configure(state=estado)
        self.txtCapital.configure(state=estado)
        #self.txtCurrency.configure(state=estado)
        self.txtName.configure(state=estado)
        
    def habilitarBtnOper(self,estado):
        self.btnNuevo.configure(state=estado)                
        self.btnModificar.configure(state=estado)
        self.btnEliminar.configure(state=estado)
        
    def habilitarBtnGuardar(self,estado):
        self.btnGuardar.configure(state=estado)                
        self.btnCancelar.configure(state=estado) 
        self.btnTomar_Foto.configure(state=estado)               
        
    def limpiarCajas(self):
        self.txtCapital.delete(0,END)
        #self.txtCurrency.delete(0,END)
        self.txtISO3.delete(0,END)
        self.txtName.delete(0,END)
        
    def limpiaGrid(self):
        for item in self.grid.get_children():
            self.grid.delete(item)
                
    def llenaDatos(self):
        datos = self.paises.consulta_empleados()        
        for row in datos:            
            self.grid.insert("",END,text=row[0], values=(row[1],row[2], row[3],row[4]))
        
        if len(self.grid.get_children()) > 0:
            self.grid.selection_set( self.grid.get_children()[0] )
            
    def fNuevo(self):         
        self.habilitarCajas("normal")  
        self.habilitarBtnOper("disabled")
        self.habilitarBtnGuardar("normal")
        self.limpiarCajas()        
        self.txtISO3.focus()
    
    def fGuardar(self): 
        if self.id ==-1:       
            self.paises.inserta_pais(self.txtISO3.get(),self.txtName.get(),self.txtCapital.get())
            messagebox.showinfo("Insertar", 'Elemento insertado correctamente.')
        else:
            self.paises.modifica_pais(self.id,self.txtISO3.get(),self.txtName.get(),self.txtCapital.get())
            messagebox.showinfo("Modificar", 'Elemento modificado correctamente.')
            self.id = -1            
        self.limpiaGrid()
        self.llenaDatos() 
        self.limpiarCajas() 
        self.habilitarBtnGuardar("disabled")      
        self.habilitarBtnOper("normal")
        self.habilitarCajas("disabled")
        #self.limpiando_foto()
        

    def fModificar(self):        
        selected = self.grid.focus()                               
        clave = self.grid.item(selected,'text')        
        if clave == '':
            messagebox.showwarning("Modificar", 'Debes seleccionar un elemento.')            
        else:            
            self.id= clave  
            self.habilitarCajas("normal")                         
            valores = self.grid.item(selected,'values')
            self.limpiarCajas()            
            self.txtISO3.insert(0,valores[0])
            self.txtName.insert(0,valores[1])
            self.txtCapital.insert(0,valores[2])
            #self.txtCurrency.insert(0,valores[3])            
            self.habilitarBtnOper("disabled")
            self.habilitarBtnGuardar("normal")
            self.txtISO3.focus()
            self.llamando_foto()
                                        
    def fEliminar(self):
        selected = self.grid.focus()                               
        clave = self.grid.item(selected,'text')        
        if clave == '':
            messagebox.showwarning("Eliminar", 'Debes seleccionar un elemento.')            
        else:                           
            valores = self.grid.item(selected,'values')
            data = str(clave) + ", " + valores[0] + ", " + valores[1]
            r = messagebox.askquestion("Eliminar", "Deseas eliminar el registro seleccionado?\n" + data)            
            if r == messagebox.YES:
                n = self.paises.elimina_pais(clave)
                if n == 1:
                    messagebox.showinfo("Eliminar", 'Elemento eliminado correctamente.')
                    self.limpiaGrid()
                    self.llenaDatos()
                else:
                    messagebox.showwarning("Eliminar", 'No fue posible eliminar el elemento.')
                            
    def fCancelar(self):
        r = messagebox.askquestion("Calcelar", "Esta seguro que desea cancelar la operación actual")
        if r == messagebox.YES:
            self.limpiarCajas() 
            self.habilitarBtnGuardar("disabled")      
            self.habilitarBtnOper("normal")
            self.habilitarCajas("disabled")

    def fTomarFoto(self):
        print("Tomando la fotografia... espere unos segundos mientras se inicializa")
        # declaracion de carpeta fotos almacenadas
        ruta = self.txtCapital.get()
        #nombre = "User"
        direccion = 'D:/Python/enrolamiento' # cambiamos la inclinacion de las plecas
        carpeta = direccion + '/' + ruta

        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # declaramos valor inicio contador
        count = 1

        # declaramos el detector
        detector = mp.solutions.face_detection # en la pagina de mediapipe se ve la sentencia

        # el detector debe tener su herramienta de dibujo
        # creamos variable que almacenaremos herramienta de dibujo
        dibujo = mp.solutions.drawing_utils # aqui llamamos al mediapipe con el sobrenombre "mp"

        # hacemos la videocaptura
        cap = cv2.VideoCapture(0) # con el cero declaramos cuál webcam usar

        # inicializamos parámetros de la deteccion
        with detector.FaceDetection(min_detection_confidence = 0.75) as rostros:

            while True:
                # 1o leemos los fotogramas o frame
                ret, frame = cap.read() # ret lectura de fotogramas y frame los fotogramas

                # corrigiendo la colorimetría
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # deteccion de rostros
                resultado = rostros.process(rgb) # guardamos los rostros que se han detectado

                # creando filtro de seguridad
                if resultado.detections is not None:
                    for rostro in resultado.detections: # si encuentra rostros en los resultados...
                        #dibujo.draw_detection(frame, rostro, dibujo.DrawingSpec(color=(255,0,0))) #para puntos rojos #le entregamos la ventana frame
                        #print(rostro)

                        #for id, coordenadas in enumerate(resultado.detections):
                            # mostrar la coordenadas
                            #print("Coordenadas: ", resultado.detections)

                        # extrayendo la dimension de la imagen
                        al, an, c = frame.shape

                        # extrayendo "x" inicial y "y" inicial
                        xi = rostro.location_data.relative_bounding_box.xmin
                        yi = rostro.location_data.relative_bounding_box.ymin

                        # extrayendo ancho y alto
                        ancho = rostro.location_data.relative_bounding_box.width
                        alto = rostro.location_data.relative_bounding_box.height

                        # pasando a pixeles
                        xi = int(xi * an)
                        yi = int(yi * al)
                        ancho = int(ancho * an)
                        alto = int(alto * al)

                        # encontrando xfinal y yfinal
                        xf = xi + ancho
                        yf = yi + alto


                # guardando las fotos...
                cv2.imwrite(carpeta + "/rostro_{}.png".format(count), frame) # cont variable incremento
                count = count + 1

                # mostramos los fotogramas
                cv2.imshow("Presione la tecla ESC para tomar la foto", frame)

                # declaramos la tecla para finalizar el while
                t = cv2.waitKey(1)
                if t == 27 or count ==1: # leo el código ASCII teclado - si el contador menor a 30
                    break

        cap.release() # borramos la videocapturas
        cv2.destroyAllWindows() # cerramos todas las ventanas        

        #############################################################################

    def create_widgets(self):
        frame1 = Frame(self, bg="#bfdaff")
        frame1.place(x=0,y=0,width=93, height=259)        
        
        self.btnNuevo=Button(frame1,text="Nuevo", command=self.fNuevo, bg="blue", fg="white")
        self.btnNuevo.place(x=5,y=50,width=80, height=30 )        
        self.btnModificar=Button(frame1,text="Modificar", command=self.fModificar, bg="blue", fg="white")
        self.btnModificar.place(x=5,y=90,width=80, height=30)                
        self.btnEliminar=Button(frame1,text="Eliminar", command=self.fEliminar, bg="blue", fg="white")
        self.btnEliminar.place(x=5,y=130,width=80, height=30)
        self.btnTomar_Foto=Button(frame1,text="Tomar Foto", command=self.fTomarFoto, bg="blue", fg="white")
        self.btnTomar_Foto.place(x=5,y=170,width=90, height=30)   
        
        #############################################################################

        frame2 = Frame(self,bg="#d3dde3" )
        frame2.place(x=95,y=0,width=150, height=259)                        
        
        lbl1 = Label(frame2,text="Nombres:")
        lbl1.place(x=3,y=5)        
        #self.txtISO3=Entry(frame2,textvariable = self.ISO3)
        self.txtISO3=Entry(frame2)
        self.txtISO3.place(x=3,y=25,width=150, height=20)                
        
        lbl2 = Label(frame2,text="Apellidos:")
        lbl2.place(x=3,y=55)        
        self.txtName=Entry(frame2)
        self.txtName.place(x=3,y=75,width=150, height=20)        
        
        lbl3 = Label(frame2,text="DUI:")
        lbl3.place(x=3,y=105)        
        self.txtCapital=Entry(frame2)
        self.txtCapital.place(x=3,y=125,width=150, height=20)        
           
        self.btnGuardar=Button(frame2,text="Guardar", command=self.fGuardar, bg="green", fg="white")
        self.btnGuardar.place(x=10,y=210,width=60, height=30)
        self.btnCancelar=Button(frame2,text="Cancelar", command=self.fCancelar, bg="red", fg="white")
        self.btnCancelar.place(x=80,y=210,width=60, height=30)         
        
        #########################################################################################

        frame3 = Frame(self,bg="yellow" )
        frame3.place(x=247,y=0,width=420, height=259)                      
        
        self.grid = ttk.Treeview(frame3, columns=("col1","col2","col3","col4"))        
        self.grid.column("#0",width=60)
        self.grid.column("col1",width=70, anchor=CENTER)
        self.grid.column("col2",width=90, anchor=CENTER)
        self.grid.column("col3",width=90, anchor=CENTER)
        self.grid.column("col4",width=90, anchor=CENTER)        
        self.grid.heading("#0", text="Id", anchor=CENTER)
        self.grid.heading("col1", text="ISO3", anchor=CENTER)
        self.grid.heading("col2", text="Country Name", anchor=CENTER)
        self.grid.heading("col3", text="Capital", anchor=CENTER)
        self.grid.heading("col4", text="Currency Code", anchor=CENTER)                
        self.grid.pack(side=LEFT,fill = Y)        
        sb = Scrollbar(frame3, orient=VERTICAL)
        sb.pack(side=RIGHT, fill = Y)
        self.grid.config(yscrollcommand=sb.set)
        sb.config(command=self.grid.yview)
        self.grid['selectmode']='browse'

        #########################################################################################
