import psycopg2
class ControlConexion():
    def __init__(self):
        self.conn=None
        self.cursor = None
        self.listaConsulta=None
        self.mensaje="ok"
    def abrirBd(self,user,password,host,port,db):
        try:
            self.conn =  psycopg2.connect(
                host=host, 
                database=db, 
                user=user, 
                password=password, 
                port=port)
            self.cursor = self.conn.cursor()
        except psycopg2.Error as objError:
                self.mensaje=objError.pgerror
                print(objError.pgerror)
        return self.mensaje
    
    def cerrarBd(self):
        try:
            #self.cursor.close()
            self.conn.close()
        except psycopg2.Error as objError:
                self.mensaje=objError.pgerror
                print(objError.pgerror)
        return self.mensaje
    
    def ejecutarComandoSql(self,comandoSql):
        try:
            self.cursor.execute(comandoSql)
            self.conn.commit()
        except psycopg2.Error as objError:
                self.mensaje=objError.pgerror
                print(objError.pgerror)
        return  self.cursor
    def ejecutarComandoSql2(self, comandoSql, variables=None):
        try:
            self.cursor.execute(comandoSql, variables)
            self.conn.commit()
        except psycopg2.Error as objError:
            self.mensaje = objError.pgerror
            print(objError.pgerror)
        return self.cursor
