from control.ControlConexion import *
from control.configBd import *
from modelo.Rol import *
class ControlRol():
    def __init__(self,objRol):
        self.objRol=objRol
    def listar(self):
        arregloRoles = [] 
        msg="ok"
        comandoSql = "SELECT * FROM rol"
        objControlConexion = ControlConexion()
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0):         
                for fila in cursor:
                    objRol=Rol(0,"")
                    objRol.setId(fila[0])
                    objRol.setNombre(fila[1])
                    arregloRoles.append(objRol)
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
            print(msg)
        return arregloRoles
    
    def consultar(self):
        msg="ok"
        id= self.objRol.getId(); 
        comandoSql = "SELECT * FROM rol where id  = '{}'".format(id)
        objControlConexion = ControlConexion()
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0): 
                for fila in cursor:           
                    self.objRol.setId(fila[0])
                    self.objRol.setNombre(fila[1])
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
            print(msg)
        return self.objRol

    def guardar(self):
        msg = "ok"
        nom= self.objRol.getNombre() 
        comandoSql = "INSERT INTO rol(nombre) VALUES ('{}')".format(nom)
        objControlConexion =  ControlConexion()
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0):
                msg=objControlConexion.cerrarBd()
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
            print(msg)
        return msg

    def borrar(self):
        msg = "ok"
        id= self.objRol.getId() 
        comandoSql = "delete from rol where id='{}'".format(id)
        objControlConexion =  ControlConexion()
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0):
                msg=objControlConexion.cerrarBd()
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
            print(msg)
        return msg
    
    def modificar(self):
        msg = "ok"
        id= self.objRol.getId() 
        nom= self.objRol.getNombre()
        comandoSql = "update rol set nombre='{}' where id={}".format(nom,id)
        objControlConexion =  ControlConexion()
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0):
                msg=objControlConexion.cerrarBd()
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
            print(msg)
        return msg
