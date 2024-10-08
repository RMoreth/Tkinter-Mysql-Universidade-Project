import customtkinter as ctk  # type:ignore
import tkinter as tk  # type:ignore
from tkinter import ttk, messagebox  # type:ignore
from tkcalendar import DateEntry  # type:ignore
from datetime import datetime
from db_functions import Controlador_db
import json
from typing import Tuple

login = True

# SECTION - Class: App


class App(ctk.CTk):
    """
    Casse que representa a janela do Aplicativo.

    Args:
        title: STR que representa o título da janela.
        size: Tuple com 2 parametros INT que representa
    """
    # SECTION - INIT

    def __init__(self, title: str, size: Tuple[int, int]) -> None:
        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        self.db_params = {
            'tipo': ctk.StringVar(),
            'host': ctk.StringVar(),
            'user': ctk.StringVar(),
            'password': ctk.StringVar(),
            'nome': ctk.StringVar()
        }
        self.carregar_db_params()
        self.db = DataBase(
            host=self.db_params['host'].get(),
            user=self.db_params['user'].get(),
            password=self.db_params['password'].get(),
            database=self.db_params['nome'].get(),


        )

        # widgets
        self.menu = Menu(master=self)

        # frame atual

        self.frame_atual = None

        # inicializa a tela login
        self.set_login()
    # !SECTION init
    # SECTION - Method: Carregar_db_params

    def carregar_db_params(self):
        """Carrega os parametros do banco de dados salvos em db_config.json"""
        try:
            with open('db_config.json', 'r') as f:
                config = json.load(f)
                self.db_params['tipo'].set(config['tipo'])
                self.db_params['host'].set(config['host'])
                self.db_params['user'].set(config['user'])
                self.db_params['password'].set(config['password'])
                self.db_params['nome'].set(config['nome'])

        except FileNotFoundError:
            pass
    # !SECTION - Method: Carregar_db_params
    # SECTION - Method: Mudar_title

    def mudar_title(self, novo: str):
        """
        Redefine o título da janela.

        Args:
            title: STR que representa o novo titulo
        """
        self.title(novo)
    # !SECTION - Method: Mudar_title
    # SECTION - Method: set_login

    def set_login(self):
        """Define a tela principal como a tela Login."""
        if self.frame_atual:
            self.frame_atual.destroy()

        self.frame_atual = Login(master=self)
        self.frame_atual.place(relx=0.1, rely=0, relwidth=0.9, relheight=1)
    # !SECTION - Method: set_login
    # SECTION - Method: set_cadastro

    def set_cadastro(self):
        """Define a tela principal como a tela cadastro."""
        if self.frame_atual:
            self.frame_atual.destroy()

        self.frame_atual = Cadastro(master=self)
        self.frame_atual.place(relx=0.1, rely=0, relwidth=0.9, relheight=1)
    # !SECTION - Method: set_cadastro
    # SECTION - Method: set_banco_de_dados

    def set_banco_de_dados(self):
        """Define a tela principal como a tela banco de dados."""
        if self.frame_atual:
            self.frame_atual.destroy()

        self.frame_atual = Banco_de_dados(master=self)
        self.frame_atual.place(relx=0.1, rely=0, relwidth=0.9, relheight=1)
    # !SECTION - Method: set_banco de dados
    # SECTION - Method: set_sobre

    def set_sobre(self):
        """Define a tela principal como a tela sobre."""
        if self.frame_atual:
            self.frame_atual.destroy()

        self.frame_atual = Sobre(master=self)
        self.frame_atual.place(relx=0.1, rely=0, relwidth=0.9, relheight=1)
    # !SECTION - Method: set_sobre
# !SECTION app

# SECTION - Class: Menu


class Menu(ctk.CTkFrame):
    """Classe que representa o frame que define o menu."""
    # SECTION - Init

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.border_width = 2
        self.border_color = 'gray'
        self.fg_color = 'black'
        self.place(relx=0, rely=0, relwidth=0.1, relheight=1)
        self.create_widgets()
        self.create_layout()
    # !SECTION - Init
    # SECTION - Method: create_widgets

    def create_widgets(self):
        """Criação dos widgets de menu, é chamado no __init__."""
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
    # !SECTION - Method: create_widgets
    # SECTION - Method: create_layout

    def create_layout(self):
        """Criação do layout dos widgets de menu, é chamado no __init__."""

        self.btn_login.place(relx=0.5, rely=0.1, anchor='center')
        self.btn_cadastro.place(relx=0.5, rely=0.15, anchor='center')
        self.btn_banco_de_dados.place(relx=0.5, rely=0.2, anchor='center')
        self.btn_sobre.place(relx=0.5, rely=0.25, anchor='center')
    # !SECTION - Method: create_layout
    # SECTION - Method: abrir_login

    def abrir_login(self):
        """Muda a tela principal para a tela Login."""
        self.master.set_login()  # type:ignore
        self.master.mudar_title(novo='Login')  # type:ignore
    # !SECTION - Method: abrir_login
    # SECTION - Method: abrir_cadastro

    def abrir_cadastro(self):
        """Muda a tela principal para a tela cadastro."""
        self.master.set_cadastro()  # type:ignore
        self.master.mudar_title(novo='Cadastro')  # type:ignore
    # !SECTION - Method: abrir_cadastro
    # SECTION - Method: abrir_banco_de_dados

    def abrir_banco_de_dados(self):
        """Muda a tela principal para a tela banco de dados."""
        self.master.set_banco_de_dados()  # type:ignore
        self.master.mudar_title(novo='Banco de Dados')  # type:ignore
    # !SECTION - Method: abrir_banco_de_dados
    # SECTION - Method: abrir_sobre

    def abrir_sobre(self):
        """Muda a tela principal para a tela sobre."""
        self.master.set_sobre()  # type:ignore
        self.master.mudar_title(novo='Sobre')  # type:ignore
    # !SECTION - Method: abrir_sobre
