import customtkinter as ctk  # type:ignore
from mysql.connector import connect
from tkcalendar import DateEntry  # type:ignore
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
import traceback
import brazilcep


janela = ctk.CTk()

# SECTION - Funções


class Funcs():
    # SECTION - Banco de Dados
    def conecta_bd(self):
        self.conn = connect(
            host="localhost",
            user="root",
            password="Ricardo&Danubia",
            db='dbricardo')
        self.cursor = self.conn.cursor()
        print("Conectado ao banco de dados")
        self.cursor.execute("USE dbricardo;")

    def desconecta_bd(self):
        self.conn.close()
        print("Desconectado do banco de dados")
    # !SECTION - Banco de dados

    def montar_dic_cursos(self):
        self.conecta_bd()
        self.cursor.execute(
            """SELECT codCurso, nome FROM tbCurso""")
        self.dic_cursos = {}
        for (codCurso, nome) in self.cursor:
            self.dic_cursos[nome] = codCurso
        print(self.dic_cursos)
        self.desconecta_bd()

    def pegar_cpf(self):
        self.entry_estado.set("")
        self.entry_cidade.delete("0", tk.END)
        self.entry_bairro.delete("0", tk.END)
        self.entry_logradouro.delete("0", tk.END)
        self.entry_numero.delete("0", tk.END)
        zipcode = self.entry_cep.get()
        dados_cep = brazilcep.get_address_from_cep(zipcode)
        print(dados_cep)
        self.entry_estado.set(dados_cep['uf'])
        self.entry_cidade.insert(tk.END, dados_cep['city'])
        self.entry_bairro.insert(tk.END, dados_cep['district'])
        self.entry_logradouro.insert(tk.END, dados_cep['street'])
    # SECTION - Funções Aluno

    def variaveis_aluno(self):
        self.codra = self.entry_codra.get()  # type: ignore
        self.nome = self.entry_nome.get()  # type: ignore
        self.cpf = self.entry_cpf.get()  # type: ignore
        self.data_nasc = self.entry_data_nasc.get()  # type: ignore
        self.email = self.entry_email.get()  # type: ignore
        self.status_matricula = self.entry_status_matricula.get()  # noqa # type: ignore
        self.curso = self.entry_curso.get()  # type: ignore
        self.estado = self.entry_estado.get()  # type: ignore
        self.cidade = self.entry_cidade.get()  # type: ignore
        self.bairro = self.entry_bairro.get()  # type: ignore
        self.cep = self.entry_cep.get()  # type: ignore
        self.logradouro = self.entry_logradouro.get()  # type: ignore
        self.numero = self.entry_numero.get()  # type: ignore
        print(self.data_nasc)

        if self.curso:
            self.cod_curso = self.dic_cursos[self.curso]

    def select_listas_aluno(self):
        self.lista_alu.delete(*self.lista_alu.get_children())  # type: ignore
        self.conecta_bd()
        try:
            QuerryA = """ SELECT a.codra,
                    a.nome,
                    a.cpf,
                    date_format(a.data_nasc, '%d/%m/%y'),
                    a.email,
                    a.statusmatricula,
                    c.nome
                    FROM tbaluno a
                    JOIN tbcurso c
                    ON c.codCurso = a.codcurso
                    ORDER BY a.nome;
                    """

            self.cursor.execute(QuerryA)
            listaA = self.cursor.fetchall()

            for i in listaA:
                self.lista_alu.insert("", tk.END, values=i)  # type: ignore
        except Exception as e:
            messagebox.showerror(
                title="Erro ao iniciar a tabela", message=f'{e}')
        finally:
            self.desconecta_bd()

    def select_listatel_aluno(self, ra):
        try:
            self.variaveis_aluno()
            self.lista_tel.delete(  # type: ignore
                *self.lista_tel.get_children())  # type: ignore

            self.conecta_bd()
            QuerryT = """SELECT t.prioridade, t.numero
                        FROM tbtelefone t
                        JOIN tbAluno_has_tbtelefone aht
                        ON t.codtelefone = aht.codtelefone
                        JOIN tbaluno a ON aht.codra = a.codra
                        where a.codra = %s
                        ORDER BY t.prioridade ;
                        """
            self.cursor.execute(QuerryT, (ra,))

            ListaT = self.cursor.fetchall()
            for i in ListaT:
                self.lista_tel.insert(  # type: ignore
                    "", tk.END, values=(i[0], i[1]))  # type: ignore
        except Exception as e:
            messagebox.showerror(
                title="Erro carregar tabela telefone", message=f'{e}')
        finally:
            self.desconecta_bd()

    def apagar_campos_aluno(self):

        self.entry_codra.delete('0', tk.END)  # type: ignore
        self.entry_nome.delete('0', tk.END)  # type: ignore
        self.entry_cpf.delete('0', tk.END)  # type: ignore
        self.entry_data_nasc.delete('0', tk.END)  # type: ignore
        self.entry_email.delete('0', tk.END)  # type: ignore
        self.entry_status_matricula.set('')  # type: ignore
        self.entry_curso.set('')  # type: ignore
        self.entry_estado.set('')  # type: ignore
        self.entry_cidade.delete('0', tk.END)  # type: ignore
        self.entry_bairro.delete('0', tk.END)  # type: ignore
        self.entry_cep.delete('0', tk.END)  # type: ignore
        self.entry_logradouro.delete('0', tk.END)  # type: ignore
        self.entry_numero.delete('0', tk.END)  # type: ignore
        self.entry_telefone.delete('0', tk.END)  # type: ignore
        self.entry_prioridade.set('')  # type: ignore

        if self.lista_tel:  # type: ignore
            self.lista_tel.delete(  # type: ignore
                *self.lista_tel.get_children())  # type: ignore

    def OnDoubleClick_aluno(self, event):
        self.apagar_campos_aluno()
        self.variaveis_aluno()
        self.lista_alu.selection()  # type: ignore
        for n in self.lista_alu.selection():  # type: ignore
            col1, col2, col3, col4, col5, col6, col7 = self.lista_alu.item(  # noqa # type: ignore
                n, 'values')

            self.entry_codra.insert(tk.END, col1)  # type: ignore
            self.entry_nome.insert(tk.END, col2)  # type: ignore
            self.entry_cpf.insert(tk.END, col3)  # type: ignore
            self.entry_data_nasc.set_date(col4)  # type: ignore
            self.entry_email.insert(tk.END, col5)  # type: ignore
            self.entry_curso.set(col7)  # type: ignore
            # FIXME - PUXAR LISTA DO BANCO DE DADOS
            self.entry_status_matricula.set(col6)  # type: ignore
        try:
            self.conecta_bd()
            self.cursor.execute(("""SELECT codEndereco FROM tbaluno
                                WHERE codra = %s"""), (col1,))
            codEndereco = self.cursor.fetchone()

            self.cursor.execute(("""SELECT cep, estado, cidade, bairro,
                                logradouro, numero 
                                FROM tbEndereco
                                WHERE codEndereco = %s"""), codEndereco)   # noqa # type: ignore
            campos_endereco = self.cursor.fetchall()

            c = 0
            for v in campos_endereco[0]:
                match c:
                    case 0:
                        self.entry_cep.insert(tk.END, v)  # type: ignore
                        c += 1
                    case 1:
                        self.entry_estado.set(v)  # type: ignore
                        c += 1
                    case 2:
                        self.entry_cidade.insert(tk.END, v)  # type: ignore
                        c += 1
                    case 3:
                        self.entry_bairro.insert(tk.END, v)  # type: ignore
                        c += 1
                    case 4:
                        self.entry_logradouro.insert(tk.END, v)  # type: ignore
                        c += 1
                    case 5:
                        self.entry_numero.insert(tk.END, v)  # type: ignore
            self.select_listatel_aluno(col1)
        except Exception as e:
            messagebox.showerror(
                title="Erro carregar tabela enderecos", message=f'{e}')
            traceback.print_exception
        finally:
            self.desconecta_bd()
        # self.indiceCurso = list(self.dicCursos.keys()).index(col8)
        # self.entry_curso.set(list(self.dicCursos.keys())[self.indiceCurso])

    def buscar_aluno(self):
        self.variaveis_aluno()
        self.montar_dic_cursos()
        self.conecta_bd()

        querrybusca = """
                SELECT a.codRA,
                a.nome,
                a.cpf,
                date_format(a.data_nasc, '%d/%m/%y'),
                a.email,
                a.statusmatricula,
                c.nome
                FROM tbaluno a
                JOIN tbCurso c
                ON a.codCurso = c.codCurso
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
        if self.data_nasc:
            self.data_nasc_obj = datetime.strptime(
                self.data_nasc, "%d/%m/%Y")
            self.data_nasc_format = self.data_nasc_obj.strftime("%Y-%m-%d")
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

        if where:
            querrybusca += " WHERE " + " AND ".join(where)
            querrybusca += " ORDER BY a.nome ;"

        self.cursor.execute(querrybusca, tuple(values))
        lista_busca = self.cursor.fetchall()

        self.lista_alu.delete(*self.lista_alu.get_children())
        for i in lista_busca:
            self.lista_alu.insert("", tk.END, values=i)

        print(querrybusca)
        print(values)
        self.desconecta_bd()
        # !SECTION - Funções Aluno
        # !SECTION - Funções

        # SECTION - APP(Classe)
        # SECTION - __INIT__


class App(Funcs):
    def __init__(self) -> None:
        self.janela = janela
        self.frame_atual = None
        self.menu()
        self.exibir_cadastro()

        janela.mainloop()

# !SECTION - __INIT__
# SECTION - Menu
# Menu

    def menu(self):
        self.frame_menu = ctk.CTkFrame(self.janela,
                                       border_width=2,
                                       border_color='gray',
                                       fg_color='black',
                                       )
        self.frame_menu.place(relx=0, rely=0, relwidth=0.1, relheight=1)
        self.btn_login = ctk.CTkButton(self.frame_menu,
                                       text="Login",
                                       command=self.exibir_login)
        self.btn_login.place(relx=0.5, rely=0.1, anchor='center')

        self.btn_cadastro = ctk.CTkButton(self.frame_menu,
                                          text="Cadastro",
                                          command=self.exibir_cadastro)
        self.btn_cadastro.place(relx=0.5, rely=0.15, anchor='center')

        self.btn_base_de_dados = ctk.CTkButton(self.frame_menu,
                                               text="Banco de dados",
                                               command=self.exibir_inicial)
        self.btn_base_de_dados.place(relx=0.5, rely=0.2, anchor='center')
        # TODO Opções de criaçao e config do banco dedados em mysql (e sqlite?)
        self.btn_sobre = ctk.CTkButton(self.frame_menu,
                                       text='Sobre',
                                       command=self.exibir_inicial)
        self.btn_sobre.place(relx=0.5, rely=0.25, anchor='c')
# !SECTION - Menu
# SECTION - Cadastro

    def tela_cadastro(self):
        self.janela.title("cadastro")
        self.janela.minsize(width=700, height=500)

    def exibir_cadastro(self):
        if self.frame_atual is not None:
            self.frame_atual.destroy()

        self.frame_atual = ctk.CTkFrame(self.janela)
        self.frame_atual.place(relx=0.1, rely=0, relwidth=0.9, relheight=1)

        self.montar_dic_cursos()
        self.tela_cadastro()
        self.frames_cadastro()
        self.widgets_alunos()
        self.select_listas_aluno()
    # SECTION - Frames - Cadastro

    def frames_cadastro(self):
        self.cadastroTree = ctk.CTkTabview(self.frame_atual,
                                           anchor='nw')
        self.cadastroTree.place(relx=0.02, rely=0.01,
                                relwidth=0.96, relheight=0.95)
        self.alunotab = self.cadastroTree.add("Aluno")
        self.professortab = self.cadastroTree.add("Professor")
        self.deptab = self.cadastroTree.add("Departamento")
        self.discitab = self.cadastroTree.add("Disciplina")
        self.turmatab = self.cadastroTree.add("Turma")

        self.frame_cadastro_aluno = ctk.CTkFrame(master=self.alunotab,
                                                 fg_color="gray48")
        self.frame_cadastro_aluno.pack(fill="both", expand=True)

        self.frame_cadastro_professor = ctk.CTkFrame(master=self.professortab,
                                                     fg_color="gray36")
        self.frame_cadastro_professor.pack(fill="both", expand=True)

        self.frame_cadastro_dep = ctk.CTkFrame(self.deptab,
                                               fg_color="gray27")
        self.frame_cadastro_dep.pack(fill="both", expand=True)

        self.frame_cadastro_disci = ctk.CTkFrame(self.discitab,
                                                 fg_color="gray68")
        self.frame_cadastro_disci.pack(fill="both", expand=True)

        self.frame_cadastro_turma = ctk.CTkFrame(self.turmatab,
                                                 fg_color="gray78")
        self.frame_cadastro_turma.pack(fill='both', expand=True)
    # !SECTION - Frames - Cadastro
    # SECTION - Widgets - Cadastro

    def widgets_alunos(self):
        # Titulo
        self.titulo = ctk.CTkLabel(self.frame_cadastro_aluno,
                                   text="Cadastro aluno",
                                   font=("Helvetica", 25),
                                   fg_color="transparent",
                                   )
        self.titulo.place(anchor='center', relx=0.5, rely=0.05)
        # SECTION - Labels e Entrys
        # Label e entrada dos atributos
        self.label_codra = ctk.CTkLabel(self.frame_cadastro_aluno,
                                        text="CodRA",
                                        fg_color='transparent')
        self.label_codra.place(relx=0.06, rely=0.12,
                               relwidth=0.2, anchor='c')

        self.entry_codra = ctk.CTkEntry(self.frame_cadastro_aluno,
                                        fg_color="white",
                                        text_color='black')
        self.entry_codra.place(relx=0.11, rely=0.1, relwidth=0.05)

        self.label_nome = ctk.CTkLabel(self.frame_cadastro_aluno,
                                       text=('Nome'),
                                       fg_color='transparent')
        self.label_nome.place(relx=0.06, rely=0.16,
                              relwidth=0.2, anchor='c')

        self.entry_nome = ctk.CTkEntry(self.frame_cadastro_aluno,
                                       fg_color="white",
                                       text_color='black')
        self.entry_nome.place(relx=0.11, rely=0.14, relwidth=0.16)

        self.label_cpf = ctk.CTkLabel(self.frame_cadastro_aluno,
                                      text=('CPF'),
                                      fg_color='transparent')
        self.label_cpf.place(relx=0.06, rely=0.2,
                             relwidth=0.2, anchor='c')

        self.entry_cpf = ctk.CTkEntry(self.frame_cadastro_aluno,
                                      fg_color="white",
                                      text_color='black')
        self.entry_cpf.place(relx=0.11, rely=0.18, relwidth=0.08)

        self.label_data_nasc = ctk.CTkLabel(self.frame_cadastro_aluno,
                                            text=('Data de Nascimento'),
                                            fg_color='transparent')
        self.label_data_nasc.place(relx=0.06, rely=0.24,
                                   relwidth=0.2, anchor='c')

        self.entry_data_nasc = DateEntry(self.frame_cadastro_aluno,
                                         locale="pt_BR",
                                         year=2000,
                                         month=1,
                                         day=1)
        self.entry_data_nasc.place(relx=0.112, rely=0.225, relwidth=0.06)

        self.label_email = ctk.CTkLabel(self.frame_cadastro_aluno,
                                        text=('Email'),
                                        fg_color='transparent')
        self.label_email.place(relx=0.06, rely=0.28, relwidth=0.2, anchor='c')

        self.entry_email = ctk.CTkEntry(self.frame_cadastro_aluno,
                                        fg_color='white',
                                        text_color='black')
        self.entry_email.place(relx=0.11, rely=0.26, relwidth=0.15)
        self.label_status_matricula = ctk.CTkLabel(self.frame_cadastro_aluno,
                                                   text=(
                                                       'Status da matricula'),
                                                   fg_color='transparent')
        self.label_status_matricula.place(relx=0.06, rely=0.32,
                                          relwidth=0.2, anchor='c')

        self.entry_status_matricula = ctk.CTkComboBox(
            self.frame_cadastro_aluno,
            fg_color="white",
            text_color='black',
            values=['Ativa',
                    'Inativa',
                    'Trancado'])
        self.entry_status_matricula.set('')
        self.entry_status_matricula.place(relx=0.11, rely=0.30, relwidth=0.08)

        # Labels e entradas endereço
        # SECTION - Endereço
        self.label_cep = ctk.CTkButton(self.frame_cadastro_aluno,
                                       fg_color='transparent',
                                       border_color='green',
                                       border_width=1,
                                       command=self.pegar_cpf,
                                       text='CEP')
        self.label_cep.place(relx=0.29, rely=0.12, anchor='c')

        self.entry_cep = ctk.CTkEntry(self.frame_cadastro_aluno,
                                      fg_color='white',
                                      text_color='black')
        self.entry_cep.place(relx=0.32, rely=0.1, relwidth=0.07)

        self.label_estado = ctk.CTkLabel(self.frame_cadastro_aluno,
                                         text="Estado",
                                         fg_color="transparent")
        self.label_estado.place(relx=0.29, rely=0.16, anchor='c')

        self.entry_estado = ctk.CTkComboBox(self.frame_cadastro_aluno,
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
        self.entry_estado.set('')
        self.entry_estado.place(relx=0.32, rely=0.14, relwidth=0.045)

        self.label_cidade = ctk.CTkLabel(self.frame_cadastro_aluno,
                                         fg_color='transparent',
                                         text="Cidade")
        self.label_cidade.place(relx=0.29, rely=0.20, anchor='c')

        self.entry_cidade = ctk.CTkEntry(self.frame_cadastro_aluno,
                                         fg_color='white',
                                         text_color='black')
        self.entry_cidade.place(relx=0.32, rely=0.18, relwidth=0.1)

        self.label_bairro = ctk.CTkLabel(self.frame_cadastro_aluno,
                                         fg_color='transparent',
                                         text='Bairro')
        self.label_bairro.place(relx=0.29, rely=0.24, anchor='c')

        self.entry_bairro = ctk.CTkEntry(self.frame_cadastro_aluno,
                                         fg_color='white',
                                         text_color='black')
        self.entry_bairro.place(relx=0.32, rely=0.22, relwidth=0.1)

        self.label_logradouro = ctk.CTkLabel(self.frame_cadastro_aluno,
                                             fg_color='transparent',
                                             text='Logradouro')
        self.label_logradouro.place(relx=0.29, rely=0.28, anchor='c')

        self.entry_logradouro = ctk.CTkEntry(self.frame_cadastro_aluno,
                                             fg_color='white',
                                             text_color='black',
                                             justify='center')
        self.entry_logradouro.place(relx=0.32, rely=0.26, relwidth=0.1)

        self.label_numero = ctk.CTkLabel(self.frame_cadastro_aluno,
                                         fg_color='transparent',
                                         text='Numero')
        self.label_numero.place(relx=0.29, rely=0.32, anchor='c')

        self.entry_numero = ctk.CTkEntry(self.frame_cadastro_aluno,
                                         fg_color='white',
                                         text_color='black')
        self.entry_numero.place(relx=0.32, rely=0.3, relwidth=0.1)
        # !SECTION - Endereço
        # !SECTION - Labels e Entrys
        # SECTION - Telefone
        # Frame, labels, botões e entradas de telefone
        self.tel_label = ctk.CTkLabel(self.frame_cadastro_aluno,
                                      text=("Telefones"),
                                      fg_color="gray27",
                                      )
        self.tel_label.place(relx=0.78, rely=0.1, relwidth=0.1, anchor='c')

        self.frame_tel = ctk.CTkFrame(self.frame_cadastro_aluno,
                                      fg_color='gray27',
                                      border_width=2,
                                      border_color='gray24',
                                      )
        self.frame_tel.place(relx=0.78, rely=0.225,
                             relwidth=0.3, relheight=0.2,
                             anchor='c')

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
        self.lista_tel.place(relx=0.01, rely=0.03,
                             relheight=0.94, relwidth=0.45)

        self.scrool_lista_tel = tk.Scrollbar(self.frame_tel,
                                             orient='vertical',
                                             command=self.lista_tel.yview)
        self.lista_tel.configure(yscrollcommand=self.scrool_lista_tel.set)
        self.scrool_lista_tel.place(
            relx=0.46, rely=0.03, relheight=0.94, relwidth=0.04)

        self.prioridade_label = ctk.CTkLabel(self.frame_tel,
                                             text=("Prioridade"),
                                             fg_color="transparent",
                                             )
        self.prioridade_label.place(relx=0.53, rely=0.05)

        self.entry_prioridade = ctk.CTkComboBox(self.frame_tel,
                                                fg_color="white",
                                                text_color="black",
                                                values=['1',
                                                        '2',
                                                        '3',
                                                        '4',
                                                        '5'])
        self.entry_prioridade.set('')
        self.entry_prioridade.place(relx=0.7, rely=0.05, relwidth=0.12)

        self.numero_label = ctk.CTkLabel(self.frame_tel,
                                         text=("Número"),
                                         fg_color="transparent",
                                         )
        self.numero_label.place(relx=0.53, rely=0.25)

        self.entry_telefone = ctk.CTkEntry(self.frame_tel,
                                           fg_color='white',
                                           text_color='black')
        self.entry_telefone.place(relx=0.7, rely=0.25, relwidth=0.28)

        self.btn_novo_tel = ctk.CTkButton(self.frame_tel,
                                          border_width=1,
                                          border_color='gray13',
                                          fg_color='gray67',
                                          text='novo'
                                          )
        self.btn_novo_tel.place(
            relx=0.58, rely=0.7, relwidth=0.1, anchor='c')

        self.btn_alterar_tel = ctk.CTkButton(self.frame_tel,
                                             border_width=1,
                                             border_color='gray13',
                                             fg_color='gray67',
                                             text='alterar')
        self.btn_alterar_tel.place(
            relx=0.72, rely=0.7, relwidth=0.15, anchor='c')

        self.btn_apagar_tel = ctk.CTkButton(self.frame_tel,
                                            border_width=1,
                                            border_color='gray13',
                                            fg_color='gray67',
                                            text='apagar')
        self.btn_apagar_tel.place(
            relx=0.89, rely=0.7, relwidth=0.15, anchor='c')
        # !SECTION - Telefone
        # SECTION - Entry Curso
        # Combobox Curso
        self.entry_curso = ctk.CTkComboBox(self.frame_cadastro_aluno,
                                           fg_color='white',
                                           text_color='black',
                                           values=list(self.dic_cursos.keys()),
                                           font=("Helvetica", 20),
                                           dropdown_font=("Helvetica", 20),
                                           justify='center')
        self.entry_curso.set('')
        self.entry_curso.place(relx=0.78, rely=0.4, anchor='c',
                               relwidth=0.3)
        # !SECTION - Entry Curso
        # SECTION - Foto
        # Foto
        self.foto_label = ctk.CTkLabel(self.frame_cadastro_aluno,
                                       text=("Foto"),
                                       fg_color="gray27",
                                       corner_radius=7)
        self.foto_label.place(relx=0.5, rely=0.105, relwidth=0.1, anchor='c')

        self.frame_foto = ctk.CTkFrame(self.frame_cadastro_aluno,
                                       fg_color='gray27',
                                       border_width=2,
                                       border_color='gray24',
                                       )
        self.frame_foto.place(relx=0.5, rely=0.23,
                              relwidth=0.1, relheight=0.18,
                              anchor='c')

        self.btn_foto = ctk.CTkButton(self.frame_cadastro_aluno,
                                      fg_color='grey84',
                                      text_color='black',
                                      text='Escolher foto')
        self.btn_foto.place(relx=0.5, rely=0.35, relwidth=0.08, anchor='c')
        # !SECTION - Foto

        # SECTION - BTN CRUD
        # Botoes Crud

        self.btn_limpar = ctk.CTkButton(self.frame_cadastro_aluno,
                                        text='Limpar',
                                        border_color='brown4',
                                        border_width=1,
                                        fg_color='gray22',
                                        text_color='black',
                                        command=self.apagar_campos_aluno)

        self.btn_limpar.place(relx=0.35, rely=0.38, relwidth=0.07)

        self.btn_buscar = ctk.CTkButton(self.frame_cadastro_aluno,
                                        text='Buscar',
                                        border_color='gray75',
                                        border_width=1,
                                        fg_color='gray22',
                                        text_color='black',
                                        command=self.buscar_aluno)

        self.btn_buscar.place(relx=0.45, rely=0.38, relwidth=0.07)

        self.btn_novo = ctk.CTkButton(self.frame_cadastro_aluno,
                                      text='Novo',
                                      border_color='green4',
                                      border_width=1,
                                      fg_color='gray22',
                                      text_color='black')

        self.btn_novo.place(relx=0.25, rely=0.38, relwidth=0.07)

        self.btn_alterar = ctk.CTkButton(self.frame_cadastro_aluno,
                                         text='Alterar',
                                         border_color='lightseagreen',
                                         border_width=1,
                                         fg_color='gray22',
                                         text_color='black')

        self.btn_alterar.place(relx=0.15, rely=0.38, relwidth=0.07)

        self.btn_excluir = ctk.CTkButton(self.frame_cadastro_aluno,
                                         text='Excluir',
                                         border_color='red1',
                                         border_width=1,
                                         fg_color='red4',
                                         text_color='white')

        self.btn_excluir.place(relx=0.05, rely=0.38, relwidth=0.07)
        # !SECTION - BTN CRUD
        # SECTION - Tabela Aluno
        self.lista_alu = ttk.Treeview(
            self.frame_cadastro_aluno,
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

        self.lista_alu.place(relx=0.08, rely=0.5,
                             relheight=0.5, relwidth=0.82)

        self.scrool_lista_alu = tk.Scrollbar(self.frame_cadastro_aluno,
                                             orient='vertical',
                                             command=self.lista_alu.yview)
        self.lista_alu.configure(yscrollcommand=self.scrool_lista_alu.set)
        self.scrool_lista_alu.place(
            relx=0.9, rely=0.5, relheight=0.5, relwidth=0.01)
        self.lista_alu.bind("<Double-1>", self.OnDoubleClick_aluno)
        # !SECTION - Tabela Aluno
    # !SECTION - Widgets - Cadastro
    # Tela inicial
    # !SECTION - Cadastro

    # SECTION - Tela Inicial
    # REVIEW - precisa?

    def tela_inicial(self):
        self.janela.title("Inicio")
        self.janela.minsize(width=700, height=500)

    def exibir_inicial(self):
        if self.frame_atual is not None:
            self.frame_atual.destroy()

        self.frame_atual = ctk.CTkFrame(self.janela)
        self.frame_atual.place(relx=0.1, rely=0, relwidth=0.9, relheight=1)

        self.tela_inicial()
        self.frames_inicial()
        self.widgets_inicial()

    def frames_inicial(self):
        self.frame_inicial = ctk.CTkFrame(self.frame_atual,
                                          border_width=5,
                                          border_color='darkgrey',
                                          fg_color='grey2')
        self.frame_inicial.place(relx=0.26, rely=0.15,
                                 relwidth=0.28, relheight=0.7)

    def widgets_inicial(self):
        # Titulo Inicial
        self.titulo_inicial = ctk.CTkLabel(self.frame_inicial,
                                           text="Projeto BD Universidade",
                                           fg_color="darkgrey",
                                           font=("Helvetica", 25))
        self.titulo_inicial.place(relx=0.5, rely=0.1, anchor='center')

    #    texto = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    #            Nam eget tempus mauris, molestie rutrum sapien.
    #            Cras sodales ut mi non mattis. Donec viverra, sapien vitae.
    #            tortor justo imperdiet nulla, ac sodales lectus sapien ut.
    #            Suspendisse ut orci sed turpis vestibulum maximus.
    #            Mauris in mattis odio, sollicitudin ultricies metus.
    #            Duis non auctor lacus. Aenean vitae pretium augue.
    #            Etiam imperdiet dui in ullamcorper eleifend.
    #            Quisque lobortis enim quis sem iaculis suscipit.
    #            Vivamus finibus nec enim non facilisis.
    #            """
        self.texto_inicial = ctk.CTkTextbox(self.frame_inicial,
                                            fg_color="darkgrey",
                                            font=("Helvetica", 18),
                                            )
        self.texto_inicial.place(
            relx=0.05, rely=0.2, relwidth=0.9, relheight=0.6)
    # !SECTION tela inicial
    # SECTION - Login

    def tela_login(self):
        self.janela.title("Login")
        self.janela.minsize(width=700, height=500)

    def exibir_login(self):
        if self.frame_atual is not None:
            self.frame_atual.destroy()

        self.frame_atual = ctk.CTkFrame(self.janela)
        self.frame_atual.place(relx=0.1, rely=0, relwidth=0.9, relheight=1)

        self.tela_login()
        self.frames_login()
        self.widgets_login()

    def frames_login(self):
        self.frame_login = ctk.CTkFrame(self.frame_atual,
                                        border_width=5,
                                        fg_color="darkgrey",
                                        )
        self.frame_login.place(relwidth=0.28, relheight=0.7,
                               relx=0.36, rely=0.15)

    def widgets_login(self):
        # Titulo login
        self.texto_login = ctk.CTkLabel(
            self.frame_login, text="Login", fg_color="darkgrey",
            text_color="grey10", font=('Helvetica', 35))
        self.texto_login.configure(justify="center")
        self.texto_login.pack(pady=50)

        # label e entradas usuario/senha

        self.lb_usuario = ctk.CTkLabel(
            self.frame_login, text="Usuário", fg_color="darkgrey",
            text_color="grey10", font=('Helvetica', 25))
        self.lb_usuario.pack(pady=20,)

        self.usuario_entry = ctk.CTkEntry(
            self.frame_login, fg_color='gray45', text_color='grey10',
            width=200, justify='center', font=('helvetica', 20), )
        self.usuario_entry.pack(pady=10)

        self.lb_senha = ctk.CTkLabel(
            self.frame_login, text="Senha", fg_color="darkgrey",
            text_color="grey10", font=('Helvetica', 25))
        self.lb_senha.pack(pady=20)

        self.senha_entry = ctk.CTkEntry(
            self.frame_login, fg_color='gray45', text_color='grey10',
            width=200, justify='center', font=('helvetica', 20),
            show="*")
        self.senha_entry.pack(pady=10)

        # botao login

        self.bt_login = ctk.CTkButton(
            self.frame_login,
            text="Login",
            fg_color='gray45',
            width=10,
            height=2,
            font=('helvetica', 15)
        )

        self.bt_login = ctk.CTkButton(
            self.frame_login,
            text="LOGIN",
            fg_color='gray45',
            text_color='gray10',
            font=('verdana', 20, 'bold'),
        )
        self.bt_login.pack(pady=50)

# !SECTION - Login
# TODO Janela de cadastro de alunos


# !SECTION - APP
App()
