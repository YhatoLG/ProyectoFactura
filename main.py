from flask import Flask, render_template, request, url_for, redirect, session
import markupsafe
#from gevent.pywsgi import WSGIServer
from datetime import datetime

from modelo.Cliente import *
from modelo.Usuario import *
from control.ControlUsuario import *
from modelo.RolUsuario import *
from control.ControlRolUsuario import *

from menu import menu
from vistaUsuarios import vistaUsuarios
from vistaRoles import vistaRoles
from vistaClientes import vistaClientes


app = Flask(__name__)
app.register_blueprint(menu)
app.register_blueprint(vistaUsuarios)
app.register_blueprint(vistaRoles)
app.register_blueprint(vistaClientes)

app.secret_key='secret_key'

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])  
def index():
    ema=""
    con=""
    bot=""
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        ema=markupsafe.escape(request.form['txtEmail'])
        con=markupsafe.escape(request.form['txtContrasena'])
        bot=markupsafe.escape(request.form['btnLogin'])
        if bot=='Login':
            validar=False
            objUsuario= Usuario(ema,con)
            objControlUsuario=ControlUsuario(objUsuario)
            validar=objControlUsuario.validarIngreso()
            if validar:
                objRolUsuario=RolUsuario(ema,0)
                objControlRolUsuario= ControlRolUsuario(objRolUsuario)
                matRolesDelUsuario = objControlRolUsuario.consultarRoles_por_EmailUsuario()
                session['ema']=markupsafe.escape(ema)
                session['matRolesDelUsuario']=matRolesDelUsuario
                return render_template('/menu.html',ema=ema)
            else:
                return render_template('/index.html')
        else:
            return render_template('/index.html')
    else:
        return render_template('/index.html')

@app.route('/cerrarSesion')
def cerrarSesion():
    session.clear()
    return redirect('index')

if __name__ == '__main__':
    # Debug/Development
    app.run(debug=True, host="127.0.0.1", port="5000")
    
    # Production
    #http_server = WSGIServer(('', 5000), app)
    #http_server.serve_forever()