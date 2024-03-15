from flask import Blueprint,render_template,session,redirect,url_for

menu=Blueprint("menu",__name__,static_folder="static",template_folder="templates")

@menu.route("/menu",methods = ['GET', 'POST'])
@menu.route("/")
def vista_menu():
    if 'ema' in session:
        ema=session['ema']
        return render_template('/menu.html',ema=ema)
    return redirect('/index')  