# !SECTION - Class: Menu

# SECTION - Class:Login


class Login(ctk.CTkFrame):
    """Classe que representa o frame que define o login."""
    # SECTION - Init

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.create_widgets()
        self.create_interface()
    # !SECTION - Init
    # SECTION - Method: create_widgets

    def create_widgets(self):
        """Criação dos widgets de login, é chamado no __init__."""
        self.frame_box = ctk.CTkFrame(self,
                                      border_width=5,
                                      fg_color='darkgrey',)

        self.texto_login = ctk.CTkLabel(
            self.frame_box, text="Login", fg_color="darkgrey",
            text_color="grey10", font=('Helvetica', 35))
        self.texto_login.configure(justify="center")
        self.lb_usuario = ctk.CTkLabel(
            self.frame_box, text="Usuário", fg_color="darkgrey",
            text_color="grey10", font=('Helvetica', 25))
        self.usuario_ent = ctk.CTkEntry(
            self.frame_box, fg_color='gray45', text_color='grey10',
            width=200, justify='center', font=('helvetica', 20), )
        self.lb_senha = ctk.CTkLabel(
            self.frame_box, text="Senha", fg_color="darkgrey",
            text_color="grey10", font=('Helvetica', 25))
        self.senha_ent = ctk.CTkEntry(
            self.frame_box, fg_color='gray45', text_color='grey10',
            width=200, justify='center', font=('helvetica', 20),
            show="*")
        self.bt_login = ctk.CTkButton(
            self.frame_box,
            text="LOGIN",
            fg_color='gray45',
            text_color='gray10',
            font=('verdana', 20, 'bold'),
        )
    # !SECTION - Method: create_widgets
    # SECTION - Method: create_interface

    def create_interface(self):
        """Criação da interface dos widgets de login, é chamado no __init__."""
        self.frame_box.place(
            relwidth=0.28,
            relheight=0.7,
            relx=0.36,
            rely=0.15)
        self.texto_login.pack(pady=50)
        self.lb_usuario.pack(pady=20,)
        self.usuario_ent.pack(pady=10)
        self.senha_ent.pack(pady=10)
        self.bt_login.pack(pady=50)
    # !SECTION - Method: create_interface
# !SECTION - Class: Login
# SECTION - Class: Label


class Label(ctk.CTkLabel):
    """
    Classe que representa uma Label genérica.

    Args:
        texto: STR que indica o texto da label
    """

    def __init__(self, texto: str, **kw) -> None:
        super().__init__(**kw)
        self.configure(text=texto,
                       fg_color='transparent',
                       font=('Helvetica', 12))

# !SECTION - Class: Label

# SECTION - Class: Entry


class Entry(ctk.CTkEntry):
    """Classe que representa uma Entry genérica."""

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.configure(fg_color="white",
                       text_color='black')

# !SECTION - Class: Entry
# SECTION - Class: Btn


class Btn(ctk.CTkButton):
    """
    Classe que representa um Botão genérico.

    Args:
        texto: STR que indica o texto do botão
    """

    def __init__(self, texto: str, **kw) -> None:
        super().__init__(**kw)
        self.configure(border_width=1,
                       border_color='gray13',
                       fg_color='gray67',
                       text=texto,)
# !SECTION - Class: Btn

# SECTION - Class: Aluno_tab


