import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import io
import mysql.connector

# Conecte-se ao banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ricardo&Danubia",
    database="testedb"
)
cursor = db.cursor()

# Função para carregar uma imagem


def carregar_imagem():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "rb") as file:
            image_blob = file.read()
            # Salvar a imagem no banco de dados
            cursor.execute(
                "INSERT INTO Perfil (foto) VALUES (%s)", (image_blob,))
            db.commit()
            mostrar_imagem(image_blob)

# Função para mostrar a imagem


def mostrar_imagem(image_blob):
    image = Image.open(io.BytesIO(image_blob))
    photo = ImageTk.PhotoImage(image)
    label_imagem.config(image=photo)
    label_imagem.image = photo


# Configuração da janela principal
root = tk.Tk()
root.title("Carregar e Exibir Imagem")

# Botão para carregar imagem
btn_carregar = tk.Button(root, text="Carregar Imagem", command=carregar_imagem)
btn_carregar.pack()

# Label para exibir a imagem
label_imagem = tk.Label(root)
label_imagem.pack()

root.mainloop()
