import tkinter as tk
from tkinter import ttk
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

janela = tk.Tk()


class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")

    def gerarRelatCliente(self):
        self.c = canvas.Canvas("cliente.pdf")
        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.telefoneRel = self.telefone_entry.get()
        self.cidadeRel = self.cidade_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawString(50, 700, 'Código: ')
        self.c.drawString(50, 670, 'Nome: ')
        self.c.drawString(50, 630, 'Telefone: ')
        self.c.drawString(50, 600, 'Cidade: ')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 670, self.nomeRel)
        self.c.drawString(150, 630, self.telefoneRel)
        self.c.drawString(150, 600, self.cidadeRel)

        self.c.rect(20, 550, 550, 5, fill=True, stroke=False)

        self.c.showPage()
        self.c.save()
        self.printCliente()


class Funcs():
    def limpa_tela(self):
        self.codigo_entry.delete('0', tk.END)  # type: ignore
        self.nome_entry.delete('0', tk.END)  # type: ignore
        self.telefone_entry.delete('0', tk.END)  # type: ignore
        self.cidade_entry.delete('0', tk.END)  # type: ignore

    def conecta_bd(self):
        self.conn = sqlite3.connect('clientes.db')
        self.cursor = self.conn.cursor()
        print("conectando ao banco de dados")

    def desconecta_bd(self):
        self.conn.close()
        print("Desconectando ao banco de dados")

    def montaTabelas(self):
        self.conecta_bd()
        # criação do banco de dados
        # self.cursor.execute("CREATE DATABASE IF NOT EXISTS clientes_bd")
        # self.cursor.execute("USE clientes_bd")
        # criação da tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente VARCHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)
            );
        """)
        self.conn.commit()
        print("Banco de dados criado")
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()

    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cidade)
                            VALUES (?, ?, ?)""", (self.nome, self.telefone, self.cidade))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
            ORDER BY nome_cliente ASC; """)

        for i in lista:
            self.listaCli.insert("", tk.END, values=i)
        self.desconecta_bd()

    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(tk.END, col1)
            self.nome_entry.insert(tk.END, col2)
            self.telefone_entry.insert(tk.END, col3)
            self.cidade_entry.insert(tk.END, col4)

    def Deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(
            """DELETE FROM clientes WHERE cod = ? """, (self.codigo,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()

    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ?
                             WHERE cod = ? """, (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())
        self.nome_entry.insert(tk.END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
            """ SELECT cod, nome_cliente, telefone, cidade FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC """ % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", tk.END, values=i)
        self.limpa_tela()
        self.desconecta_bd()


class App(Funcs, Relatorios):

    def __init__(self) -> None:
        self.listaCli = None
        self.janela = janela
        self.tela()
        self.frame_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        janela.mainloop()

    def tela(self):
        self.janela.title('Cadastro de Professores')  # titulo da janela
        # configuraçoes de cores etc
        self.janela.configure(background='lightblue')
        self.janela.geometry('700x500')  # tamanho que abre a janela
        # se a janela pode ser redimensionada em largura e altura
        self.janela.resizable(True, True)
        self.janela.maxsize(width=900, height=700)  # tamanho maximo da janela
        self.janela.minsize(width=600, height=500)  # tamanho minimo da janela

    def frame_da_tela(self):
        self.frame_1 = tk.Frame(self.janela,
                                # largura da borda(padding) e cor do fundo.
                                bd=4, bg='#dfe3ee',
                                highlightbackground='#759fe6',  # cor da borda
                                highlightthickness=2)  # largura da borda
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = tk.Frame(self.janela,
                                bd=4, bg='#dfe3ee',
                                highlightbackground='#759fe6',
                                highlightthickness=2)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
        self.canvas_bt = tk.Canvas(self.frame_1, bd=0, bg='#1e3743',
                                   highlightbackground='gray',
                                   highlightthickness=5)
        self.canvas_bt.place(relx=0.19, rely=0.08,
                             relwidth=0.22, relheight=0.19)
        # Criação botão limpar
        self.bt_limpar = tk.Button(
            self.frame_1,
            text="limpar",
            bd=2,
            bg='#107bd2',
            fg='white',
            font=('verdana', 8, 'bold'),
            command=self.limpa_tela,
            activebackground='#108ecb',
            activeforeground='white'
        )
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        # Criação botão buscar
        self.bt_buscar = tk.Button(
            self.frame_1,
            text="buscar",
            bd=2, bg='#107bd2',
            fg='white',
            font=('verdana', 8, 'bold'),
            command=self.busca_cliente
        )
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        # Criação botão novo
        self.bt_novo = tk.Button(
            self.frame_1,
            text="novo",
            bd=2,
            bg='#107bd2',
            fg='white',
            font=('verdana', 8, 'bold'),
            command=self.add_cliente
        )
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        # Criação botão alterar
        self.bt_alterar = tk.Button(
            self.frame_1,
            text="alterar",
            bd=2,
            bg='#107bd2',
            fg='white',
            font=('verdana', 8, 'bold'),
            command=self.altera_cliente
        )
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        # Criação botão apagar
        self.bt_apagar = tk.Button(
            self.frame_1,
            text="apagar",
            bd=2,
            bg='#107bd2',
            fg='white',
            font=('verdana', 8, 'bold'),
            command=self.Deleta_cliente
        )
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        # Criação da label e entrada do codigo

        self.lb_codigo = tk.Label(
            self.frame_1, text='Código', bg='#dfe3ee', fg='#107db2')
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = tk.Entry(
            self.frame_1, bg='lightgray', fg='#107db2')
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.08)

        # Criação da label e entrada do nome

        self.lb_nome = tk.Label(self.frame_1, text='Nome',
                                bg='#dfe3ee', fg='#107db2')
        self.lb_nome.place(relx=0.05, rely=0.35)
        self.nome_entry = tk.Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.6)

        # Criação da label e entrada do telefone

        self.lb_telefone = tk.Label(
            self.frame_1, text='Telefone', bg='#dfe3ee', fg='#107db2')
        self.lb_telefone.place(relx=0.05, rely=0.6)

        self.telefone_entry = tk.Entry(self.frame_1)
        self.telefone_entry.place(relx=0.05, rely=0.7, relwidth=0.4)

        # Criação da label e entrada do cidade

        self.lb_cidade = tk.Label(
            self.frame_1, text='Cidade', bg='#dfe3ee', fg='#107db2')
        self.lb_cidade.place(relx=0.5, rely=0.6)

        self.cidade_entry = tk.Entry(self.frame_1)
        self.cidade_entry.place(relx=0.5, rely=0.7, relwidth=0.4)

    def lista_frame2(self):
        self.listaCli = ttk.Treeview(
            self.frame_2, height=3, columns=('col1', 'col2', 'col3', 'col4'))
        self.listaCli.heading("#0", text='')
        self.listaCli.heading("#1", text='codigo')
        self.listaCli.heading("#2", text='nome')
        self.listaCli.heading("#3", text='telefone')
        self.listaCli.heading("#4", text='cidade')

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)

        self.listaCli.place(relx=0.01, rely=0.1,
                            relwidth=0.95, relheight=0.85)
        self.scroolLista = ttk.Scrollbar(
            self.frame_2, orient='vertical', command=self.listaCli.yview)
        self.listaCli.configure(yscrollcommand=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1,
                               relwidth=0.04, relheight=0.85)

        self.listaCli.bind("<Double-1>", self.OnDoubleClick)

    def Menus(self):
        menubar = tk.Menu(self.janela)
        self.janela.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        filemenu2 = tk.Menu(menubar)

        def Quit(): self.janela.destroy()

        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Relatorio", menu=filemenu2)

        filemenu.add_command(label="Sair", command=Quit)
        filemenu.add_command(label="Limpa Cliente", command=self.limpa_tela)

        filemenu2.add_command(label="Ficha do Cliente",
                              command=self.gerarRelatCliente)


App()
