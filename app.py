from flask import Flask #Importacion de libreria Flask
from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_mysqldb import MySQL, MySQLdb

#Enlace con el directorio de archivos
app = Flask(__name__,template_folder='template')
app.secret_key="fabian_pc"

#Variable global para indicar si el inicio de sesión se realizó correctamente
sesion_iniciada = False
correo = ""

#Conexion a la base de datos
app.config['MYSQL_HOST']='34.29.193.58'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='1234'
app.config['MYSQL_DB']='LOGIN'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)

#Agregar el acceso a las paginas web
@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM restaurantes")
    restaurantes = cur.fetchall()
    cur.close()

    if 'usuario' in session:
        return render_template('index2.html', restaurantes=restaurantes, usuario=session['usuario'],confirmacion=sesion_iniciada)
    else:
        return render_template('index2.html', restaurantes=restaurantes)


#Registro de datos con funcion (ruta para duadarlos)
@app.route('/restaurante',methods=["GET","POST"])
def addRestaurante():
    if 'usuario' in session:
        nombre=request.form['txtNombreR']
        tipo=request.form['txtTipoR']
        direccion=request.form['txtDireccionR']
        telefono=request.form['txtTelefonoR']

        if nombre and tipo and direccion and telefono:
            cur=mysql.connection.cursor()
            cur.execute("INSERT INTO restaurantes (nombre,tipo,direccion,telefono) VALUES(%s,%s,%s,%s)",(nombre,tipo,direccion,telefono))
            mysql.connection.commit()
        
        
        return redirect(url_for('home')) #Refrescar pagina
    else:
        flash('Necesitas iniciar sesion para agregar un nuevo restaurante:/', 'danger')
        return redirect(url_for('home'))  # Refrescar página

#Eliminar restaurante
@app.route('/delete/<string:idrestaurante>')
def delete(idrestaurante):
    

    

    if 'usuario' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM restaurantes WHERE idrestaurante=%s", (idrestaurante,))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('home'))
    else:
        mensaje=False
        flash('Necesitas iniciar sesión para eliminar un restaurante:/', 'danger')
        return redirect(url_for('home'))
   

#Editar restaurante
@app.route('/edit/<string:idrestaurante>', methods=["GET", "POST"])
def update(idrestaurante):
    if 'usuario' in session:
        if request.method == "POST":
            nombre = request.form['txtNombreR']
            tipo = request.form['txtTipoR']
            direccion = request.form['txtDireccionR']
            telefono = request.form['txtTelefonoR']

        if nombre and tipo and direccion and telefono:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE restaurantes SET nombre=%s, tipo=%s, direccion=%s, telefono=%s WHERE idrestaurante=%s",
                                    (nombre, tipo, direccion, telefono, idrestaurante))
            mysql.connection.commit()
            cur.close()

        redirect(url_for('home'))
        return redirect(url_for('home'))  # Refrescar página
    else:
        flash('Necesitas iniciar sesion para actualizar un restaurante:/', 'danger')
        return redirect(url_for('home'))  # Refrescar página

@app.route('/admin')
def admin():
    return render_template('admin.html')

#Redirige a la pestaña para iniciar sesion
@app.route('/iniciosesion')
def iniciosesion():
    if 'usuario' in session: #Si logeado no lo deja iniciar sesion
        return redirect(url_for('home'))
    else:
        return render_template('index.html') 
    #if sesion_iniciada==True:
        #return redirect(url_for('home'))  
    #else:
        #return render_template('index.html')

#Cierra la sesion del usuario
@app.route('/cerrar-sesion')
def cerrar_sesion():
    # Verifica si hay un usuario en la sesión
    if 'usuario' in session:
        # Elimina al usuario de la sesión
        session.pop('usuario', None)
    return redirect(url_for('home'))  # Redirige a la página de inicio o a donde desees

@app.route('/acceso-login', methods=["POST"])
def login():
    # Verifica si ya hay un usuario logueado
    
    #if 'usuario' in session:
        #return redirect(url_for('home'))

    # Recuperación de la información del formulario
    _correo = request.form['txtCorreo']
    _password = request.form['txtPassword']

    # Ejecución de BD y consulta SQL
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE correo=%s AND password=%s', (_correo, _password))
    account = cur.fetchone()  # Guardando el resultado

    # Respuesta a la consulta del inicio de sesión con lo guardado
    if account:
        # Guarda el nombre de usuario en la sesión
        session['usuario'] = _correo
        return redirect(url_for('home'))
    else:
        return render_template('index.html', mensaje="Usuario incorrecto") 
        #return redirect(url_for('iniciosesion'))

#Funcion de registro que me dirige a el HTML de registro
@app.route('/registro')
def registro():
    if 'usuario' in session:
        return redirect(url_for('home')) 
    else:
        return render_template('registro.html')

#Funcion de registro que me dirige a el HTML de registro
@app.route('/cerrar-sesion')
def logout():
    global sesion_iniciada # Marca la variable global como verdadera
    global correo

    sesion_iniciada = False  # Marca la variable global como verdadera
    correo=""

    return redirect(url_for('home'))
    

#Funcion de crear nuevo registro
@app.route('/crear-registro',methods=["GET","POST"])
def crear_registro():
    correo=request.form['txtCorreo']
    username=request.form['txtUsername']
    password=request.form['txtPassword']

    if correo!="" and username!="" and password!="":
        #Ejecucion de BD y consulta SQL
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (username,correo,password,id_rol) VALUES(%s,%s,%s,'2')",(username,correo,password))
        mysql.connection.commit()

        return render_template("index.html", mensaje2="usuario registrado exitosamente, ya puedes iniciar sesion:)")
    else:
        return render_template("registro.html",mensaje3="Ingresa todos los campos para realizar el registro:(")

#----------------------


#------LISTAR USAURIOS---------
@app.route('/listar',methods=["GET","POST"])
def listar():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM restaurantes")
    restaurantes=cur.fetchall()
    cur.close()

    return render_template("listar_usuarios.html",restaurantes=restaurantes)


#------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0',port="5000",debug = True)