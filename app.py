import hashlib
import sqlite3
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("login.html")

@app.route("/login", methods=["GET","POST"])
def login():
    correo = request.form["correo"]
    contrasena = request.form["clave"]
    contra = hashlib.sha256(contrasena.encode())
    contra_enc = contra.hexdigest()
      
    # Se conecta a la base de datos
    with sqlite3.connect("./DB/registros.db") as con:
        cur = con.cursor()
        cur.execute("SELECT email, passwor FROM usuarios WHERE email = ? AND passwor = ?", [correo,contra_enc])
        row = cur.fetchone()
        print(row)
        if row:
            if contra_enc == row[1] and correo == row[0]:
                return redirect("/dashboard")
        else:
            return f"Usuario o contraseña inconrrecto"
    
    return render_template("login.html")

@app.route("/registrar", methods=["GET"])
def registrar():
    return render_template("registro.html")

@app.route("/registro", methods=["POST"]) # La ruta donde se guardan los datos (Eje: registro) tiene que ser la misma Ruta en el <FORM> del html Registro.
def registro():
    primer_nombre = request.form["primer_nombre"]
    segundo_nombre = request.form["segundo_nombre"]
    primer_apellido = request.form["primer_apellido"]
    segundo_apellido = request.form["segundo_apellido"]
    genero = request.form["genero"]
    nacimiento = request.form["nacimiento"]
    identificacion = request.form["identificacion"]
    celular = request.form["celular"]
    correo = request.form["correo"]
    direccion = request.form["direccion"]
    rol = request.form["rol"]
    contrasena = request.form["contraseña"]
    contra = hashlib.sha256(contrasena.encode())
    contra_enc = contra.hexdigest()
    
    print(identificacion,primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,nacimiento,direccion,celular,correo,contrasena,genero,rol)
    
    with sqlite3.connect("./DB/registros.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO usuarios (identificacion,primerNombre,segundoNombre,primerApellido,segundoApellido,fechaNacimiento,direccion,telefono,email,password,genero,rol) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",[identificacion,primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,nacimiento,direccion,celular,correo,contra_enc,genero,rol]) 
        con.commit
        return render_template("registro.html")
    
@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/perfil", methods=["GET"])
def perfil():
    return render_template("perfil.html")

app.run(debug=True)
 