from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json


# -------------------- GENERADOR DE CONTRASEÑA -------------------- #
def generar_contraseña():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    contraseña_letras = [choice(letters) for _ in range(randint(8, 10))]
    contraseña_simbolos = [choice(symbols) for _ in range(randint(2, 4))]
    contraseña_numeros = [choice(numbers) for _ in range(randint(2, 4))]
    contraseña_lista = contraseña_numeros + contraseña_simbolos + contraseña_letras
    shuffle(contraseña_lista)

    password = "".join(contraseña_lista)
    output_contraseña.insert(0, password)
    pyperclip.copy(password)


# ---------------------- GUARDAR  CONTRASEÑA ---------------------- #
def save():
    website = input_website.get()
    usuario = usuario_input.get()
    contraseña = output_contraseña.get()
    new_data = {
        website: {
            "usuario": usuario,
            "contrasena": contraseña
        }
    }
    if len(website) == 0 or len(contraseña) == 0:
        messagebox.showinfo(title="Oops", message="Por favor no dejes ningún espacio vacío")
    else:
        try:
            with open("data_base.json", "r") as data_file:
                # Lee datos anteriores
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data_base.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Actualiza los datos anteriores con datos nuevos
            data.update(new_data)

            with open("data_base.json", "w") as data_file:
                # Salva los datos nuevos
                json.dump(data, data_file, indent=4)
        finally:
            input_website.delete(0, END)
            output_contraseña.delete(0, END)


# --------------------- ENCONTRAR  CONTRASEÑA --------------------- #
def encontrar_contraseña():
    website = input_website.get()
    try:
        with open("data_base.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Archivo de datos no encontrado.")
    else:
        if website in data:
            usuario = data[website]["usuario"]
            contraseña = data[website]["contrasena"]
            messagebox.showinfo(title=website, message=f"Usuario: {usuario}\nContraseña: {contraseña}")
        else:
            messagebox.showinfo(title="Error.", message=f"No hay datos sobre {website}")


# ---------------------------- UI SETUP --------------------------- #
ventana = Tk()
ventana.title("Administrador De Contraseñas")
ventana.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200, highlightthickness=0)
u_lock_img = PhotoImage(file="u_lock2.png")
canvas.create_image(100, 100, image=u_lock_img)
canvas.grid(column=1, row=0)

texto_website = Label(text="Website:", font=("Times New Roman", 12))
texto_website.grid(column=0, row=1)

input_website = Entry(width=31)
input_website.grid(column=1, row=1)
input_website.focus()

texto_usuario = Label(text="Usuario:", font=("Times New Roman", 12))
texto_usuario.grid(column=0, row=2)

usuario_input = Entry(width=57)
usuario_input.grid(column=1, row=2, columnspan=2)
usuario_input.insert(0, "brandonlibertad@gmail.com")

texto_contraseña = Label(text="Contraseña:", font=("Times New Roman", 12))
texto_contraseña.grid(column=0, row=3)

boton_generar_contraseña = Button(text="Generar Contraseña", width=21, highlightthickness=0, command=generar_contraseña)
boton_generar_contraseña.grid(column=2, row=3)

boton_buscar_contraseña = Button(text="Buscar", width=21, highlightthickness=0, command=encontrar_contraseña)
boton_buscar_contraseña.grid(column=2, row=1)

output_contraseña = Entry(width=31)
output_contraseña.grid(column=1, row=3)

boton_agregar = Button(text="Agregar", width=49, highlightthickness=0, command=save)
boton_agregar.grid(column=1, row=4, columnspan=2)

ventana.mainloop()
