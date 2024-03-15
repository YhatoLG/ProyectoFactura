from flask import Blueprint,render_template,session,redirect,url_for,request
import math
import markupsafe

from modelo.Rol import *
from control.ControlRol import *
from modelo.Usuario import *
from control.ControlUsuario import *
from modelo.RolUsuario import *
from control.ControlRolUsuario import *

vistaUsuarios=Blueprint("vistaUsuarios",__name__,static_folder="static",template_folder="templates")

@vistaUsuarios.route("/vistaUsuarios",methods = ['GET', 'POST'])
@vistaUsuarios.route("/")
def vista_Usuarios():

    arregloUsuarios=[]
    usuario = {
    'email': '',
    'contrasena': ''
    }
    if 'ema' in session:
        ema=session['ema']
        permisoParaEntrar=False
        matRolesDelUsuario = session.get('matRolesDelUsuario', [])
        i=0
        while i < len(matRolesDelUsuario):
            if matRolesDelUsuario[i][1] == "admin":
                permisoParaEntrar = True
            i+=1
        if permisoParaEntrar==False:
            print("ema=",ema)
            return render_template('menu.html',ema=ema)
    else:
        return redirect('/index')  
    msg="ok"
    objControlUsuario=ControlUsuario(None)
    arregloUsuarios=objControlUsuario.listar() 
   
    itemsxpagina=5
    totalItems=len(arregloUsuarios)
    numPaginas=math.ceil(totalItems/itemsxpagina)
    
    paginaActiva = request.args.get('paginaActiva')
    if paginaActiva==None: paginaActiva='1'            
    posInicial=(int(paginaActiva)-1)*itemsxpagina
    posFinal=posInicial+itemsxpagina
    if posFinal>totalItems: posFinal=totalItems
    rango=range(posInicial,posFinal)
    itemsMostrados=len(rango)
    itemsCombo2=[5,10,20,30,50,100,200,1]
    paginacion={
        "itemsxpagina":itemsxpagina,
        "totalItems":totalItems,
        "numPaginas":numPaginas,
        "paginaActiva":paginaActiva,
        "posInicial":posInicial,
        "rango":rango,
        "itemsMostrados":itemsMostrados,
        "itemsCombo2":itemsCombo2
        }

    
    objControlRol=ControlRol(None)
    arregloRoles=objControlRol.listar()
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        bt=markupsafe.escape(request.form.get('bt'))
        ema=markupsafe.escape(request.form['txtEmail'])
        con=markupsafe.escape(request.form['txtContrasena']) 
        ListBox1=request.form.getlist('ListBox1')
        cheks = request.form.getlist('options[]')
        combo2=request.form.get('combo2')                           
        usuario = {
            'email': ema,
            'contrasena': con
        }
        if bt=='Guardar':
            try:
                objUsuario= Usuario(ema,con)
                objControlUsuario= ControlUsuario(objUsuario)
                objControlUsuario.guardar()
                arregloRolUsuario=[]
                if len(ListBox1) != 0:
                    for i in range(len(ListBox1)):
                        id = ListBox1[i].split(";")[0]
                        objRolUsuario = RolUsuario(ema, id)
                        objControlRolUsuario = ControlRolUsuario(objRolUsuario)
                        objControlRolUsuario.guardar() #Guarda los datos de las claves foráneas en la tabla intermedia tblrol_usuario
                else:
                    id=5 #id=5 es invitado
                    objRolUsuario = RolUsuario(ema, id)
                    arregloRolUsuario[0] = objRolUsuario
                    objControlRolUsuario = ControlRolUsuario(objRolUsuario)
                    objControlRolUsuario.guardar()           
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaUsuarios')			          
        elif bt=='Consultar':
            try:
                objUsuario=  Usuario(ema,"");
                objControlUsuario= ControlUsuario(objUsuario);
                objUsuario=objControlUsuario.consultarPor('email',ema)
                ema=objUsuario.getEmail()
                con=objUsuario.getContrasena()
                objRolUsuario = RolUsuario(ema, 0)
                objControlRolUsuario = ControlRolUsuario(objRolUsuario)
                matRolesDelUsuario = objControlRolUsuario.consultarRoles_por_EmailUsuario()
                if matRolesDelUsuario==None:
                    matRolesDelUsuario=[[5,'invitado']]
                usuario = {
                    'email': ema,
                    'contrasena': con
                }                 
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
                print(msg)
            #return render_template('/vistaUsuarios.html',arregloUsuarios=arregloUsuarios,usuario=usuario,matRolesDelUsuario=matRolesDelUsuario,arregloRoles=arregloRoles,paginacion=paginacion)
        elif bt=='Modificar':
            try:
                #modifica en la tabla Usuario
                #nota: Para esto debería hacerse en un procedimiento almacenado con manejo de transacciones
			    #1. modifica en la tabla Usuario
                objUsuario= Usuario(ema,con)
                objControlUsuario= ControlUsuario(objUsuario)
                objControlUsuario.modificar()
                #2. borra los registros asociados del usuario en la tabla intermedia
                objRolUsuario = RolUsuario(ema, 0)
                objControlRolUsuario = ControlRolUsuario(objRolUsuario)
                objControlRolUsuario.borrarTodosEmailUsuario()
                #3. guarda de nuevo en la tabla intermedia
                arregloRolUsuario=[]
                if len(ListBox1) != 0:
                    i=0
                    while i < len(ListBox1):
                        id = ListBox1[i].split(";")[0]
                        objRolUsuario = RolUsuario(ema, id)
                        objControlRolUsuario = ControlRolUsuario(objRolUsuario)
                        objControlRolUsuario.guardar() #Guarda los datos de las claves foráneas en la tabla intermedia tblrol_usuario
                        i+=1
                else:
                    objRolUsuario = RolUsuario(ema, 1)
                    arregloRolUsuario[0] = objRolUsuario
                    objControlRolUsuario = ControlRolUsuario(objRolUsuario)
                    objControlRolUsuario.guardar() #Guarda los datos de las claves foráneas en la tabla intermedia tblrol_usuario

            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
                print(msg)
            return redirect('/vistaUsuarios')			
        elif bt=='Borrar':
            try:
                objUsuario=  Usuario(ema,"")
                objControlUsuario= ControlUsuario(objUsuario)
                #en este caso considero que está bien aplicar ON DELETE CASCADE 
		        #al contraint de clave foránea con_fkEmail de la tabla rol_usuario
                objControlUsuario.borrar()
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaUsuarios')
        elif bt=='BorrarVarios':
            try:
                for posicion in cheks:               
                    ema=arregloUsuarios[int(posicion)].getEmail()
                    objUsuario=  Usuario(ema,"")
                    objControlUsuario= ControlUsuario(objUsuario)
                    #en este caso considero que está bien aplicar ON DELETE CASCADE 
                    #al contraint de clave foránea con_fkEmail de la tabla rol_usuario
                    objControlUsuario.borrar()
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaUsuarios')			                                
    return render_template('/vistaUsuarios.html',ema=ema,arregloUsuarios=arregloUsuarios,usuario=usuario,matRolesDelUsuario=matRolesDelUsuario,arregloRoles=arregloRoles,paginacion=paginacion)

