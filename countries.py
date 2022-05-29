import mysql.connector

class Countries:

    def __init__(self):
        #self.cnn = mysql.connector.connect(host="localhost", user="root", 
        #passwd="", database="bdEjemploPy")
        self.conn = mysql.connector.connect(user='root', password='Pass123', host='localhost', database='empresa', port='3306')

    def __str__(self):
        datos=self.consulta_paises()        
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux
        
    def consulta_empleados(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM empleados")
        datos = cur.fetchall()
        cur.close()    
        return datos

    def buscar_pais(self, Id):
        cur = self.conn.cursor()
        sql= "SELECT * FROM empleados WHERE Id = {}".format(Id)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()    
        return datos
    
    def inserta_pais(self,nombres, apellidos, dui):
        cur = self.conn.cursor()
        sql='''INSERT INTO empleados (nombres, apellidos, dui) 
        VALUES('{}', '{}', '{}')'''.format(nombres, apellidos, dui)
        cur.execute(sql)
        n=cur.rowcount
        self.conn.commit()    
        cur.close()
        return n    

    def elimina_pais(self,id):
        cur = self.conn.cursor()
        sql='''DELETE FROM empleados WHERE id_empleado = {}'''.format(id)
        cur.execute(sql)
        n=cur.rowcount
        self.conn.commit()    
        cur.close()
        return n   

    def modifica_pais(self, id, nombres, apellidos, dui):
        cur = self.conn.cursor()
        sql='''UPDATE empleados SET nombres='{}', apellidos='{}', dui='{}' WHERE id_empleado={}'''.format(nombres, apellidos, dui, id)
        cur.execute(sql)
        n=cur.rowcount
        self.conn.commit()    
        cur.close()
        return n   
