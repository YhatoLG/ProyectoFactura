from control.ControlConexion import *
from control.configBd import *
from modelo.Cliente import *
class ControlCliente():
    def __init__(self,objPersona=None,objCliente=None):
        self.objPersona=objPersona
        self.objCliente=objCliente
    
    def listar(self):
        arregloClientes = [] 
        msg="ok"
        comandoSql = "SELECT * FROM persona inner join cliente on cliente.fkcodpersona=persona.codigo"
        objControlConexion = ControlConexion()
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0):         
                for fila in cursor:
                    objCliente=Cliente(0)
                    objCliente.setCodigo(fila[0])
                    objCliente.setNombre(fila[1])
                    objCliente.setTelefono(fila[2])
                    objCliente.setEmail(fila[3])
                    objCliente.setcredito(fila[5])
                    arregloClientes.append(objCliente)
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
            print(msg)
        return arregloClientes
    
    def consultar(self, usua, passw, serv, port, bdat):
        msg = "ok"
        cod = self.objCliente.getCodigo()

        try:
            objControlConexion = ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)

            comandoSql = "SELECT * FROM persona INNER JOIN cliente ON cliente.fkcodpersona = persona.codigo WHERE codigo = '{}';".format(cod)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            if cursor.rowcount > 0:
                for fila in cursor:
                    self.objCliente = Cliente(0)
                    self.objCliente.setCodigo(fila[0])
                    self.objCliente.setNombre(fila[1])
                    self.objCliente.setTelefono(fila[2])
                    self.objCliente.setEmail(fila[3])
                    self.objCliente.setcredito(fila[5])

            objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)

        return self.objCliente


    def guardar(self): #
        msg = "ok"
        
        cod= self.objPersona.getCodigo() 
        nom= self.objPersona.getNombre()
        tel= self.objPersona.getTelefono() 
        ema= self.objPersona.getEmail()
        cre= self.objCliente.getCredito()
        
        try:
            
            objControlConexion =  ControlConexion()
            msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)

            comandoSql = "INSERT INTO persona(codigo,nombre,telefono,email) VALUES ('{}','{}','{}','{}')".format(cod,nom,tel,ema)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "INSERT INTO cliente(credito,fkcodpersona,fkcodempresa) VALUES ({},'{}',null)".format(cre,cod)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)
            
            if (cursor.rowcount> 0):
                msg=objControlConexion.cerrarBd()

        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
            print(msg)
            
        return msg

    def borrar(self): #hay que comentarlo xd
        cod = self.objPersona.getCodigo() 
        try:
            objControlConexion =  ControlConexion()
            msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)

            comandoSql = "BEGIN;"
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "DELETE FROM cliente WHERE fkcodpersona = '{}';".format(cod);
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "DELETE FROM persona WHERE codigo = '{}';".format(cod)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "END;"
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            if (cursor.rowcount> 0):
                msg=objControlConexion.cerrarBd()

        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
            print(msg)
        return msg
    
    def modificar(self):
        cod = self.objPersona.getCodigo()
        nom = self.objPersona.getNombre()
        tel = self.objPersona.getTelefono()
        ema = self.objPersona.getEmail()
        cre = self.objCliente.getCredito()

        try:
            objControlConexion = ControlConexion()
            msg = objControlConexion.abrirBd(usua, passw, serv, port, bdat)

            comandoSql = "INSERT INTO persona (codigo, nombre, telefono, email) VALUES ('{}', '{}', '{}', '{}') ON CONFLICT (codigo) DO UPDATE SET nombre = '{}', telefono = '{}', email = '{}'".format(cod, nom, tel, ema, nom, tel, ema)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            comandoSql = "INSERT INTO cliente (fkcodpersona, credito) VALUES ('{}', {}) ON CONFLICT (fkcodpersona) DO UPDATE SET credito = excluded.credito".format(cod, cre)
            cursor = objControlConexion.ejecutarComandoSql(comandoSql)

            if cursor.rowcount > 0:
                msg = objControlConexion.cerrarBd()
        except Exception as objException:
            msg = "Algo salió mal: {}".format(objException)
            print(msg)
        return msg