class Aluno_tab(ctk.CTkFrame):
    """Classe que representa o frame que define a Aba Alunos em Cadastro."""
    # SECTION - Init

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.selecionado = False
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.create_layout()
        self.montar_lista_alu()
    # !SECTION - Init
    # SECTION - Method: create_widgets

    def create_widgets(self):
        """Criação dos widgets de Alunotab, é chamado no __init__."""

        self.titulo = ctk.CTkLabel(self,
                                   text="Cadastro aluno",
                                   font=("Helvetica", 25),
                                   fg_color="transparent")
        self.lb_codra = Label('CodRA', master=self)
        self.ent_codra = Entry(master=self)

        self.lb_nome = Label('Nome', master=self)
        self.ent_nome = Entry(master=self)

        self.lb_cpf = Label('CPF', master=self)
        self.ent_cpf = Entry(master=self)

        self.lb_data_nasc = Label('Data de Nascimento', master=self)
        self.ent_data_nasc = DateEntry(self,
                                       locale="pt_BR",
                                       year=2000,
                                       month=1,
                                       day=1)

        self.lb_email = Label('Email', master=self)
        self.ent_email = Entry(master=self)

        self.lb_status_matricula = Label('Status da Matricula', master=self)
        self.ent_status_matricula = ctk.CTkComboBox(self,
                                                    fg_color="white",
                                                    text_color='black',
                                                    values=['Ativa',
                                                            'Inativa',
                                                            'Trancado'])
        self.ent_status_matricula.set('')

        self.lb_cep = ctk.CTkButton(self,
                                    fg_color='transparent',
                                    border_color='green',
                                    border_width=1,
                                    text='CEP')
        self.ent_cep = Entry(master=self)

        self.lb_estado = Label('Estado', master=self)
        self.ent_estado = ctk.CTkComboBox(self,
                                          fg_color='white',
                                          text_color='black',
                                          values=[
                                              'AC', 'AL', 'AP', 'AM', 'BA',
                                              'CE', 'DF', "ES", 'GO', 'MA',
                                              'MT', 'MS', 'MG', 'PA', 'PB',
                                              'PR', 'PE', 'PI', 'RJ', 'RN',
                                              'RS', 'RO', 'RR', 'SC', 'SP',
                                              'SE', 'TO']
                                          )
        self.ent_estado.set('')

        self.lb_cidade = Label('Cidade', master=self)
        self.ent_cidade = Entry(master=self)

        self.lb_bairro = Label('Bairro', master=self)
        self.ent_bairro = Entry(master=self)

        self.lb_logradouro = Label('Logradouro', master=self)
        self.ent_logradouro = Entry(master=self)

        self.lb_numero = Label('Numero', master=self)
        self.ent_numero = Entry(master=self)

        self.lb_foto = Label('Foto', master=self)
        self.lb_foto.configure(fg_color="gray27",
                               corner_radius=7)
        self.frame_foto = ctk.CTkFrame(self,
                                       fg_color='gray27',
                                       border_width=2,
                                       border_color='gray24',
                                       )

        self.lb_tel = Label('Telefone', master=self)
        self.lb_tel.configure(fg_color="gray27",
                              corner_radius=7)

        self.frame_tel = ctk.CTkFrame(self,
                                      fg_color='gray27',
                                      border_width=2,
                                      border_color='gray24',
                                      )
        self.lb_sel_alu = Label(
            'Aluno: Não selecionado', master=self.frame_tel)
        self.lista_tel = ttk.Treeview(
            self.frame_tel,
            height=3,
            columns=('col1', 'col2',)
        )
        self.lista_tel.heading('#0', text='')
        self.lista_tel.heading('#1', text='P')
        self.lista_tel.heading('#2', text='Número')

        self.lista_tel.column('#0', width=1, minwidth=1, anchor='center')
        self.lista_tel.column('#1', width=20, anchor='center', minwidth=20)
        self.lista_tel.column('#2', width=150, anchor='center', minwidth=150)
        self.lista_tel.bind("<Double-1>", self.ondoubleclick_alu_tel)

        self.scrool_lista_tel = tk.Scrollbar(self.frame_tel,
                                             orient='vertical',
                                             command=self.lista_tel.yview)
        self.lista_tel.configure(yscrollcommand=self.scrool_lista_tel.set)

        self.lb_prioridade = Label('Prioridade', master=self.frame_tel)
        self.ent_prioridade = ctk.CTkComboBox(self.frame_tel,
                                              fg_color="white",
                                              text_color="black",
                                              values=['1',
                                                      '2',
                                                      '3',
                                                      '4',
                                                      '5'])
        self.ent_prioridade.set('')

        self.lb_telefone = Label('Telefone', master=self.frame_tel)
        self.ent_telefone = Entry(master=self.frame_tel)

        self.btn_novo_tel = Btn('Novo',
                                master=self.frame_tel,
                                command=self.add_tel_aluno)
        self.btn_apagar_tel = Btn('Apagar',
                                  master=self.frame_tel,
                                  command=self.excluir_tel_alu)
        self.btn_excluir = Btn('Excluir', master=self)
        self.btn_excluir.configure(border_color='red1',
                                   border_width=1,
                                   fg_color='red4',
                                   text_color='white',
                                   command=self.excluir_aluno,)

        self.btn_alterar = Btn('Alterar', master=self)
        self.btn_alterar.configure(border_color='lightseagreen',
                                   border_width=1,
                                   fg_color='gray22',
                                   text_color='black',)

        self.btn_novo = Btn('Novo', master=self)
        self.btn_novo.configure(border_color='green4',
                                border_width=1,
                                fg_color='gray22',
                                command=self.add_aluno,
                                text_color='black')

        self.btn_limpar = Btn('Limpar', master=self)
        self.btn_limpar.configure(border_color='brown4',
                                  border_width=1,
                                  fg_color='gray22',
                                  command=self.apagar_campos_aluno,
                                  text_color='black',)

        self.btn_buscar = Btn('Buscar', master=self)
        self.btn_buscar.configure(border_color='gray75',
                                  border_width=1,
                                  fg_color='gray22',
                                  text_color='black',
                                  command=self.buscar_aluno,)

        self.lb_curso = Label('Curso', master=self)
        self.lista_curso = self.montar_lista_cursos()

        self.ent_curso = ctk.CTkComboBox(self,
                                         fg_color='white',
                                         text_color='black',
                                         values=self.lista_curso,
                                         font=("Helvetica", 20),
                                         dropdown_font=("Helvetica", 20),
                                         justify='center')
        self.ent_curso.set('')

        self.lista_alu = ttk.Treeview(
            self,
            height=3,
            columns=('col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7')
        )
        self.lista_alu.heading('#0', text='')
        self.lista_alu.heading('#1', text='CodRA')
        self.lista_alu.heading('#2', text='Nome')
        self.lista_alu.heading('#3', text='CPF')
        self.lista_alu.heading('#4', text='Data de Nascimento')
        self.lista_alu.heading('#5', text='Email')
        self.lista_alu.heading('#6', text='Situação')
        self.lista_alu.heading('#7', text='Curso')

        self.lista_alu.column('#0', width=1, minwidth=1, anchor='center')
        self.lista_alu.column('#1', width=50, anchor='center', minwidth=50)
        self.lista_alu.column('#2', width=160, anchor='center', minwidth=160)
        self.lista_alu.column('#3', width=160, anchor='center', minwidth=160)
        self.lista_alu.column('#4', width=90, anchor='center', minwidth=90)
        self.lista_alu.column('#5', width=160, anchor='center', minwidth=160)
        self.lista_alu.column('#6', width=100, anchor='center', minwidth=100)
        self.lista_alu.column('#7', width=220, anchor='center', minwidth=220)

        self.scrool_lista_alu = tk.Scrollbar(self,
                                             orient='vertical',
                                             command=self.lista_alu.yview)
        self.lista_alu.configure(yscrollcommand=self.scrool_lista_alu.set)
        self.lista_alu.bind("<Double-1>", self.on_doubleclick_aluno)
    # !SECTION - Method: create_widgets
    # SECTION - Method: create_layout

    def create_layout(self):
        """Criação do layout dos widgets de Alunotab, é chamado no __init__."""

        self.titulo.place(anchor='center', relx=0.5, rely=0.05)

        self.lb_codra.place(relx=0.06, rely=0.12,
                            relwidth=0.2, anchor='c')
        self.ent_codra.place(relx=0.11, rely=0.1, relwidth=0.05)

        self.lb_nome.place(relx=0.06, rely=0.16,
                           relwidth=0.2, anchor='c')
        self.ent_nome.place(relx=0.11, rely=0.14, relwidth=0.16)

        self.lb_cpf.place(relx=0.06, rely=0.2,
                          relwidth=0.2, anchor='c')
        self.ent_cpf.place(relx=0.11, rely=0.18, relwidth=0.08)

        self.lb_data_nasc.place(relx=0.06, rely=0.24,
                                relwidth=0.2, anchor='c')
        self.ent_data_nasc.place(relx=0.112, rely=0.225, relwidth=0.06)

        self.lb_email.place(relx=0.06, rely=0.28,
                            relwidth=0.2, anchor='c')
        self.ent_email.place(relx=0.11, rely=0.26, relwidth=0.15)

        self.lb_status_matricula.place(relx=0.06, rely=0.32,
                                       relwidth=0.2, anchor='c')
        self.ent_status_matricula.place(relx=0.11, rely=0.30, relwidth=0.08)

        self.lb_cep.place(relx=0.29, rely=0.12, anchor='c', relwidth=0.04)
        self.ent_cep.place(relx=0.32, rely=0.1, relwidth=0.07)

        self.lb_estado.place(relx=0.29, rely=0.16, anchor='c')
        self.ent_estado.place(relx=0.32, rely=0.14, relwidth=0.045)

        self.lb_cidade.place(relx=0.29, rely=0.20, anchor='c')
        self.ent_cidade.place(relx=0.32, rely=0.18, relwidth=0.1)

        self.lb_bairro.place(relx=0.29, rely=0.24, anchor='c')
        self.ent_bairro.place(relx=0.32, rely=0.22, relwidth=0.1)

        self.lb_logradouro.place(relx=0.29, rely=0.28, anchor='c')
        self.ent_logradouro.place(relx=0.32, rely=0.26, relwidth=0.1)

        self.lb_numero.place(relx=0.29, rely=0.32, anchor='c')
        self.ent_numero.place(relx=0.32, rely=0.3, relwidth=0.1)

        self.lb_foto.place(relx=0.5, rely=0.105, relwidth=0.1, anchor='c')
        self.frame_foto.place(relx=0.5, rely=0.23,
                              relwidth=0.1, relheight=0.18,
                              anchor='c')

        self.lb_tel.place(
            relx=0.78, rely=0.1, relwidth=0.1, anchor='c')

        self.frame_tel.place(relx=0.78, rely=0.225,
                             relwidth=0.3, relheight=0.2,
                             anchor='c')
        self.lb_sel_alu.place(relx=0.5, rely=0.06, anchor='c')
        self.lista_tel.place(relx=0.01, rely=0.13,
                             relheight=0.85, relwidth=0.45)
        self.scrool_lista_tel.place(
            relx=0.46, rely=0.13, relheight=0.85, relwidth=0.04)

        self.lb_prioridade.place(relx=0.53, rely=0.13)
        self.ent_prioridade.place(relx=0.7, rely=0.13, relwidth=0.12)

        self.lb_telefone.place(relx=0.53, rely=0.34)
        self.ent_telefone.place(relx=0.7, rely=0.34, relwidth=0.28)

        self.btn_novo_tel.place(
            relx=0.62, rely=0.74, relwidth=0.1, anchor='c')

        self.btn_apagar_tel.place(
            relx=0.79, rely=0.74, relwidth=0.15, anchor='c')

        self.btn_excluir.place(relx=0.12, rely=0.4, relwidth=0.05)
        self.btn_alterar.place(relx=0.18, rely=0.4, relwidth=0.05)
        self.btn_novo.place(relx=0.24, rely=0.4, relwidth=0.05)
        self.btn_limpar.place(relx=0.30, rely=0.4, relwidth=0.05)
        self.btn_buscar.place(relx=0.36, rely=0.4, relwidth=0.05)

        self.lb_curso.place(relx=0.78, rely=0.38, relwidth=0.1, anchor='c')
        self.ent_curso.place(relx=0.78, rely=0.41, anchor='c',
                             relwidth=0.3)

        self.lista_alu.place(relx=0.08, rely=0.5,
                             relheight=0.5, relwidth=0.82)
        self.scrool_lista_alu.place(
            relx=0.9, rely=0.5, relheight=0.5, relwidth=0.01)
    # !SECTION - Method: create_layout
    # SECTION - Method: variaveis_alu

    def variaveis_alu(self):
        self.codra = self.ent_codra.get()
        self.nome = self.ent_nome.get()
        self.cpf = self.ent_cpf.get()
        self.email = self.ent_email.get()
        self.status_matricula = self.ent_status_matricula.get()
        self.curso = self.ent_curso.get()
        self.estado = self.ent_estado.get()
        self.cidade = self.ent_cidade.get()
        self.bairro = self.ent_bairro.get()
        self.cep = self.ent_cep.get()
        self.logradouro = self.ent_logradouro.get()
        self.numero = self.ent_numero.get()
        self.data_nasc = self.ent_data_nasc.get()
        self.prioridade = self.ent_prioridade.get()
        self.telefone = self.ent_telefone.get()
        if self.data_nasc:
            self.data_nasc_obj = datetime.strptime(
                self.data_nasc, "%d/%m/%Y")
            self.data_nasc_format = self.data_nasc_obj.strftime("%Y-%m-%d")
        else:
            self.data_nasc_format = ""
    # !SECTION - Method: variaveis_alu
    # SECTION - Method: montar_lista_alu

    def montar_lista_alu(self):
        """Preenche a Treeview lista_alu com as informações do banco de dados."""  # noqa

        self.lista_alu.delete(*self.lista_alu.get_children())
        querry_lista_alu = """ SELECT a.codra,
                    a.nome,
                    a.cpf,
                    date_format(a.data_nasc, '%d/%m/%Y'),
                    a.email,
                    a.statusmatricula,
                    c.nome
                    FROM tbaluno a
                    JOIN tbcurso c
                    ON c.codCurso = a.codcurso
                    ORDER BY a.nome;
                    """

        lista = mainapp.db.consultar_query(querry_lista_alu)

        for i in lista:
            self.lista_alu.insert("", tk.END, values=i)  # type:ignore
    # !SECTION - Method: montar_lista_alu
    # SECTION - Method: montar_lista_cursos

    def montar_lista_cursos(self) -> list:
        """Recupera as informações de Cursos do banco de dados para ser usada na Combobox ent_curso."""  # noqa
        resultado = []
        query = "SELECT nome FROM tbCurso"
        consulta = mainapp.db.consultar_query(query=query)
        for row in consulta:
            resultado.append(row[0])  # type:ignore
        return resultado
    # !SECTION - Method: montar_lista_cursos
    # SECTION - Method: apagar_campos_aluno

    def apagar_campos_aluno(self):
        """Apaga os caracteres inseridos nas entrys de Alunotab."""

        self.ent_codra.delete('0', tk.END)  # type: ignore
        self.ent_nome.delete('0', tk.END)  # type: ignore
        self.ent_cpf.delete('0', tk.END)  # type: ignore
        self.ent_data_nasc.delete('0', tk.END)  # type: ignore
        self.ent_email.delete('0', tk.END)  # type: ignore
        self.ent_status_matricula.set('')  # type: ignore
        self.ent_curso.set('')  # type: ignore
        self.ent_estado.set('')  # type: ignore
        self.ent_cidade.delete('0', tk.END)  # type: ignore
        self.ent_bairro.delete('0', tk.END)  # type: ignore
        self.ent_cep.delete('0', tk.END)  # type: ignore
        self.ent_logradouro.delete('0', tk.END)  # type: ignore
        self.ent_numero.delete('0', tk.END)  # type: ignore
        self.ent_telefone.delete('0', tk.END)  # type: ignore
        self.ent_prioridade.set('')  # type: ignore

        self.lista_tel.delete(*self.lista_tel.get_children())
        self.lb_sel_alu.configure(
            text='Aluno: não selecionado', fg_color='red')
    # !SECTION - Method: apagar_campos_aluno
    # SECTION - Method: Apagar_campos_tel

    def apagar_campos_tel(self):
        self.ent_telefone.delete('0', tk.END)
        self.ent_prioridade.set('')
    # !SECTION - Method: Apagar_campos_tel
    # SECTION - Method: on_doubleclick_aluno

    def on_doubleclick_aluno(self, event):
        """
        Evento acionado com duplo clique em uma linha da treeview lista_alu,
        busca as informações do aluno no banco de dados
        e preenche as entrys com essas informações
        """
        self.apagar_campos_aluno()
        self.lista_alu.selection()  # type: ignore
        for n in self.lista_alu.selection():  # type: ignore
            col1, col2, col3, col4, col5, col6, col7 = self.lista_alu.item(  # noqa # type: ignore
                n, 'values')

            self.ent_codra.insert(tk.END, col1)
            self.ent_nome.insert(tk.END, col2)
            self.ent_cpf.insert(tk.END, col3)
            self.ent_data_nasc.set_date(col4)  # type: ignore
            self.ent_email.insert(tk.END, col5)  # type: ignore
            self.ent_curso.set(col7)  # type: ignore
            self.ent_status_matricula.set(col6)  # type: ignore
        self.variaveis_alu()
        query = "SELECT codEndereco FROM tbAluno WHERE codra = %s"
        self.result = mainapp.db.consultar_query(
            query=query, var=(self.codra, ))
        self.codendereco = str(self.result[0][0])  # type:ignore
        queryend = """
                SELECT cep, estado, cidade, bairro, logradouro, numero
                FROM tbEndereco
                WHERE codEndereco = %s
        """
        self.result_list = []
        self.result_list = mainapp.db.consultar_query(
            queryend, (self.codendereco, ))
        self.campos_endereco = self.result_list

        c = 0
        for v in self.campos_endereco[0]:
            match c:
                case 0:
                    self.ent_cep.insert(tk.END, v)
                    c += 1
                case 1:
                    self.ent_estado.set(str(v))
                    c += 1
                case 2:
                    self.ent_cidade.insert(tk.END, v)
                    c += 1
                case 3:
                    self.ent_bairro.insert(tk.END, v)
                    c += 1
                case 4:
                    self.ent_logradouro.insert(tk.END, v)
                    c += 1
                case 5:
                    self.ent_numero.insert(tk.END, v)

        self.montar_lista_tel(col1)
    # !SECTION - Method: on_doubleclick_aluno
    # SECTION - Method: montar_lista_tel

    def montar_lista_tel(self, ra):
        self.lista_tel.delete(*self.lista_tel.get_children())

        self.lb_sel_alu.configure(text=f'Aluno: {self.nome}', fg_color='green')

        querytel = """SELECT t.prioridade, t.numero
                        FROM tbtelefone t
                        JOIN tbAluno_has_tbtelefone aht
                        ON t.codtelefone = aht.codtelefone
                        JOIN tbaluno a ON aht.codra = a.codra
                        where a.codra = %s
                        ORDER BY t.prioridade ;
                        """

        self.lista_tel_result = mainapp.db.consultar_query(
            querytel, (ra,)
        )

        for i in self.lista_tel_result:
            self.lista_tel.insert(
                "", tk.END, values=(i[0], i[1]))  # type:ignore
    # !SECTION - Method: montar_lista_tel
    # SECTION - Method: buscar_aluno

    def buscar_aluno(self):
        self.variaveis_alu()

        querrybusca = """
                SELECT a.codRA,
                a.nome,
                a.cpf,
                date_format(a.data_nasc, '%d/%m/%Y'),
                a.email,
                a.statusmatricula,
                c.nome
                FROM tbaluno a
                JOIN tbCurso c
                ON a.codCurso = c.codCurso
                JOIN tbEndereco e
                ON e.codEndereco = a.codEndereco
            """
        where = []
        values = []

        if self.codra:
            where.append("a.codRA = %s")
            values.append(self.codra)
        if self.nome:
            where.append("a.nome LIKE %s")
            values.append(f'%{self.nome}%')
        if self.cpf:
            where.append("a.cpf LIKE %s")
            values.append(f'%{self.cpf}%')
        if self.data_nasc_format:
            where.append("a.data_nasc LIKE %s")
            values.append(f"{self.data_nasc_format}")
        if self.email:
            where.append("a.email LIKE %s")
            values.append(f'%{self.email}%')
        if self.status_matricula:
            where.append("a.statusmatricula LIKE %s")
            values.append(self.status_matricula)
        if self.curso:
            where.append("c.nome LIKE %s")
            values.append(f'%{self.curso}%')
        if self.cep:
            where.append("e.cep LIKE %s")
            values.append(f'%{self.cep}%')
        if self.estado:
            where.append("e.estado LIKE %s")
            values.append(self.estado)
        if self.cidade:
            where.append("e.cidade LIKE %s")
            values.append(f'%{self.cidade}%')
        if self.bairro:
            where.append("e.bairro LIKE %s")
            values.append(f"%{self.bairro}%")
        if self.logradouro:
            where.append("e.logradouro LIKE %s")
            values.append(f"%{self.logradouro}%")
        if self.numero:
            where.append("e.numero LIKE %s")
            values.append(f"%{self.numero}%")

        if where:
            querrybusca += " WHERE " + " AND ".join(where)
            querrybusca += " ORDER BY a.nome ;"

        self.lista_alu_busca = mainapp.db.consultar_query(querrybusca, values)

        self.lista_alu.delete(*self.lista_alu.get_children())
        for i in self.lista_alu_busca:
            self.lista_alu.insert("", tk.END, values=(i))  # type:ignore
    # !SECTION - Method: buscar_aluno
    # SECTION - Method: add_aluno

    def add_aluno(self):
        """
        Adiciona os dados de um novo aluno no banco de dados
        """
        self.variaveis_alu()
        lista_campos = []
        if not self.nome:
            lista_campos.append("nome")
        if not self.cpf:
            lista_campos.append("cpf")
        if not self.email:
            lista_campos.append("email")
        if not self.status_matricula:
            lista_campos.append("status da matricula")
        if not self.data_nasc:
            lista_campos.append("data de Nascimento")
        if not self.cep:
            lista_campos.append("cep")
        if not self.estado:
            lista_campos.append("estado")
        if not self.cidade:
            lista_campos.append("cidade")
        if not self.bairro:
            lista_campos.append("bairro")
        if not self.logradouro:
            lista_campos.append("logradouro")
        if not self.numero:
            lista_campos.append("número")
        if not self.curso:
            lista_campos.append("Curso")

        if lista_campos:
            messagebox.showerror(title='campos invalidos',
                                 message=f"Os campos {lista_campos}, são obrigatórios")  # noqa
        else:

            querry_end = """
                INSERT INTO tbEndereco (cep, estado, cidade, bairro,
                logradouro, numero)
                VALUES (%s, %s, %s, %s, %s, %s)
                        """
            mainapp.db.executar_querry(querry_end,
                                       (self.cep, self.estado, self.cidade,
                                        self.bairro, self.logradouro,
                                        self.numero))
            lastcodend = mainapp.db.last_id

            querry_codcurso = """
                SELECT codCurso FROM tbCurso WHERE nome like %s
                            """
            codcurso = mainapp.db.consultar_query(
                querry_codcurso, (f'%{self.curso}%', ))[0][0]  # type: ignore

            querry_add = """
            INSERT INTO tbaluno (nome, cpf, email, statusmatricula,
            data_nasc, codendereco, codcurso)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            mainapp.db.executar_querry(querry_add,
                                       (self.nome, self.cpf, self.email,
                                        self.status_matricula,
                                        self.data_nasc_format,
                                        lastcodend, codcurso))
            messagebox.showinfo(
                title='Sucesso',
                message=f'Aluno {self.nome} foi adicionado com sucesso.'
            )
        # TODO - fazer aparecer apenas o aluno adicionado ao final
        self.montar_lista_alu()

    # !SECTION - Method: add_aluno
    # SECTION - Method: excluir_aluno

    def excluir_aluno(self):
        self.variaveis_alu()
        if self.codra:
            msg = messagebox.askyesno(
                title="Deletar",
                message=f"""VOCÊ TEM CERTEZA QUE QUER DELETAR O ALUNO:
                                          {self.nome} CodRA = {self.codra}""")
            if msg is True:

                querry_del = """
                DELETE from tbaluno WHERE codra = %s
                """
                mainapp.db.executar_querry(querry_del, (self.codra,))
                self.montar_lista_alu()
                messagebox.showinfo(
                    title='Sucesso',
                    message=f'Aluno {self.nome} apagado com sucesso'
                )
            else:
                messagebox.showerror(
                    title="ERRO",
                    message=f'CodRA: {self.codra} NÃO foi excluido ')
        else:
            messagebox.showwarning(
                title="Deletar",
                message="CodRA não selecionado")

    # !SECTION - Method: excluir_aluno
    # SECTION - Method: add_tel_aluno
    def add_tel_aluno(self):
        self.variaveis_alu()

        if not self.codra:
            msg = """
                    Não há CodRA selecionado,
                    Verifique o campo CodRA e tente novamente"""
            messagebox.showerror(
                title='ERRO',
                message=f'{msg}'
            )
        else:
            querrytel = """
                        INSERT INTO tbTelefone
                        (numero, prioridade)
                        VALUES (%s, %s)"""
            values = (self.telefone, self.prioridade)

            mainapp.db.executar_querry(query=querrytel,
                                       value=values)

            codTel = mainapp.db.last_id

            querryaht = """
                        INSERT INTO tbAluno_has_tbTelefone
                        (codRa, codTelefone)
                        VALUES (%s, %s)"""
            valuesaht = (self.codra, codTel)

            mainapp.db.executar_querry(query=querryaht,
                                       value=valuesaht)
            self.montar_lista_tel(self.codra)
            messagebox.showinfo(
                title='Sucesso',
                message=f"""O numero {self.telefone},
                foi adicionado ao aluno {self.nome} """
            )
    # !SECTION - Method: add_tel_aluno
    # SECTION - Method: ondoubleclick_alu_tel

    def ondoubleclick_alu_tel(self, event):
        self.apagar_campos_tel()
        self.lista_tel.selection()
        for n in self.lista_tel.selection():
            col1, col2 = self.lista_tel.item(
                n, 'values'
            )
            self.ent_prioridade.set(col1)
            self.ent_telefone.insert(tk.END, col2)
    # !SECTION - Method: ondoubleclick_alu_tel

    # SECTION - Method: excluir_tel_alu
    def excluir_tel_alu(self):
        self.variaveis_alu()
        if self.telefone:
            querry_select = """
                        SELECT t.codTelefone FROM tbTelefone t
                        JOIN tbAluno_has_tbTelefone aht
                        ON aht.codTelefone = t.codTelefone
                        WHERE aht.codRa = %s AND t.numero = %s"""
            values = (self.codra, self.telefone)
            resultado = mainapp.db.consultar_query(querry_select, values)[0]
            print(resultado)
            querry_del = """
                    DELETE FROM tbTelefone WHERE codTelefone = %s"""

            executar = mainapp.db.executar_querry(
                querry_del, resultado)  # type: ignore
            if executar is True:
                messagebox.showinfo(
                    title='Sucesso',
                    message=f'Telefone: {self.telefone} apagado com sucesso'
                )
                self.montar_lista_tel(self.codra)
            else:
                messagebox.showerror(
                    title="ERRO",
                    message="O telefone não pode ser apagado"
            )
        else:
            messagebox.showerror(
                    title="ERRO",
                    message="Selecione ou digite um numero de telefone"
            )
    # !SECTION - Method: excluir_tel_alu
# !SECTION - Class: Aluno_tab

# SECTION - Class: Cadastro


class Cadastro(ctk.CTkFrame):
    """Classe que representa o frame que define Cadastro."""
    # SECTION - Init

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.create_widgets()
        self.create_layout()
    # !SECTION - Init
    # SECTION - Method: create_widgets

    def create_widgets(self):
        """Criação dos widgets de Cadastro, é chamado no __init__."""

        self.cadastro_tree = ctk.CTkTabview(self, anchor='nw')
        self.alunotab = self.cadastro_tree.add("Aluno")
        self.professortab = self.cadastro_tree.add("Professor")
        self.deptab = self.cadastro_tree.add("Departamento")
        self.discitab = self.cadastro_tree.add("Disciplina")
        self.turmatab = self.cadastro_tree.add("Turma")
        self.frame_aluno = Aluno_tab(master=self.alunotab)
    # !SECTION - Method: create_widgets
    # SECTION - Method: create_layout

    def create_layout(self):
        """Criação do layout dos widgets de Cadastro, é chamado no __init__."""

        self.cadastro_tree.place(relx=0.02, rely=0.01,
                                 relwidth=0.96, relheight=0.95)
        self.frame_aluno.pack()
    # !SECTION - Method: create_layout
# !SECTION - Class: Cadastro

# SECTION - Class: Banco_de_dados


class Banco_de_dados(ctk.CTkFrame):
    """Classe que representa o frame que define a tela Banco de Dados."""
    # SECTION - Init

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        # Variáveis para os parâmetros do banco de dados

        self.create_widgets()
        self.create_layout()
    # !SECTION - Init
    # SECTION - Method: create_widgets

    def create_widgets(self):
        """Criação dos widgets da tela Banco de dados, é chamado no __init__."""  # noqa

        self.frame_bd = ctk.CTkFrame(self,
                                     fg_color='gray24',
                                     border_width=2)
        self.title_bd = Label('Banco de Dados', master=self.frame_bd)
        self.title_bd.configure(font=('Helvetica', 25))

        self.tipo_bd_var = ctk.StringVar()

        self.lb_tipo_bd = Label('Tipo', master=self.frame_bd)
        self.ent_tipo_bd = ctk.CTkComboBox(
            self.frame_bd,
            variable=self.tipo_bd_var,
            justify='center',
            values=['Mysql',
                    'SQLite']
        )
        self.tipo_bd_var.trace_add('write', callback=self.att_frame_bd_sub)
        # self.ent_tipo_bd.bind("<<ComboboxSelected>>", self.att_frame_bd_sub)

        self.frame_bd_mysql = ctk.CTkFrame(self.frame_bd,
                                           fg_color='grey',
                                           border_width=2)
    # !SECTION - Method: create_widgets
    # SECTION - Method: create_sub_widgets

    def create_sub_widgets(self, tipo: str):
        """
        Cria os widgets do banco de dados de acordo com o tipo de banco de dados. # noqa

        args:
            tipo: STR que define o tipo do banco de dados
        TODO: Implementar o tipo SQL.
        """
        if self.frame_bd_mysql:
            for widget in self.frame_bd_mysql.winfo_children():
                widget.destroy()

        if tipo == "Mysql" or tipo is None:
            self.lb_mysq = Label("Mysql", master=self.frame_bd_mysql)
            self.lb_mysq.configure(font=('Helvetica', 20))
            self.lb_mysq.place(relx=0.5, rely=0.1, anchor='c')

            self.lb_host_bd = Label('Host', master=self.frame_bd_mysql)
            self.lb_host_bd.place(relx=0.15, rely=0.25, anchor='c')

            self.ent_host_bd = Entry(
                master=self.frame_bd_mysql,
                textvariable=self.master.db_params['host']  # type:ignore
            )
            self.ent_host_bd.place(relx=0.5, rely=0.25, anchor='c')

            self.lb_user_bd = Label('User', master=self.frame_bd_mysql)
            self.lb_user_bd.place(relx=0.15, rely=0.4, anchor='c')

            self.ent_user_bd = Entry(
                master=self.frame_bd_mysql,
                textvariable=self.master.db_params['user']  # type:ignore
            )
            self.ent_user_bd.place(relx=0.5, rely=0.4, anchor='c')

            self.lb_senha_bd = Label(
                'Password', master=self.frame_bd_mysql)
            self.lb_senha_bd.place(relx=0.15, rely=0.55, anchor='c')

            self.ent_senha_bd = Entry(
                master=self.frame_bd_mysql,
                textvariable=self.master.db_params['password'],  # type:ignore
                show='*'
            )
            self.ent_senha_bd.place(relx=0.5, rely=0.55, anchor='c')

            self.lb_nome_bd = Label(
                'Nome do Banco', master=self.frame_bd_mysql)
            self.lb_nome_bd.place(relx=0.15, rely=0.70, anchor='c')

            self.ent_nome_bd = Entry(
                master=self.frame_bd_mysql,
                textvariable=self.master.db_params['nome'])  # type:ignore
            self.ent_nome_bd.place(relx=0.5, rely=0.70, anchor='c'
                                   )

            self.btn_testar_bd = Btn(
                'Testar',
                master=self.frame_bd_mysql,
                command=self.master.db.teste_bd  # type:ignore
            )
            self.btn_testar_bd.place(relx=0.85, rely=0.4,
                                     relwidth=0.2, anchor='c')

            self.btn_salvar_bd = Btn('Salvar', master=self.frame_bd_mysql,
                                     command=self.salvar_params)
            self.btn_salvar_bd.place(relx=0.85, rely=0.6,
                                     relwidth=0.2, anchor='c')
        else:
            self.lb_default = Label('Selecione uma opção',
                                    master=self.frame_bd_mysql)
            self.lb_default.pack()
    # !SECTION - Method: create_sub_widgets
    # SECTION - Method: att_frame_bd_sub

    def att_frame_bd_sub(self, var, index, mode):
        """TODO: entender para fazer DocSting"""
        self.tipo = self.ent_tipo_bd.get()
        self.create_sub_widgets(self.tipo)
    # !SECTION - Method: att_frame_bd_sub
    # SECTION - Method: create_layout

    def create_layout(self):
        """Criação do layout dos widgets da tela Banco de dados, é chamado no __init__."""  # noqa

        self.frame_bd.place(relx=0.5, rely=0.5,
                            relwidth=0.4, relheight=0.5,
                            anchor='c')
        self.title_bd.place(relx=0.5, rely=0.1,
                            anchor='c')
        self.lb_tipo_bd.place(relx=0.05, rely=0.20, anchor='c')
        self.lb_tipo_bd.configure(font=('Helvetica', 15))

        self.ent_tipo_bd.place(relx=0.3, rely=0.20, anchor='c')

        self.frame_bd_mysql.place(relx=0.15, rely=0.3,
                                  relwidth=0.7, relheight=0.6,)
    # !SECTION Method: create_layout
    # SECTION - Method: salvar_params

    def salvar_params(self):
        """Salva os parametros do Banco de dados em no arquivo db_config.json."""  # noqa
        try:
            with open('db_config.json', 'w') as f:
                json.dump({
                    'tipo': self.ent_tipo_bd.get(),
                    'host': self.ent_host_bd.get(),
                    'user': self.ent_user_bd.get(),
                    'password': self.ent_senha_bd.get(),
                    'nome': self.ent_nome_bd.get()

                }, f)
                messagebox.showinfo(title='Sucesso',
                                    message='Configurações salvas')

        except Exception as e:
            messagebox.showerror(
                title="Erro ao salvar as configurações", message=f'{e}')
    # !SECTION - Method: salvar_params
# !SECTION - Class: Banco de dados
# SECTION - Class: Sobre


class Sobre(ctk.CTkFrame):
    """Classe que representa o frame que define a tela Sobre."""

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        lb = ctk.CTkLabel(self, text="Sobre")
        lb.pack(expand=True, fill='both', padx=20, pady=20)
# !SECTION - class: Sobre
# SECTION - class: DataBase


class DataBase(Controlador_db):
    """
    Classe que herda de Controlador_db, para intermediar o acesso ao banco de dados # noqa

    Args:
        host: STR que indica o nome do host do banco de dados
        user: STR que indica o nome do user do banco de dados
        password: STR que indica a senha do banco de dados
        database: STR que indica o nome do banco de dados
    """

    def __init__(self, host: str, user: str, password: str, database: str) -> None:  # noqa
        super().__init__(host, user, password, database)
        self.host = host
        self.user = user
        self.password = password
        self.database = database
# !SECTION - class: DataBase


if __name__ == '__main__':
    mainapp = App('Login', (500, 500))
    mainapp.mainloop()
