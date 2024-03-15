from flask import Blueprint,render_template,session,redirect,request
import markupsafe
import math

from modelo.Persona import Persona
from modelo.Cliente import Cliente
from control.ControlCliente import ControlCliente



vistaClientes=Blueprint("vistaClientes",__name__,static_folder="static",template_folder="templates")

@vistaClientes.route("/vistaClientes",methods = ['GET', 'POST'])
@vistaClientes.route("/")

def vista_Clientes():
    arregloClientes=[]
    cliente = {
    'codigo': '',
    'nombre': '',
    'telefono':'',
    'email':'',
    'credito':0
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
    objControlCliente=ControlCliente(None)
    arregloClientes=objControlCliente.listar()
    itemsxpagina=5
    totalItems=len(arregloClientes)
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
        cod=markupsafe.escape(request.form['txtCodigo'])
        nom=markupsafe.escape(request.form['txtNombre'])
        tel=markupsafe.escape(request.form['txtTelefono'])
        ema=markupsafe.escape(request.form['txtEmail'])
        cre=markupsafe.escape(request.form['txtCredito'])
        btnMsg=markupsafe.escape(request.form.get('btnMsg'))
        cheks = request.form.getlist('options[]')
        combo2=request.form.get('combo2')                            
        cliente = {
        'codigo': cod,
        'nombre': nom,
        'telefono':tel,
        'email':ema,
        'credito':cre
        }
        if bt=='Guardar':
            try:
                objPersona= Persona(cod,nom,tel,ema)
                objCliente= Cliente(cre)
                objControlCliente= ControlCliente(objPersona,objCliente)
                objControlCliente.guardar()        
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaClientes')		          
        elif bt=='Consultar':
            try:
                objPersona= Persona(cod,nom,tel,ema)
                objCliente= Cliente(cre)
                objControlCliente= ControlCliente(objPersona,objCliente)
                objControlCliente.consultar()        
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaClientes')	
        elif bt=='Modificar':
            try:
                objPersona= Persona(cod,nom,tel,ema)
                objCliente= Cliente(cre)
                objControlCliente= ControlCliente(objPersona,objCliente)
                objControlCliente.modificar()        
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaClientes')	
        elif bt=='Borrar':
            try:
                objPersona= Persona(cod,nom,tel,ema)
                objCliente= Cliente(cre)
                objControlCliente= ControlCliente(objPersona,objCliente)
                objControlCliente.borrar()        
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaClientes')	
        elif bt=='BorrarVarios':
            pass
    return render_template('/vistaClientes.html',ema=ema,arregloClientes=arregloClientes,cliente=cliente,paginacion=paginacion)

