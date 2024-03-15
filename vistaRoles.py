from flask import Blueprint,render_template,session,redirect,request
import markupsafe
import math

from modelo.Rol import *
from control.ControlRol import *

vistaRoles=Blueprint("vistaRoles",__name__,static_folder="static",template_folder="templates")

@vistaRoles.route("/vistaRoles",methods = ['GET', 'POST'])
@vistaRoles.route("/")

def vista_Roles():
    arregloRoles=[]
    rol = {
    'id': 0,
    'nombre': ''
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
            return render_template('menu.html',ema=ema)
    else:
        return redirect('/')  
    msg="ok"
    objControlRol=ControlRol(None)
    arregloRoles=objControlRol.listar()
    itemsxpagina=5
    totalItems=len(arregloRoles)
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

    if request.method == 'GET':
        pass
    if request.method == 'POST':
        bt=markupsafe.escape(request.form.get('bt'))
        id=markupsafe.escape(request.form['txtId'])
        nom=markupsafe.escape(request.form['txtNombre'])
        btnMsg=markupsafe.escape(request.form.get('btnMsg'))
        cheks = request.form.getlist('options[]')
        combo2=request.form.get('combo2')                            
        rol = {
            'id': id,
            'nombre': nom
        }
        if bt=='Guardar':
            try:
                objRol= Rol(id,nom)
                objControlRol= ControlRol(objRol)
                objControlRol.guardar()        
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaRoles')		          
        elif bt=='Consultar':
            try:
                print("Entró a Consultar")
                objRol=Rol(id,0);
                objControlRol= ControlRol(objRol)
                objRol=objControlRol.consultar()
                id=objRol.getId()
                nom=objRol.getNombre()
                rol = {
                    'id': id,
                    'nombre': nom
                }                 
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
                print(msg)
        elif bt=='Modificar':
            try:
                objRol= Rol(id,nom)
                objControlRol= ControlRol(objRol)
                objControlRol.modificar()        
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaRoles')	
        elif bt=='Borrar':
            try:
                objRol= Rol(id,'')
                objControlRol= ControlRol(objRol)
                objControlRol.borrar()        
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaRoles')	
        elif bt=='BorrarVarios':
            try:
                for posicion in cheks:               
                    id=arregloRoles[int(posicion)].getId()
                    objRol=  Rol(id,"")
                    objControlRol= ControlRol(objRol)
                    objControlRol.borrar()
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaRoles')	 
    return render_template('/vistaRoles.html',ema=ema,arregloRoles=arregloRoles,rol=rol,paginacion=paginacion)

