import tkinter as tk
from tkinter import ttk
from mysql.connector import connect
import re
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import tkinter.filedialog as filedialog
import io

janela = tk.Tk()


class Funcs():
    telselection = None

    def Montar_Dic_Cursos(self):
        # montando dicionario de cursos
        self.conecta_bd()

        querydicurso = """SELECT idcurso, nome FROM tbcurso"""
        self.cursor.execute(querydicurso, )
        self.dicCursos = {}
        for (idcurso, nome) in self.cursor:
            self.dicCursos[nome] = idcurso
        print(self.dicCursos)
        self.desconecta_bd()

    def apagar_campos(self):

        self.codra_entry.delete('0', tk.END)
        self.nome_entry.delete('0', tk.END)
        self.sobrenome_entry.delete('0', tk.END)
        self.data_nasc_entry.delete('0', tk.END)
        self.email1_entry.delete('0', tk.END)
        self.email2_entry.delete('0', tk.END)
        self.cpf_entry.delete('0', tk.END)
        self.curso_entry.set('')
        self.telefone_entry.delete('0', tk.END)
        self.prioridade_sb.set('')
        self.cep_entry.delete('0', tk.END)
        self.estado_entry.set('')
        self.cidade_entry.delete('0', tk.END)
        self.bairro_entry.delete('0', tk.END)
        self.complemento_entry.delete('0', tk.END)
        self.logradouro_entry.delete('0', tk.END)
        self.numero_entry.delete('0', tk.END)

        self.imagem = Image.new("RGB", (150, 150), color="black")
        self.imagem_tk = ImageTk.PhotoImage(self.imagem)
        self.label_foto.config(image=self.imagem_tk)
        self.label_foto.pack()

    def conecta_bd(self):
        self.conn = connect(
            host="localhost",
            user="root",
            password="Ricardo&Danubia",
            db='projetodb')
        self.cursor = self.conn.cursor()
        print('Conectando ao banco de dados')
        self.cursor.execute(""" use projetodb; """)
        print("conectado ao schema projetodb")

    def desconecta_bd(self):
        self.conn.close()
        print('Desconectando do banco de dados')

    def variaveis(self):
        self.codra = self.codra_entry.get()
        self.nome = self.nome_entry.get()
        self.sobrenome = self.sobrenome_entry.get()
        self.data_nasc = self.data_nasc_entry.get()
        self.email1 = self.email1_entry.get()
        self.email2 = self.email2_entry.get()
        self.cpf = self.cpf_entry.get()

        self.telefone = self.telefone_entry.get()
        self.prioridade = self.prioridade_sb.get()

        self.cep = self.cep_entry.get()
        self.estado = self.estado_entry.get()
        self.cidade = self.cidade_entry.get()
        self.bairro = self.bairro_entry.get()
        self.complemento = self.complemento_entry.get()
        self.logradouro = self.logradouro_entry.get()
        self.numero = self.numero_entry.get()

        self.curso = self.curso_entry.get()

        if self.curso:
            self.cursoid = self.dicCursos[self.curso]
        self.datetime_data_nasc = self.data_nasc_entry.get_date()
        self.data_nasc_datetime = self.datetime_data_nasc.strftime("%Y-%m-%d")

    def selecionar_imagens(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[('imagens', '*.png *.jpg *.jpeg')])
        if self.file_path:
            self.label_foto.config(image=None)
            self.imagem = Image.open(self.file_path)
            self.imagem = self.imagem.resize((150, 150), Image.NEAREST)
            self.imagem_tk = ImageTk.PhotoImage(self.imagem)
            self.label_foto.config(image=self.imagem_tk)

            self.label_foto.pack(fill=tk.BOTH, expand=True)

    def addPerfilAluno(self):
        self.variaveis()
        self.conecta_bd()
        #  Validação dos campos e email
        if not self.validar_email(self.email1):
            messagebox.showerror(
                "Erro de validação, o endereço de email não é valido.")
            self.desconecta_bd
            return
        if not self.validar_email(self.email2):
            messagebox.showerror(
                "Erro de validação o endereço de email2 não é válido")
            self.desconecta_bd
            return

        #  pega a data registrada no entry_data_nasc
        self.data_string = self.data_nasc
        #  transforma a data em um datetime
        self.data_datetime = self.data_nasc_entry.get_date()
        # coloca no formato desejado
        self.data_final = self.data_datetime.strftime("%Y-%m-%d")

        #  Inserindo valores na tabela tbPerfil

        querryPerfil = (""" INSERT INTO tbPerfil (nome, sobrenome, data_nasc, email1,
        email2, cpf) VALUES (%s, %s, %s, %s, %s, %s) """)

        self.cursor.execute(querryPerfil, (self.nome, self.sobrenome,
                                           self.data_final, self.email1,
                                           self.email2, self.cpf))

        #  Inserindo valores na tabela tbTelefone
        if len(self.telefone) > 0:

            querryTel = ("""INSERT INTO tbTelefone (numero, prioridade)
                          VALUES (%s, %s) """)

            self.cursor.execute(querryTel, (self.telefone, self.prioridade))

        #  Inserindo valores na tabela tbEndereco
        querryEndereco = (""" INSERT INTO tbEndereco(CEP, estado, cidade,
                            bairro, complemento,
                            logradouro, numero) VALUES(
                            %s, %s, %s, %s, %s, %s, %s) """)
        self.cursor.execute(querryEndereco, (
            self.cep, self.estado, self.cidade, self.bairro,
            self.complemento, self.logradouro, self.numero
        ))

        #  Criando variaveis de idPerfil, idEndereco e idTelefone
        querrygetid = (
            """ SELECT
                (SELECT idPerfil FROM tbPerfil ORDER BY idPerfil DESC LIMIT 1) as idPerfil,
                (SELECT idEndereco FROM tbEndereco ORDER BY idEndereco DESC LIMIT 1) as idEndereco,
                (SELECT idTelefone FROM tbTelefone ORDER BY idTelefone DESC LIMIT 1) as idTelefone,
                (SELECT RA FROM tbAluno ORDER BY RA DESC LIMIT 1) as RA
            """
        )
        self.cursor.execute(querrygetid,)
        self.result = self.cursor.fetchone()

        self.idPerfil_ultimo = self.result[0]
        self.idEndereco_ultimo = self.result[1]
        self.idTelefone_ultimo = self.result[2]
        self.codra_ultimo = self.result[3]

        # Inserindo os dados na tabela tbAluno

        querryCriaraluno = ("""INSERT INTO tbAluno
                            (idPerfil, idEndereco, idCurso)
                            VALUES
                            (%s, %s, %s)
                            """)
        self.cursor.execute(
            querryCriaraluno, (self.idPerfil_ultimo, self.idEndereco_ultimo, self.cursoid))

        #  Inserindo valores da tabela de junção telefone/aluno
        QuerryTelAlu = """ INSERT INTO tbAluno_has_tbTelefone (RA, idTelefone)
                            VALUES (%s, %s);
                        """
        self.cursor.execute(
            QuerryTelAlu, (self.codra_ultimo, self.idTelefone_ultimo))

        self.conn.commit()
        self.desconecta_bd()
        self.Select_listas()
        self.apagar_campos()

    def addTelefone(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO tbTelefone (numero, prioridade)
                            VALUES (%s, %s); """, (self.telefone, self.prioridade))

        self.idTelefone_ultimo = self.cursor.lastrowid

        querryAHT = """ INSERT INTO tbAluno_has_tbTelefone (RA, idTelefone)
                        VALUES (%s, %s); """
        self.cursor.execute(querryAHT, (self.codra, self.idTelefone_ultimo))

        self.conn.commit()

        self.desconecta_bd()

        self.select_listatel(self.codra)

    def Select_listas(self):
        self.listaAlu.delete(*self.listaAlu.get_children())
        self.conecta_bd()

        QuerryA = """ SELECT a.ra,
                p.nome,
                p.sobrenome,
                date_format(p.data_nasc, '%d/%m/%y'),
                p.email1,
                p.email2,
                p.cpf,
                c.nome
                FROM tbperfil p
                JOIN tbaluno a
                ON p.idperfil = a.idperfil
                JOIN tbcurso c on c.idcurso = a.idcurso
                ORDER BY p.nome, p.sobrenome;
                """

        self.cursor.execute(QuerryA)
        listaA = self.cursor.fetchall()

        for i in listaA:
            self.listaAlu.insert("", tk.END, values=i)

        self.desconecta_bd()

    def select_listatel(self, ra):
        self.variaveis()
        self.listaTel.delete(*self.listaTel.get_children())

        self.conecta_bd()
        QuerryT = """SELECT t.prioridade, t.numero
                    FROM tbtelefone t
                    JOIN tbAluno_has_tbtelefone aht ON t.idtelefone = aht.idtelefone
                    JOIN tbaluno a ON aht.ra = a.ra
                    where a.ra = %s
                    ORDER BY t.prioridade ;
                    """
        self.cursor.execute(QuerryT, (ra,))

        ListaT = self.cursor.fetchall()

        for i in ListaT:
            self.listaTel.insert("", tk.END, values=(i[0], i[1]))

        self.desconecta_bd()

    def OnDoubleClick(self, event):
        self.apagar_campos()
        self.variaveis()
        self.listaAlu.selection()
        for n in self.listaAlu.selection():
            col1, col2, col3, col4, col5, col6, col7, col8 = self.listaAlu.item(
                n, 'values')

            self.codra_entry.insert(tk.END, col1)
            self.nome_entry.insert(tk.END, col2)
            self.sobrenome_entry.insert(tk.END, col3)
            self.data_nasc_entry.insert(tk.END, col4)
            self.email1_entry.insert(tk.END, col5)
            self.email2_entry.insert(tk.END, col6)
            self.cpf_entry.insert(tk.END, col7)

            self.indiceCurso = list(self.dicCursos.keys()).index(col8)
            self.curso_entry.set(list(self.dicCursos.keys())[self.indiceCurso])

        self.select_listatel(col1)

        self.conecta_bd()

        self.cursor.execute(""" SELECT a.idEndereco
                            FROM tbaluno a
                            WHERE a.ra = %s """, (self.codra,))
        resultado = self.cursor.fetchone()
        self.idEndereco = resultado[0]
        print(self.idEndereco)
        querryEndereco = ("""SELECT te.cep, te.estado,
                            te.cidade, te.bairro, te.complemento,
                            te.logradouro, te.numero
                            from tbendereco te
                            where te.idEndereco = %s ; """)
        listaE = self.cursor.execute(querryEndereco, (self.idEndereco,))
        listaE = self.cursor.fetchall()
        for n in listaE:
            coll1, coll2, coll3, coll4, coll5, coll6, coll7 = listaE[0]

        self.cep_entry.insert(tk.END, coll1)
        self.estado_entry.insert(tk.END, coll2)
        self.cidade_entry.insert(tk.END, coll3)
        self.bairro_entry.insert(tk.END, coll4)
        self.complemento_entry.insert(tk.END, coll5)
        self.logradouro_entry.insert(tk.END, coll6)
        self.numero_entry.insert(tk.END, coll7)

        # carregar a imagem do banco de dados

        querryfoto = """SELECT foto FROM tbPerfil tp
                        JOIN tbAluno ta ON ta.idperfil = tp.idperfil
                        WHERE ta.ra = %s"""
        self.cursor.execute(querryfoto, (self.codra, ))
        self.foto_bytes = self.cursor.fetchone()[0]
        if self.foto_bytes:
            self.foto_bytes = io.BytesIO(self.foto_bytes)
            self.foto_bytes.seek(0)
            self.imagem_tk = ImageTk.PhotoImage(Image.open(self.foto_bytes))
            self.label_foto.config(image=self.imagem_tk)
            self.label_foto.pack()
        else:
            self.imagem = Image.new("RGB", (150, 150), color="black")
            self.imagem_tk = ImageTk.PhotoImage(self.imagem)
            self.label_foto.config(image=self.imagem_tk)
            self.label_foto.pack()

    def onDoubleClicktel(self, event):
        self.variaveis()
        self.telefone_entry.delete('0', tk.END)
        self.prioridade_sb.set('')

        self.listaTel.selection()

        for n in self.listaTel.selection():
            col1, col2 = self.listaTel.item(n, 'values')

            self.telefone_entry.insert(tk.END, col2)
            self.prioridade_sb.insert(tk.END, col1)
        Funcs.telselection = self.telefone_entry.get()

    def deleta_perfil(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(
            """DELETE FROM tbAluno WHERE RA = %s """, (self.codra,))

        self.conn.commit()
        self.desconecta_bd()
        self.apagar_campos()
        self.Select_listas()

     # Deletar telefone

    def deleta_telefone(self):
        self.variaveis()
        self.conecta_bd()

        querryidTel = """SELECT tbAluno_has_tbTelefone.idTelefone
                        FROM  tbAluno_has_tbTelefone
                        join tbtelefone on tbAluno_has_tbTelefone.idtelefone = tbtelefone.idtelefone
                        WHERE tbAluno_has_tbTelefone.ra = %s
                        and tbTelefone.numero = %s"""
        self.cursor.execute(querryidTel, (self.codra, self.telefone))
        self.id_Telefone = self.cursor.fetchone()
        id_Telefone = self.id_Telefone[0] if self.id_Telefone else None
        print(id_Telefone)
        print(self.codra)
        if id_Telefone is not None:

            self.cursor.execute("""DELETE FROM TbTelefone
                                WHERE tbTelefone.idtelefone = %s
                                and tbTelefone.numero = %s
                                and tbTelefone.prioridade = %s""",
                                (id_Telefone, self.telefone, self.prioridade))
            self.cursor.fetchall()
            self.conn.commit()
            self.select_listatel(self.codra)
        self.desconecta_bd()
        self.telefone_entry.delete('0', tk.END)
        self.prioridade_sb.set('')

    def busca_aluno(self):
        self.variaveis()
        self.conecta_bd()

        querryBusca = """
             SELECT a.ra,
                p.nome,
                p.sobrenome,
                date_format(p.data_nasc, '%d/%m/%y'),
                p.email1,
                p.email2,
                p.cpf,
                a.idendereco
                FROM tbperfil p
                JOIN tbaluno a
                ON p.idperfil = a.idperfil
                """

        if not self.data_nasc_entry.get():
            self.data.nasc.set("")

        where_clauses = []
        valores = []

        # Verifica se cada entrada está preenchida e adiciona a cláusula WHERE correspondente

        if self.codra:
            where_clauses.append("a.RA = %s")
            valores.append(self.codra)

        if self.nome:
            where_clauses.append("p.nome LIKE %s")
            valores.append(f'%{self.nome}%')

        if self.sobrenome:
            where_clauses.append("p.sobrenome LIKE %s")
            valores.append(f'%{self.sobrenome}%')

        if self.data_nasc:
            self.data_nasc_format = datetime.strptime(
                self.data_nasc, "%d/%m/%y")
            self.data_nasc_format_final = self.data_nasc_format.date()
            print(self.data_nasc_format_final)
            self.data_nasc_format.strftime("%Y-%m%d")
            where_clauses.append("p.data_nasc LIKE %s")
            valores.append(f'%{self.data_nasc_format_final}%')

        if self.email1:
            where_clauses.append("p.email1 LIKE %s")
            valores.append(f'%{self.email1}%')

        if self.email2:
            where_clauses.append("p.email2 LIKE %s")
            valores.append(f'%{self.email2}%')

        if self.cpf:
            where_clauses.append("p.cpf LIKE %s")
            valores.append(f'%{self.cpf}%')

        # Adiciona as cláusulas WHERE à consulta SQL, se houver alguma

        if where_clauses:
            querryBusca += " WHERE " + " AND ".join(where_clauses)

        # Adiciona order by

        querryBusca += """ ORDER BY p.nome, p.sobrenome;"""

        self.cursor.execute(querryBusca, tuple(valores))
        listaBusca = self.cursor.fetchall()

        self.listaAlu.delete(*self.listaAlu.get_children())

        for i in listaBusca:
            self.listaAlu.insert("", tk.END, values=i)

        print(f"{querryBusca}")
        print(valores)
        self.desconecta_bd()

    def altera_aluno(self):
        self.variaveis()
        self.conecta_bd()
        self.imagem_bytesIO = io.BytesIO()
        self.imagem_bytes = Image.open(self.file_path)
        self.imagem_bytes = self.imagem_bytes.resize(
            (150, 150), Image.NEAREST)
        self.imagem_bytes.save(self.imagem_bytesIO, "PNG")
        self.imagem_bytesIO.seek(0)
        self.imagem_bytes = self.imagem_bytesIO.read()

        querryUpdt = """ UPDATE tbperfil as p
                            JOIN tbAluno a ON a.idperfil = p.idperfil
                            SET p.nome = %s,
                            p.sobrenome = %s,
                            p.data_nasc = %s,
                            p.email1 = %s,
                            p.email2 = %s,
                            p.cpf = %s,
                            p.foto = %s,
                            a.idcurso = %s
                            WHERE RA = %s  """
        self.cursor.execute(querryUpdt,
                            (self.nome, self.sobrenome,
                             self.data_nasc_datetime, self.email1,
                             self.email2, self.cpf, self.imagem_bytes,
                             self.cursoid, self.codra)
                            )

        self.conn.commit()
        self.desconecta_bd()
        self. Select_listas()
        self.apagar_campos()

    def altera_telefone(self):
        self.variaveis()
        self.conecta_bd()
        print(self.codra)
        print(self.telefone)
        querryidTel = """SELECT tbAluno_has_tbTelefone.idTelefone
                        FROM  tbAluno_has_tbTelefone
                        join tbtelefone on tbAluno_has_tbTelefone.idtelefone = tbtelefone.idtelefone
                        WHERE tbAluno_has_tbTelefone.ra = %s
                        and tbTelefone.numero = %s"""
        self.cursor.execute(querryidTel, (self.codra, Funcs.telselection))
        self.id_Telefone2 = self.cursor.fetchone()
        print(self.id_Telefone2)
        id_Telefone2 = self.id_Telefone2[0] if self.id_Telefone2 else None
        querryUPDTel = """ UPDATE tbTelefone t
                            SET t.numero = %s,
                            t.prioridade = %s
                            WHERE t.idtelefone = %s"""
        self.cursor.execute(querryUPDTel, (self.telefone,
                            self.prioridade, id_Telefone2))

        self.conn.commit()
        self.desconecta_bd()
        self.select_listatel(self.codra)
        self.telefone_entry.delete('0', tk.END)
        self.prioridade_sb.set('')

    def validar_email(self, email):
        regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        return re.search(regex, email) is not None


class App(Funcs):

    def __init__(self) -> None:
        self.frame_atual = None
        self.janela = janela
        self.listaAlu = None
        self.tela_cadastro_aluno()
        self.frames()
        self.menus()
        self.Montar_Dic_Cursos()
        self.widgets_tela2()
        self.Select_listas()

        janela.mainloop()

    def menus(self):
        menubar = tk.Menu(self.janela)
        self.janela.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        filemenu2 = tk.Menu(menubar)
        filemenu3 = tk.Menu(menubar)
        filemenu4 = tk.Menu(menubar)

        def quit(): self.janela.destroy()

        menubar.add_cascade(label="Login", menu=filemenu)
        menubar.add_cascade(label="Cadastro", menu=filemenu2)
        menubar.add_cascade(label="Opções", menu=filemenu3)
        menubar.add_cascade(label="Sobre", menu=filemenu4)

        filemenu2.add_cascade(label="Alunos")
        filemenu2.add_cascade(label="Professores")
        filemenu2.add_cascade(label="Departamentos")
        filemenu2.add_cascade(label="Cursos")
        filemenu2.add_cascade(label="Disciplinas")
        filemenu2.add_cascade(label="Turmas")

        filemenu3.add_command(label="Sair", command=quit)

    def exibir_alunos(self):
        if self.frame_atual is not None:
            self.frame_atual.destroy()

        self.frame_atual = tk.Frame(self.janela)
        self.frame_atual.pack(fill="both", expand=True)

    def tela_cadastro_aluno(self):
        self.janela.title('Cadastro de Aluno')
        self.janela.configure(background='#549535')
        # self.janela.attributes('-fullscreen', True)
        self.janela.minsize(width=700, height=500)

    def frames(self):
        self.frame_heading = tk.Frame(self.janela,
                                      bd=2,
                                      bg='#1C5700'
                                      )
        self.frame_heading.place(relx=0.01, rely=0.01,
                                 relwidth=0.98, relheight=0.15)
        self.texto_top = tk.Label(
            self.frame_heading, text="UniSenai", bg='#1C5700',
            fg='black', font=('Helvetica', 30))
        self.texto_top.configure(justify='center')
        self.texto_top.pack(expand=True)
        self.frame_body = tk.Frame(self.janela,
                                   bd=5,
                                   bg='#76EE00'
                                   )
        self.frame_body.place(relx=0.01, rely=0.17,
                              relheight=0.50, relwidth=0.98)

        self.frame_foto = tk.Frame(self.frame_body,
                                   bd=5,
                                   bg='black'
                                   )
        self.frame_foto.place(rely=0.1, relx=0.02, relwidth=0.1, relheight=0.4)

        self.frame_tel = tk.Frame(self.frame_body,
                                  bd=5,
                                  bg='yellow')

        self.frame_tel.place(rely=0.53, relx=0.13,
                             relwidth=0.17, relheight=0.4)

        self.frame_endereco = tk.Frame(self.frame_body,
                                       bd=2,
                                       bg='chartreuse4')
        self.frame_endereco.place(
            rely=0.16, relx=0.35, relheight=0.5, relwidth=0.30)

        self.endereco_title = tk.Label(
            self.frame_endereco, text="Endereço",
            bg='chartreuse4', font=('Helvetica', 20))
        self.endereco_title.configure(justify="center")
        self.endereco_title.pack()

        self.frame_btn = tk.Frame(self.frame_body,
                                  bd=2,
                                  bg='chartreuse4')
        self.frame_btn.place(
            rely=0.05, relx=0.7, relheight=0.9, relwidth=0.28)

        self.frame_bot = tk.Frame(self.janela,
                                  bd=2,
                                  background='springgreen3')

        self.frame_bot.place(rely=0.67, relx=0.01,
                             relwidth=0.98, relheight=0.32)

    def widgets_tela2(self):

        self.texto_aluno = tk.Label(
            self.frame_body, text="Cadastro de Alunos", bg='#1C5700',
            fg='black', font=('Helvetica', 25))
        self.texto_aluno.configure(justify='center')
        self.texto_aluno.pack(padx=10)

        self.bt_foto = tk.Button(self.frame_body,
                                 text="Selecionar Imagem",
                                 command=self.selecionar_imagens)
        self.bt_foto.place(relx=0.03, rely=0.56, relwidth=0.08)

        self.label_foto = tk.Label(self.frame_foto)

        # ------------------Botoes----------------

        # Criação botão limpar
        self.bt_limpar = tk.Button(
            self.frame_btn,
            text="limpar",
            bd=2,
            bg='#107bd2',
            fg='white',
            font=('verdana', 8, 'bold'),
            activebackground='#108ecb',
            activeforeground='white',
            command=self.apagar_campos

        )
        self.bt_limpar.configure()

        self.bt_limpar.place(relx=0.18, rely=0.2,
                             relheight=0.15, relwidth=0.3)

        # Criação botão buscar
        self.bt_buscar = tk.Button(
            self.frame_btn,
            text="buscar",
            bd=2,
            bg='#107bd2',
            fg='white',
            font=('verdana', 8, 'bold'),
            activebackground='#108ecb',
            activeforeground='white',
            command=self.busca_aluno
        )
        self.bt_buscar.place(relx=0.52, rely=0.2,
                             relheight=0.15, relwidth=0.3)

        # Criação botão novo
        self.bt_novo = tk.Button(
            self.frame_btn,
            text="novo",
            bd=2,
            bg='#107bd2',
            fg='white',
            font=('verdana', 8, 'bold'),
            activebackground='#108ecb',
            activeforeground='white',
            command=self.addPerfilAluno
        )
        self.bt_novo.place(relx=0.18, rely=0.45,
                           relheight=0.15, relwidth=0.3)

        # Criação botão alterar
        self.bt_alterar = tk.Button(
            self.frame_btn,
            text="alterar",
            bd=2,
            bg='#107bd2',
            fg='white',
            font=('verdana', 8, 'bold'),
            activebackground='#108ecb',
            activeforeground='white',
            command=self.altera_aluno
        )
        self.bt_alterar.place(relx=0.52, rely=0.45,
                              relheight=0.15, relwidth=0.3)

        # Criação botão apagar
        self.bt_apagar = tk.Button(
            self.frame_btn,
            text="apagar",
            bd=2,
            bg='#107bd2',
            fg='white',
            font=('verdana', 8, 'bold'),
            activebackground='#108ecb',
            activeforeground='white',
            command=self.deleta_perfil
        )
        self.bt_apagar.place(relx=0.35, rely=0.70,
                             relheight=0.15, relwidth=0.3)

        # ------------------Labels e Entradas frame_body-----------------

        # Criação da label e entrada do RA

        self.lb_codra = tk.Label(
            self.frame_body, text='RA', bg='#dfe3ee', fg='#107db2')
        self.lb_codra.place(relx=0.13, rely=0.1)

        self.codra_entry = tk.Entry(
            self.frame_body, bg='lightgray', fg='#107db2')
        self.codra_entry.place(relx=0.20, rely=0.1, relwidth=0.1)

        # Criação da label e entrada do nome

        self.lb_nome = tk.Label(
            self.frame_body, text='Nome', bg='#dfe3ee', fg='#107db2')
        self.lb_nome.place(relx=0.13, rely=0.16)

        self.nome_entry = tk.Entry(
            self.frame_body, bg='lightgray', fg='#107db2')
        self.nome_entry.place(relx=0.20, rely=0.16, relwidth=0.1)

        # Criação da label e entrada do sobrenome

        self.lb_sobrenome = tk.Label(
            self.frame_body, text='Sobrenome', bg='#dfe3ee', fg='#107db2')
        self.lb_sobrenome.place(relx=0.13, rely=0.22)

        self.sobrenome_entry = tk.Entry(
            self.frame_body, bg='lightgray', fg='#107db2')
        self.sobrenome_entry.place(relx=0.20, rely=0.22, relwidth=0.1)

        # Criação da label e entrada de nascimento

        self.lb_data_nasc = tk.Label(
            self.frame_body, text='Data de nascimento',
            bg='#dfe3ee', fg='#107db2')
        self.lb_data_nasc.place(relx=0.13, rely=0.28)

        self.data_nasc_entry = DateEntry(
            self.frame_body, date_pattern='dd/MM/yy')
        self.data_nasc_entry.place(relx=0.20, rely=0.28, relwidth=0.1)

        # Criação da label e entrada email1

        self.lb_email1 = tk.Label(
            self.frame_body, text='Email 1', bg='#dfe3ee', fg='#107db2')
        self.lb_email1.place(relx=0.13, rely=0.34)

        self.email1_entry = tk.Entry(
            self.frame_body, bg='lightgray', fg='#107db2')
        self.email1_entry.place(relx=0.2, rely=0.34, relwidth=0.1)

        # Criação da label e entrada email2

        self.lb_email2 = tk.Label(
            self.frame_body, text='Email 2', bg='#dfe3ee', fg='#107db2')
        self.lb_email2.place(relx=0.13, rely=0.40)

        self.email2_entry = tk.Entry(
            self.frame_body, bg='lightgray', fg='#107db2')
        self.email2_entry.place(relx=0.2, rely=0.40, relwidth=0.1)

        # Criação da label e entrada CPF

        self.lb_cpf = tk.Label(
            self.frame_body, text='CPF', bg='#dfe3ee', fg='#107db2')
        self.lb_cpf.place(relx=0.13, rely=0.46)

        self.cpf_entry = tk.Entry(
            self.frame_body, bg='lightgray', fg='#107db2')
        self.cpf_entry.place(relx=0.2, rely=0.46, relwidth=0.1)

        # Criação da label e entrada de Curso
        self.listaCurso = ['curso1', 'curso2']    # MODIFICAR POSICAO TODO
        self.lb_curso = tk.Label(
            self.frame_body, text='Curso',
            bg='#dfe3ee', fg='#107db2', font=('helvetica', 15))
        self.lb_curso.place(relx=0.48, rely=0.67)

        self.curso_entry = ttk.Combobox(
            self.frame_body,
            background='lightgray',
            foreground='#107db2',
            values=list(self.dicCursos.keys()),
            state='readonly',
            font=("helvetica", 20), justify='center')
        self.curso_entry.place(
            relx=0.35, rely=0.75, relwidth=0.3, relheight=0.18)

        # ------------------Labels e Entradas frame_tel----------------

        # Criação da label entrada de telefones

        self.lb_telefone = tk.Label(
            self.frame_tel, text='telefone', bg='#dfe3ee', fg='#107db2')
        self.lb_telefone.place(relx=0.02, rely=0.02)

        self.telefone_entry = tk.Entry(
            self.frame_tel, bg='lightgray', fg='#107db2')
        self.telefone_entry.place(
            relx=0.02, rely=0.14, relwidth=0.50, relheight=0.1)

        self.lb_prioridade = tk.Label(
            self.frame_tel, text='prioridade', bg='#dfe3ee', fg='#107db2')
        self.lb_prioridade.place(relx=0.54, rely=0.02)

        self.prioridade_sb = ttk.Spinbox(
            self.frame_tel, from_=1, to=5
        )
        self.prioridade_sb.place(relx=0.54, rely=0.14, relwidth=0.1)

        # -----------------Treeview e botoes frame_tel-----------------

        self.listaTel = ttk.Treeview(
            self.frame_tel,
            height=3,
            columns=('col0', 'col1', 'col2', 'col3')
        )
        self.listaTel.heading('#0', text='')
        self.listaTel.heading('#1', text='prioridade')
        self.listaTel.heading('#2', text='número')

        self.listaTel.column('#0', width=1, minwidth=1, anchor='center')
        self.listaTel.column('#1', width=80, anchor='center', minwidth=80)
        self.listaTel.column('#2', width=160, anchor='center', minwidth=160)
        self.listaTel.place(relx=0.02, rely=0.26,
                            relheight=0.5, relwidth=0.9)
        self.listaTel.bind("<Double-1>", self.onDoubleClicktel)

        self.scroollistaTel = tk.Scrollbar(self.frame_tel,
                                           orient='vertical',
                                           command=self.listaTel.yview)
        self.listaTel.configure(yscrollcommand=self.scroollistaTel.set)
        self.scroollistaTel.place(
            relx=0.97, rely=0.26, relheight=0.6, relwidth=0.04)
        # Criação botão adicionar telefone
        self.bt_add_tel = tk.Button(
            self.frame_tel,
            text="adicionar",
            bd=1,
            bg='#107bd2',
            fg='white',
            font=('verdana', 6, 'bold'),
            activebackground='#108ecb',
            activeforeground='white',
            command=self.addTelefone
        )
        self.bt_add_tel.place(relx=0.1, rely=0.88,
                              relheight=0.13, relwidth=0.20)

        # Criação botão apagar telefone
        self.bt_apg_tel = tk.Button(
            self.frame_tel,
            text="apagar",
            bd=1,
            bg='#107bd2',
            fg='white',
            font=('verdana', 6, 'bold'),
            activebackground='#108ecb',
            activeforeground='red',
            command=self.deleta_telefone
        )
        self.bt_apg_tel.place(relx=0.4, rely=0.88,
                              relheight=0.13, relwidth=0.2)

        # Criação botão alterar telefone
        self.bt_upd_tel = tk.Button(
            self.frame_tel,
            text="alterar",
            bd=1,
            bg='#107bd2',
            fg='white',
            font=('verdana', 6, 'bold'),
            activebackground='#108ecb',
            activeforeground='red',
            command=self.altera_telefone
        )
        self.bt_upd_tel.place(relx=0.7, rely=0.88,
                              relheight=0.13, relwidth=0.2)

        # ------------------Labels e Entradas frame_endereco----------------

        # Criação da label e entrada cep
        self.lb_cep = tk.Label(
            self.frame_endereco, text='cep', bg='#dfe3ee', fg='#107db2')
        self.lb_cep.place(relx=0.02, rely=0.2)

        self.cep_entry = tk.Entry(
            self.frame_endereco, bg='lightgray', fg='#107db2')
        self.cep_entry.place(
            relx=0.22, rely=0.2, relwidth=0.2, relheight=0.1)

        # Criação da label e entrada cep
        self.lb_estado = tk.Label(
            self.frame_endereco, text='Estado', bg='#dfe3ee', fg='#107db2')
        self.lb_estado.place(relx=0.02, rely=0.32)

        self.estado_entry = ttk.Combobox(
            self.frame_endereco, values=(
                'AC', 'AL', 'AP', 'AM', 'BA',
                'CE', 'DF', "ES", 'GO', 'MA',
                'MT', 'MS', 'MG', 'PA', 'PB',
                'PR', 'PE', 'PI', 'RJ', 'RN',
                'RS', 'RO', 'RR', 'SC', 'SP',
                'SE', 'TO'))
        self.estado_entry.place(
            relx=0.22, rely=0.32, relwidth=0.1, relheight=0.1)

        # Criação da label e entrada Cidade
        self.lb_cidade = tk.Label(
            self.frame_endereco, text='Cidade', bg='#dfe3ee', fg='#107db2')
        self.lb_cidade.place(relx=0.02, rely=0.44)

        self.cidade_entry = tk.Entry(
            self.frame_endereco, bg='lightgray', fg='#107db2')
        self.cidade_entry.place(
            relx=0.22, rely=0.44, relwidth=0.2, relheight=0.1)

        # Criação da label e entrada Bairro
        self.lb_bairro = tk.Label(
            self.frame_endereco, text='Bairro', bg='#dfe3ee', fg='#107db2')
        self.lb_bairro.place(relx=0.02, rely=0.56)

        self.bairro_entry = tk.Entry(
            self.frame_endereco, bg='lightgray', fg='#107db2')
        self.bairro_entry.place(
            relx=0.22, rely=0.56, relwidth=0.2, relheight=0.1)

        # Criação da label e entrada Complemento
        self.lb_complemento = tk.Label(
            self.frame_endereco, text='Complemento',
            bg='#dfe3ee', fg='#107db2')
        self.lb_complemento.place(relx=0.02, rely=0.68)

        self.complemento_entry = tk.Entry(
            self.frame_endereco, bg='lightgray', fg='#107db2')
        self.complemento_entry.place(
            relx=0.22, rely=0.68, relwidth=0.2, relheight=0.1)

        # Criação da label e entrada logradouro
        self.lb_logradouro = tk.Label(
            self.frame_endereco, text='Logradouro', bg='#dfe3ee', fg='#107db2')
        self.lb_logradouro.place(relx=0.44, rely=0.2)

        self.logradouro_entry = tk.Entry(
            self.frame_endereco, bg='lightgray', fg='#107db2')
        self.logradouro_entry.place(
            relx=0.64, rely=0.2, relwidth=0.2, relheight=0.1)

        # Criação da label e entrada numero
        self.lb_numero = tk.Label(
            self.frame_endereco, text='Número', bg='#dfe3ee', fg='#107db2')
        self.lb_numero.place(relx=0.44, rely=0.32)

        self.numero_entry = tk.Entry(
            self.frame_endereco, bg='lightgray', fg='#107db2')
        self.numero_entry.place(
            relx=0.64, rely=0.32, relwidth=0.2, relheight=0.1)

        # ------------------Treeview com apresentação dos dados----------------

        self.listaAlu = ttk.Treeview(self.frame_bot, height=10,
                                     columns=("col1", "col2",
                                              "col3", "col4",
                                              "col5", "col6",
                                              "col7", "col8"))

        self.listaAlu.heading('#0', text='')
        self.listaAlu.heading('#1', text='RA')
        self.listaAlu.heading('#2', text='Nome')
        self.listaAlu.heading('#3', text='Sobrenome')
        self.listaAlu.heading('#4', text='Data de Nascimento')
        self.listaAlu.heading('#5', text='Email1')
        self.listaAlu.heading('#6', text='Email2')
        self.listaAlu.heading('#7', text='CPF')
        self.listaAlu.heading('#8', text='Curso')

        self.listaAlu.column('#0', width=1, minwidth=1, anchor='center')
        self.listaAlu.column('#1', width=80, anchor='center')
        self.listaAlu.column('#2', width=100, minwidth=100, anchor='center')
        self.listaAlu.column('#3', width=160, minwidth=160, anchor='center')
        self.listaAlu.column('#4', width=160, minwidth=160, anchor='center')
        self.listaAlu.column('#5', width=160, minwidth=160, anchor='center')
        self.listaAlu.column('#6', width=160, minwidth=160, anchor='center')
        self.listaAlu.column('#7', width=160, minwidth=160, anchor='center')
        self.listaAlu.column('#8', width=100, minwidth=100, anchor='center')
        self.listaAlu.place(rely=0.1, relx=0.15, relheight=0.90, relwidth=0.7)

        self.listaAluScroll = tk.Scrollbar(self.frame_bot, orient='vertical',
                                           command=self.listaTel.yview)
        self.listaAlu.configure(yscrollcommand=self.listaAluScroll.set)
        self.listaAluScroll.place(
            relx=0.85, rely=0.1,
            relheight=0.9, relwidth=0.02)
        self.listaAlu.bind("<Double-1>", self.OnDoubleClick)


App()
