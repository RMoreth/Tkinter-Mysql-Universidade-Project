import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

login = True


class App(ctk.CTk):
    def __init__(self, title, size) -> None:
        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        # widgets
        self.menu = Menu(master=self)

        # frame atual

        self.frame_atual = None

        # inicializa a tela login
        self.set_login()
        # metodos

    def mudar_title(self, novo):
        self.title(novo)

    def set_login(self):
        if self.frame_atual:
            self.frame_atual.destroy()

        self.frame_atual = Login(master=self)
        self.frame_atual.place(relx=0.1, rely=0, relwidth=0.9, relheight=1)

    def set_cadastro(self):
        if self.frame_atual:
            self.frame_atual.destroy()

        self.frame_atual = Cadastro(master=self)
        self.frame_atual.place(relx=0.1, rely=0, relwidth=0.9, relheight=1)

    def set_banco_de_dados(self):
        if self.frame_atual:
            self.frame_atual.destroy()

        self.frame_atual = Banco_de_dados(master=self)
        self.frame_atual.place(relx=0.1, rely=0, relwidth=0.9, relheight=1)

    def set_sobre(self):
        if self.frame_atual:
            self.frame_atual.destroy()

        self.frame_atual = Sobre(master=self)
        self.frame_atual.place(relx=0.1, rely=0, relwidth=0.9, relheight=1)


class Menu(ctk.CTkFrame):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.border_width = 2
        self.border_color = 'gray'
        self.fg_color = 'black'
        self.place(relx=0, rely=0, relwidth=0.1, relheight=1)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.btn_login = ctk.CTkButton(
            self, text="Login", command=self.abrir_login)
        self.btn_cadastro = ctk.CTkButton(
            self, text="Cadastro", command=self.abrir_cadastro)
        self.btn_banco_de_dados = ctk.CTkButton(
            self, text="Banco de dados", command=self.abrir_banco_de_dados)
        self.btn_sobre = ctk.CTkButton(
            self, text='Sobre', command=self.abrir_sobre)
        if login is not True:
            self.btn_cadastro.configure(state='disabled')
            self.btn_banco_de_dados.configure(state='disabled')

    def create_layout(self):
        self.btn_login.place(relx=0.5, rely=0.1, anchor='center')
        self.btn_cadastro.place(relx=0.5, rely=0.15, anchor='center')
        self.btn_banco_de_dados.place(relx=0.5, rely=0.2, anchor='center')
        self.btn_sobre.place(relx=0.5, rely=0.25, anchor='center')

    def abrir_login(self):
        self.master.set_login()
        self.master.mudar_title(novo='Login')

    def abrir_cadastro(self):
        self.master.set_cadastro()
        self.master.mudar_title(novo='Cadastro')

    def abrir_banco_de_dados(self):
        self.master.set_banco_de_dados()
        self.master.mudar_title(novo='Banco de Dados')

    def abrir_sobre(self):
        self.master.set_sobre()
        self.master.mudar_title(novo='Sobre')


class Login(ctk.CTkFrame):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        label = ctk.CTkLabel(self, text="Login")
        label.pack(expand=True, fill='both', padx=20, pady=20)


class Aluno_tab(ctk.CTkFrame):
    def __init__(self, **kw) -> None:
        super().__init__(self, **kw)


class Cadastro(ctk.CTkFrame):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.cadastro_tree = ctk.CTkTabview(self, anchor='nw')
        self.alunotab = self.cadastro_tree.add("Aluno")
        self.professortab = self.cadastro_tree.add("Professor")
        self.deptab = self.cadastro_tree.add("Departamento")
        self.discitab = self.cadastro_tree.add("Disciplina")
        self.turmatab = self.cadastro_tree.add("Turma")

    def create_layout(self):
        self.cadastro_tree.place(relx=0.02, rely=0.01,
                                 relwidth=0.96, relheight=0.95)


class Banco_de_dados(ctk.CTkFrame):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        label = ctk.CTkLabel(self, text="Banco de dados")
        label.pack(expand=True, fill='both', padx=20, pady=20)


class Sobre(ctk.CTkFrame):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        label = ctk.CTkLabel(self, text="Sobre")
        label.pack(expand=True, fill='both', padx=20, pady=20)


if __name__ == '__main__':
    mainapp = App('Login', (500, 500))
    mainapp.mainloop()
