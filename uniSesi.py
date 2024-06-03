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
# type: ignore
janela = tk.Tk()


class Funcs():
    telselection = None

# Conexao com banco de dados
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

# Funcões globais
    def Montar_Dic_Cursos(self):
        # montando dicionario de cursos
        self.conecta_bd()

        querydicurso = """SELECT idcurso, nome FROM tbcurso"""
        self.cursor.execute(querydicurso, )
        self.dicCursos = {}
        for (idcurso, nome) in self.cursor:
            self.dicCursos[nome] = idcurso
        self.desconecta_bd()

    def Montar_Dic_Departamentos(self):
        self.conecta_bd()
        self.cursor.execute(
            """SELECT idDepartamento, nome FROM tbDepartamento""")
        self.dicDepartamento = {}
        for (idDepartamento, nome) in self.cursor:
            self.dicDepartamento[nome] = idDepartamento
        self.desconecta_bd()

    def validar_email(self, email):
        regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        return re.search(regex, email) is not None

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

# Funções Aluno
    def variaveis_aluno(self):
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

    def apagar_campos_aluno(self):

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

    def addPerfilAluno(self):
        self.variaveis_aluno()
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

        # Verificando se há foto e inserindo o dado na tabela perfil

        if self.file_path is not None:
            self.imagem_bytesIO = io.BytesIO()
            self.imagem_bytes = Image.open(self.file_path)
            self.imagem_bytes = self.imagem_bytes.resize(
                (150, 150), Image.NEAREST)
            self.imagem_bytes.save(self.imagem_bytesIO, "PNG")
            self.imagem_bytesIO.seek(0)
            self.imagem_bytes = self.imagem_bytesIO.read()

            self.cursor.execute(
                ("""UPDATE tbPerfil SET foto = %s WHERE idPerfil = %s"""), (self.imagem_bytes, self.idPerfil_ultimo))

        # Inserindo os dados na tabela tbAluno

        querryCriaraluno = ("""INSERT INTO tbAluno
                            (idPerfil, idEndereco, idCurso)
                            VALUES
                            (%s, %s, %s)
                            """)
        self.cursor.execute(
            querryCriaraluno, (self.idPerfil_ultimo, self.idEndereco_ultimo, self.cursoid))

        #  Inserindo valores da tabela de junção telefone/aluno
        self.codra_ultimo = self.cursor.lastrowid
        QuerryTelAlu = """ INSERT INTO tbAluno_has_tbTelefone (RA, idTelefone)
                            VALUES (%s, %s);
                        """
        self.cursor.execute(
            QuerryTelAlu, (self.codra_ultimo, self.idTelefone_ultimo))

        self.conn.commit()
        self.desconecta_bd()
        self.Montar_Dic_Cursos
        self.Select_listas_aluno()
        self.apagar_campos_aluno()

    def addTelefone_aluno(self):
        self.variaveis_aluno()
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

    def Select_listas_aluno(self):
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

    def select_listatel_aluno(self, ra):
        self.variaveis_aluno()
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

    def OnDoubleClick_aluno(self, event):
        self.apagar_campos_aluno()
        self.variaveis_aluno()
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

        self.select_listatel_aluno(col1)

        self.conecta_bd()

        self.cursor.execute(""" SELECT a.idEndereco
                            FROM tbaluno a
                            WHERE a.ra = %s """, (self.codra,))
        resultado = self.cursor.fetchone()
        self.idEndereco = resultado[0]
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

    def onDoubleClicktel_aluno(self, event):
        self.variaveis_aluno()
        self.telefone_entry.delete('0', tk.END)
        self.prioridade_sb.set('')

        self.listaTel.selection()

        for n in self.listaTel.selection():
            col1, col2 = self.listaTel.item(n, 'values')

            self.telefone_entry.insert(tk.END, col2)
            self.prioridade_sb.insert(tk.END, col1)
        Funcs.telselection = self.telefone_entry.get()

    def deleta_perfil_aluno(self):
        self.variaveis_aluno()
        self.conecta_bd()

        self.cursor.execute(
            """DELETE FROM tbAluno WHERE RA = %s """, (self.codra,))

        self.conn.commit()
        self.desconecta_bd()
        self.apagar_campos_aluno()
        self.Select_listas_aluno()

     # Deletar telefone

    def deleta_telefone_aluno(self):
        self.variaveis_aluno()
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
            self.select_listatel_aluno(self.codra)
        self.desconecta_bd()
        self.telefone_entry.delete('0', tk.END)
        self.prioridade_sb.set('')

    def busca_aluno(self):
        self.variaveis_aluno()
        self.Montar_Dic_Departamentos()
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
        self.variaveis_aluno()
        self.conecta_bd()

        if self.file_path is not None:
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
        self. Select_listas_aluno()
        self.apagar_campos_aluno()

    def altera_telefone_aluno(self):
        self.variaveis_aluno()
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
        self.select_listatel_aluno(self.codra)
        self.telefone_entry.delete('0', tk.END)
        self.prioridade_sb.set('')

# Funções Professor

    def apagar_campos_professor(self):

        self.idprofessor_entry.delete('0', tk.END)
        self.nome_entry.delete('0', tk.END)
        self.sobrenome_entry.delete('0', tk.END)
        self.data_nasc_entry.delete('0', tk.END)
        self.email1_entry.delete('0', tk.END)
        self.email2_entry.delete('0', tk.END)
        self.cpf_entry.delete('0', tk.END)
        self.departamento_entry.set('')
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

    def select_listas_professor(self):
        self.listaProf.delete(*self.listaProf.get_children())
        self.conecta_bd()
        self.cursor.execute(
            ("""SELECT * FROM professor_perfil_vw ORDER BY nome, sobrenome"""),)
        listaP = self.cursor.fetchall()

        for i in listaP:
            self.listaProf.insert("", tk.END, values=i)

        self.desconecta_bd()

    def variaveis_professor(self):
        self.idprofessor = self.idprofessor_entry.get()
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

        self.departamento = self.departamento_entry.get()

        if self.departamento:
            self.departamentoid = self.dicDepartamento[self.departamento]
        self.datetime_data_nasc = self.data_nasc_entry.get_date()
        self.data_nasc_datetime = self.datetime_data_nasc.strftime("%Y-%m-%d")

    def addPerfilProfessor(self):
        self.variaveis_professor()
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
                (SELECT idprofessor FROM tbprofessor ORDER BY idprofessor DESC LIMIT 1) as idprofessor
            """
        )
        self.cursor.execute(querrygetid,)
        self.result = self.cursor.fetchone()

        self.idPerfil_ultimo = self.result[0]
        self.idEndereco_ultimo = self.result[1]
        self.idTelefone_ultimo = self.result[2]
        self.idProfessor_ultimo = self.result[3]

        # Verificando se há foto e inserindo o dado na tabela perfil
        if self.file_path is not None:
            self.imagem_bytesIO = io.BytesIO()
            self.imagem_bytes = Image.open(self.file_path)
            self.imagem_bytes = self.imagem_bytes.resize(
                (150, 150), Image.NEAREST)
            self.imagem_bytes.save(self.imagem_bytesIO, "PNG")
            self.imagem_bytesIO.seek(0)
            self.imagem_bytes = self.imagem_bytesIO.read()

            self.cursor.execute(
                ("""UPDATE tbPerfil SET foto = %s WHERE idPerfil = %s"""), (self.imagem_bytes, self.idPerfil_ultimo))

        # Inserindo os dados na tabela tbAluno

        querryCriaraluno = ("""INSERT INTO tbProfessor
                            (idPerfil, idEndereco, iddepartamento)
                            VALUES
                            (%s, %s, %s)
                            """)
        self.cursor.execute(
            querryCriaraluno, (self.idPerfil_ultimo, self.idEndereco_ultimo, self.departamentoid))

        #  Inserindo valores da tabela de junção telefone/aluno
        self.idProfessor_ultimo = self.cursor.lastrowid
        QuerryTelProf = """ INSERT INTO tbProfessor_has_tbTelefone (idProfessor, idTelefone)
                            VALUES (%s, %s);
                        """
        self.cursor.execute(
            QuerryTelProf, (self.idProfessor_ultimo, self.idTelefone_ultimo))

        self.conn.commit()
        self.desconecta_bd()
        self.select_listas_professor()
        self.apagar_campos_professor()

    def select_listatel_professor(self, id):
        self.variaveis_professor()
        self.listaTel.delete(*self.listaTel.get_children())

        self.conecta_bd()
        QuerryT = """SELECT t.prioridade, t.numero
                    FROM tbtelefone t
                    JOIN tbProfessor_has_tbtelefone pht ON t.idtelefone = pht.idtelefone
                    JOIN tbProfessor p ON pht.idprofessor = p.idprofessor
                    where p.idprofessor = %s
                    ORDER BY t.prioridade ;
                    """
        self.cursor.execute(QuerryT, (id,))

        ListaT = self.cursor.fetchall()

        for i in ListaT:
            self.listaTel.insert("", tk.END, values=(i[0], i[1]))

        self.desconecta_bd()

    def OnDoubleClick_professor(self, event):
        self.apagar_campos_professor()
        self.variaveis_professor()
        self.listaProf.selection()
        for n in self.listaProf.selection():
            col1, col2, col3, col4, col5, col6, col7, col8 = self.listaProf.item(
                n, 'values')

            self.idprofessor_entry.insert(tk.END, col1)
            self.nome_entry.insert(tk.END, col2)
            self.sobrenome_entry.insert(tk.END, col3)
            self.data_nasc_entry.insert(tk.END, col4)
            self.email1_entry.insert(tk.END, col5)
            self.email2_entry.insert(tk.END, col6)
            self.cpf_entry.insert(tk.END, col7)

            self.indicedepartamento = list(
                self.dicDepartamento.keys()).index(col8)
            self.departamento_entry.set(list(self.dicDepartamento.keys())[
                                        self.indicedepartamento])

        self.select_listatel_professor(col1)

        self.conecta_bd()

        self.cursor.execute(""" SELECT p.idEndereco
                            FROM tbprofessor p
                            WHERE p.idprofessor = %s """, (self.idprofessor,))
        resultado = self.cursor.fetchone()
        self.idEndereco = resultado[0]
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
                        JOIN tbprofessor tpr ON tpr.idperfil = tp.idperfil
                        WHERE tpr.idprofessor = %s"""
        self.cursor.execute(querryfoto, (self.idprofessor, ))
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

    def onDoubleClicktel_professor(self, event):
        self.variaveis_professor()
        self.telefone_entry.delete('0', tk.END)
        self.prioridade_sb.set('')

        self.listaTel.selection()

        for n in self.listaTel.selection():
            col1, col2 = self.listaTel.item(n, 'values')

            self.telefone_entry.insert(tk.END, col2)
            self.prioridade_sb.insert(tk.END, col1)
        Funcs.telselection = self.telefone_entry.get()

    def deleta_perfil_professor(self):
        self.variaveis_professor()
        self.conecta_bd()

        self.cursor.execute(
            """DELETE FROM tbProfessor WHERE idProfessor = %s """, (self.idprofessor,))

        self.conn.commit()
        self.desconecta_bd()
        self.apagar_campos_professor()
        self.select_listas_professor()

     # Deletar telefone

    def busca_professor(self):
        self.variaveis_professor()
        self.conecta_bd()

        querryBusca = """
             SELECT p.idprofessor,
                p.nome,
                p.sobrenome,
                date_format(p.data_nasc, '%d/%m/%y'),
                p.email1,
                p.email2,
                p.cpf,
                p.departamento
                FROM professor_perfil_vw p
                """

        if not self.data_nasc_entry.get():
            self.data.nasc.set("")

        where_clauses = []
        valores = []

        # Verifica se cada entrada está preenchida e adiciona a cláusula WHERE correspondente

        if self.idprofessor:
            where_clauses.append("pr.idprofessor = %s")
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

        if self.departamento:
            where_clauses.append("p.departamento LIKE %s")
            valores.append(f'%{self.departamento}')

        # Adiciona as cláusulas WHERE à consulta SQL, se houver alguma

        if where_clauses:
            querryBusca += " WHERE " + " AND ".join(where_clauses)

        # Adiciona order by

        querryBusca += """ ORDER BY p.nome, p.sobrenome;"""

        self.cursor.execute(querryBusca, tuple(valores))
        listaBusca = self.cursor.fetchall()

        self.listaProf.delete(*self.listaProf.get_children())

        for i in listaBusca:
            self.listaProf.insert("", tk.END, values=i)

        self.desconecta_bd()

    def altera_professor(self):
        self.variaveis_professor()
        self.conecta_bd()

        if self.file_path is not None:
            self.imagem_bytesIO = io.BytesIO()
            self.imagem_bytes = Image.open(self.file_path)
            self.imagem_bytes = self.imagem_bytes.resize(
                (150, 150), Image.NEAREST)
            self.imagem_bytes.save(self.imagem_bytesIO, "PNG")
            self.imagem_bytesIO.seek(0)
            self.imagem_bytes = self.imagem_bytesIO.read()

        querryUpdt = """ UPDATE tbperfil as p
                            JOIN tbprofessor pr ON pr.idperfil = p.idperfil
                            SET p.nome = %s,
                            p.sobrenome = %s,
                            p.data_nasc = %s,
                            p.email1 = %s,
                            p.email2 = %s,
                            p.cpf = %s,
                            p.foto = %s,
                            pr.iddepartamento = %s
                            WHERE pr.idprofessor = %s  """
        self.cursor.execute(querryUpdt,
                            (self.nome, self.sobrenome,
                             self.data_nasc_datetime, self.email1,
                             self.email2, self.cpf, self.imagem_bytes,
                             self.departamentoid, self.idprofessor)
                            )

        self.conn.commit()
        self.desconecta_bd()
        self. select_listas_professor()
        self.apagar_campos_professor()

    def addTelefone_professor(self):
        self.variaveis_professor()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO tbTelefone (numero, prioridade)
                            VALUES (%s, %s); """, (self.telefone, self.prioridade))

        self.idTelefone_ultimo = self.cursor.lastrowid

        querryPHT = """ INSERT INTO tbProfessor_has_tbTelefone (idProfessor, idTelefone)
                        VALUES (%s, %s); """
        self.cursor.execute(
            querryPHT, (self.idprofessor, self.idTelefone_ultimo))

        self.conn.commit()

        self.desconecta_bd()

        self.select_listatel_professor(self.idprofessor)

    def deleta_telefone_professor(self):
        self.variaveis_professor()
        self.conecta_bd()

        querryidTel = """SELECT tbProfessor_has_tbTelefone.idTelefone
                        FROM  tbProfessor_has_tbTelefone
                        join tbtelefone on tbProfessor_has_tbTelefone.idtelefone = tbtelefone.idtelefone
                        WHERE tbProfessor_has_tbTelefone.idProfessor = %s
                        and tbTelefone.numero = %s"""
        self.cursor.execute(querryidTel, (self.idprofessor, self.telefone))
        self.id_Telefone = self.cursor.fetchone()
        id_Telefone = self.id_Telefone[0] if self.id_Telefone else None
        if id_Telefone is not None:

            self.cursor.execute("""DELETE FROM TbTelefone
                                WHERE tbTelefone.idtelefone = %s
                                and tbTelefone.numero = %s
                                and tbTelefone.prioridade = %s""",
                                (id_Telefone, self.telefone, self.prioridade))
            self.cursor.fetchall()
            self.conn.commit()
            self.select_listatel_professor(self.idprofessor)
        self.desconecta_bd()
        self.telefone_entry.delete('0', tk.END)
        self.prioridade_sb.set('')

    def altera_telefone_professor(self):
        self.variaveis_professor()
        self.conecta_bd()
        querryidTel = """SELECT tbProfessor_has_tbTelefone.idTelefone
                        FROM  tbProfessor_has_tbTelefone
                        join tbtelefone on tbProfessor_has_tbTelefone.idtelefone = tbtelefone.idtelefone
                        WHERE tbProfessor_has_tbTelefone.idProfessor = %s
                        and tbTelefone.numero = %s"""
        self.cursor.execute(
            querryidTel, (self.idprofessor, Funcs.telselection))
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
        self.select_listatel_professor(self.idprofessor)
        self.telefone_entry.delete('0', tk.END)
        self.prioridade_sb.set('')

# Funções Departamento
    def apagar_campos_departamento(self):
        self.nomeDepEntry.delete('0', tk.END)
        self.descricao_entry.delete('1.0', tk.END)
        self.profDepartamentoLista.delete(
            *self.profDepartamentoLista.get_children())
        self.disciplinaDepLista.delete(
            *self.disciplinaDepLista.get_children())
        self.CursosDepartamentoLista.delete(
            *self.CursosDepartamentoLista.get_children())

    def variaveis_departamento(self):
        self.nomeDep = self.nomeDepEntry.get()
        self.descricao = self.descricao_entry.get('1.0', tk.END)

    def select_listas_departamento(self):
        self.listaDep.delete(*self.listaDep.get_children())
        self.profLista.delete(*self.profDepartamentoLista.get_children())

        self.conecta_bd()
        self.cursor.execute(
            ("""SELECT * FROM departamentos_treeview_vw ORDER BY nome"""),)
        listaP = self.cursor.fetchall()

        for i in listaP:
            self.listaDep.insert("", tk.END, values=i)

        self.cursor.execute(
            ("""SELECT p.idprofessor, ConcatNomeProf(p.idprofessor), d.nome
             FROM tbProfessor p JOIN tbDepartamento d ON p.idDepartamento = d.idDepartamento
            ORDER BY ConcatNomeProf(idProfessor) """),)
        listaP = self.cursor.fetchall()

        for i in listaP:
            self.profLista.insert("", tk.END, values=i)

        self.cursor.execute(
            ("""SELECT di.iddisciplina, di.nome, de.nome
             FROM tbdisciplina di JOIN tbDepartamento de
             ON di.idDepartamento = de.idDepartamento
             ORDER BY di.nome """),)
        listaP = self.cursor.fetchall()

        for i in listaP:
            self.disciplinaLista.insert("", tk.END, values=i)

        self.cursor.execute(
            ("""SELECT c.idcurso, c.nome, de.nome
             FROM tbcurso c JOIN tbDepartamento de
             ON c.idDepartamento = de.idDepartamento
             ORDER BY c.nome """),)
        listaP = self.cursor.fetchall()

        for i in listaP:
            self.cursosLista.insert("", tk.END, values=i)

        self.desconecta_bd()

    def onDoubleClick_Departamento(self, event):
        self.apagar_campos_departamento()
        self.variaveis_departamento()
        self.listaDep.selection()
        for n in self.listaDep.selection():
            col1, col2, col3, col4, col5 = self.listaDep.item(
                n, 'values')

            self.idDepartamentoselect = col1
            self.nomeDepEntry.insert(tk.END, col2)
        self.conecta_bd()
        self.cursor.execute(
            (""" SELECT d.descricao from tbdepartamento d
             WHERE d.idDepartamento = %s """), (self.idDepartamentoselect,))
        self.descricaoselect = self.cursor.fetchone()[0]
        if self.descricaoselect is None:
            self.descricaoselect = ''
            self.descricao_entry.insert(tk.END, self.descricaoselect)
        else:
            self.descricao_entry.insert(tk.END, self.descricaoselect)

        self.desconecta_bd()
        self.select_lista_dep_prof(self.idDepartamentoselect)
        self.select_lista_dep_disciplina(self.idDepartamentoselect)
        self.select_lista_dep_cursos(self.idDepartamentoselect)
        self.update_treeviews(self.idDepartamentoselect)

    def select_lista_dep_prof(self, iddepartamento):
        self.conecta_bd()
        self.variaveis_departamento()
        self.profDepartamentoLista.delete(
            *self.profDepartamentoLista.get_children())

        Querry = """SELECT pr.idProfessor, ConcatNomeProf(pr.idProfessor), d.nome
                    FROM tbProfessor pr JOIN tbDepartamento d
                    ON pr.idDepartamento = d.idDepartamento
                    WHERE pr.idDepartamento = %s """

        self.cursor.execute(Querry, (iddepartamento,))

        ListaP = self.cursor.fetchall()

        for i in ListaP:
            self.profDepartamentoLista.insert("", tk.END, values=i)

        self.desconecta_bd()

    def select_lista_dep_disciplina(self, iddepartamento):
        self.conecta_bd()
        self.variaveis_departamento()
        self.disciplinaDepLista.delete(
            *self.disciplinaDepLista.get_children())

        Querry = """SELECT di.idDisciplina, di.nome , de.nome
                    FROM tbDisciplina di JOIN tbDepartamento de
                    ON di.idDepartamento = de.idDepartamento
                    WHERE di.idDepartamento = %s """

        self.cursor.execute(Querry, (iddepartamento,))

        ListaD = self.cursor.fetchall()

        for i in ListaD:
            self.disciplinaDepLista.insert("", tk.END, values=i)

        self.desconecta_bd()

    def select_lista_dep_cursos(self, iddepartamento):
        self.conecta_bd()
        self.variaveis_departamento()
        self.CursosDepartamentoLista.delete(
            *self.CursosDepartamentoLista.get_children())

        Querry = """SELECT c.idCurso, c.nome , de.nome
                    FROM tbCurso c JOIN tbDepartamento de
                    ON c.idDepartamento = de.idDepartamento
                    WHERE c.idDepartamento = %s """

        self.cursor.execute(Querry, (iddepartamento,))

        ListaD = self.cursor.fetchall()

        for i in ListaD:
            self.CursosDepartamentoLista.insert("", tk.END, values=i)

        self.desconecta_bd()

    def update_treeviews(self, iddepartamento):
        self.profLista.delete(*self.profLista.get_children())
        self.disciplinaLista.delete(*self.disciplinaLista.get_children())
        self.cursosLista.delete(*self.cursosLista.get_children())

        self.conecta_bd()
        self.cursor.execute(
            ("""SELECT p.idprofessor, ConcatNomeProf(p.idprofessor), d.nome
             FROM tbProfessor p JOIN tbDepartamento d
             ON p.idDepartamento = d.idDepartamento
             WHERE p.idDepartamento != %s
             ORDER BY ConcatNomeProf(idProfessor)  """), (iddepartamento,))
        listaP = self.cursor.fetchall()

        for i in listaP:
            self.profLista.insert("", tk.END, values=i)

        self.cursor.execute(
            ("""SELECT di.iddisciplina, di.nome, de.nome
             FROM tbdisciplina di JOIN tbDepartamento de
             ON di.idDepartamento = de.idDepartamento
             WHERE di.idDepartamento != %s
             ORDER BY di.nome """), (iddepartamento,))
        listaDi = self.cursor.fetchall()

        for i in listaDi:
            self.disciplinaLista.insert("", tk.END, values=i)

        self.cursor.execute(
            ("""SELECT c.idcurso, c.nome, de.nome
             FROM tbcurso c JOIN tbDepartamento de
             ON c.idDepartamento = de.idDepartamento
             WHERE c.idDepartamento != %s
             ORDER BY c.nome """), (iddepartamento,))
        listaC = self.cursor.fetchall()

        for i in listaC:
            self.cursosLista.insert("", tk.END, values=i)

        self.desconecta_bd()

    def moveProf_to_ProfDep(self):
        linha_selecionada = self.profLista.selection()
        if linha_selecionada:
            valores = self.profLista.item(linha_selecionada, "values")
            if valores not in self.listaProf:
                self.profDepartamentoLista.insert(
                    "", tk.END, values=valores, tags=("inserido",))
                self.profLista.item(linha_selecionada, tags=("copiado",))
                self.listaProf.append(valores)
                print(self.listaProf)
                for item in self.profLista.selection():
                    self.profLista.selection_remove(item)
            else:
                messagebox.showerror(
                    title="ERRO", message="Esta linha já foi adicionada")


class App(Funcs):

    def __init__(self) -> None:
        self.janela = janela
        self.listaProf: list = []
        self.frame_atual = None
        self.file_path = None
        self.imagem_bytes = None
        self.menus()
        self.exibir_Login()

        janela.mainloop()

    def menus(self):
        menubar = tk.Menu(self.janela)
        self.janela.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        filemenu2 = tk.Menu(menubar)
        filemenu3 = tk.Menu(menubar)
        filemenu4 = tk.Menu(menubar)

        def quit(): self.janela.destroy()

        menubar.add_cascade(label="Login",
                            command=self.exibir_Login)
        menubar.add_cascade(label="Cadastro", menu=filemenu2)
        menubar.add_cascade(label="Opções", menu=filemenu3)
        menubar.add_cascade(label="Configurações", menu=filemenu4)

        filemenu2.add_cascade(label="Alunos", command=self.exibir_alunos)
        filemenu2.add_cascade(label="Professores",
                              command=self.exibir_Professor)
        filemenu2.add_cascade(label="Departamentos",
                              command=self.exibir_Departamento)
        filemenu2.add_cascade(label="Cursos")
        filemenu2.add_cascade(label="Disciplinas")
        filemenu2.add_cascade(label="Turmas")

        filemenu3.add_command(label="Sair", command=quit)

# Janela Login

    def tela_Login(self):
        self.janela.title('Login')
        self.janela.minsize(width=700, height=500)

    def exibir_Login(self):
        if self.frame_atual is not None:
            self.frame_atual.destroy()

        self.frame_atual = tk.Frame(self.janela)
        self.frame_atual.pack(fill="both", expand=True)

        self.tela_Login()
        self.framesLogin()
        self.widgetsLogin()

    def framesLogin(self):
        self.frame_login = tk.Frame(self.frame_atual,
                                    bd=5,
                                    bg="darkgrey",
                                    )
        self.frame_login.place(relwidth=0.28, relheight=0.7,
                               relx=0.36, rely=0.15)

    def widgetsLogin(self):
        # Titulo login
        self.texto_login = tk.Label(
            self.frame_login, text="Login", background="darkgrey",
            fg="grey10", font=('Helvetica', 35))
        self.texto_login.configure(justify="center")
        self.texto_login.pack(pady=50, fill='both', expand=True)

        # label e entradas usuario/senha

        self.lb_usuario = tk.Label(
            self.frame_login, text="Usuário", background="darkgrey",
            fg="grey10", font=('Helvetica', 20))
        self.lb_usuario.pack(pady=20, fill='both', expand=True)

        self.usuario_entry = tk.Entry(
            self.frame_login, bg='gray45', fg='grey10',
            width=20, justify='center', font=('helvetica', 20))
        self.usuario_entry.pack(pady=10, fill='both', expand=True)

        self.lb_senha = tk.Label(
            self.frame_login, text="Senha", background="darkgrey",
            fg="grey10", font=('Helvetica', 25))
        self.lb_senha.pack(pady=20, fill='both', expand=True)

        self.senha_entry = tk.Entry(
            self.frame_login, bg='gray45', fg='grey10',
            width=20, justify='center', font=('helvetica', 20),
            show="*")
        self.senha_entry.pack(pady=10, fill='both', expand=True)

        # botao login

        self.bt_login = tk.Button(
            self.frame_login, text="Login", bg='gray45', fg='grey10',
            width=10, height=2, font=('helvetica', 15)
        )

        self.bt_login = tk.Button(
            self.frame_login,
            text="LOGIN",
            bd=2,
            bg='gray45',
            fg='gray10',
            font=('verdana', 20, 'bold'),
        )
        self.bt_login.pack(pady=20, fill='both', expand=True)

# Janela Cadastro Alunos

    def tela_cadastro_aluno(self):
        self.janela.title('Cadastro de Aluno')
        self.janela.configure(background='#549535')
        # self.janela.attributes('-fullscreen', True)
        self.janela.minsize(width=700, height=500)

    def exibir_alunos(self):
        if self.frame_atual is not None:
            self.frame_atual.destroy()

        self.frame_atual = tk.Frame(self.janela)
        self.frame_atual.pack(fill="both", expand=True)

        self.tela_cadastro_aluno()
        self.framesAlunos()
        self.Montar_Dic_Cursos()
        self.widgetsAluno()
        self.Select_listas_aluno()

    def framesAlunos(self):

        # Frame Heading e filhos
        self.frame_heading = tk.Frame(self.frame_atual,
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

        # Frame body e filhos
        self.frame_body = tk.Frame(self.frame_atual,
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

        # Frame bot e filhos

        self.frame_bot = tk.Frame(self.frame_atual,
                                  bd=2,
                                  background='springgreen3')

        self.frame_bot.place(rely=0.67, relx=0.01,
                             relwidth=0.98, relheight=0.32)

    def widgetsAluno(self):

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
            command=self.apagar_campos_aluno

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
            command=self.deleta_perfil_aluno
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
            columns=('col1', 'col2',)
        )
        self.listaTel.heading('#0', text='')
        self.listaTel.heading('#1', text='prioridade')
        self.listaTel.heading('#2', text='número')

        self.listaTel.column('#0', width=1, minwidth=1, anchor='center')
        self.listaTel.column('#1', width=80, anchor='center', minwidth=80)
        self.listaTel.column('#2', width=160, anchor='center', minwidth=160)
        self.listaTel.place(relx=0.02, rely=0.26,
                            relheight=0.5, relwidth=0.9)
        self.listaTel.bind("<Double-1>", self.onDoubleClicktel_aluno)

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
            command=self.addTelefone_aluno
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
            command=self.deleta_telefone_aluno
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
            command=self.altera_telefone_aluno
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
        self.listaAlu.bind("<Double-1>", self.OnDoubleClick_aluno)

# Janela Cadastro Professor
    def tela_cadastro_Professor(self):
        self.janela.title('Cadastro de Professor')
        self.janela.configure(background='steelblue4')
        # self.janela.attributes('-fullscreen', True)
        self.janela.minsize(width=700, height=500)

    def exibir_Professor(self):
        if self.frame_atual is not None:
            self.frame_atual.destroy()

        self.frame_atual = tk.Frame(self.janela)
        self.frame_atual.pack(fill="both", expand=True)

        self.tela_cadastro_Professor()
        self.framesProfessor()
        self.Montar_Dic_Departamentos()
        self.widgetsProfessor()
        self.select_listas_professor()

    def framesProfessor(self):

        # Frame Heading e filhos
        self.frame_heading = tk.Frame(self.frame_atual,
                                      bd=2,
                                      bg='steelblue4'
                                      )
        self.frame_heading.place(relx=0.01, rely=0.01,
                                 relwidth=0.98, relheight=0.15)
        self.texto_top = tk.Label(
            self.frame_heading, text="UniSenai", bg='steelblue4',
            fg='black', font=('Helvetica', 30))
        self.texto_top.configure(justify='center')
        self.texto_top.pack(expand=True)

        # Frame body e filhos
        self.frame_body = tk.Frame(self.frame_atual,
                                   bd=5,
                                   bg='steelblue'
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
                                  bg='steelblue3')

        self.frame_tel.place(rely=0.53, relx=0.13,
                             relwidth=0.17, relheight=0.4)

        self.frame_endereco = tk.Frame(self.frame_body,
                                       bd=2,
                                       bg='steelblue3')
        self.frame_endereco.place(
            rely=0.16, relx=0.35, relheight=0.5, relwidth=0.30)

        self.endereco_title = tk.Label(
            self.frame_endereco, text="Endereço",
            bg='steelblue3', font=('Helvetica', 20))
        self.endereco_title.configure(justify="center")
        self.endereco_title.pack()

        self.frame_btn = tk.Frame(self.frame_body,
                                  bd=2,
                                  bg='steelblue3')
        self.frame_btn.place(
            rely=0.05, relx=0.7, relheight=0.9, relwidth=0.28)

        # Frame bot e filhos

        self.frame_bot = tk.Frame(self.frame_atual,
                                  bd=2,
                                  background='steelblue4')

        self.frame_bot.place(rely=0.67, relx=0.01,
                             relwidth=0.98, relheight=0.32)

    def widgetsProfessor(self):

        self.texto_professor = tk.Label(
            self.frame_body, text="Cadastro Professor", bg='steelblue',
            fg='black', font=('Helvetica', 25))
        self.texto_professor.configure(justify='center')
        self.texto_professor.pack(padx=10)

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
            command=self.apagar_campos_professor

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
            command=self.busca_professor
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
            command=self.addPerfilProfessor
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
            command=self.altera_professor
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
            command=self.deleta_perfil_professor
        )
        self.bt_apagar.place(relx=0.35, rely=0.70,
                             relheight=0.15, relwidth=0.3)

        # ------------------Labels e Entradas frame_body-----------------

        # Criação da label e entrada do idProfessor

        self.lb_idprofessor = tk.Label(
            self.frame_body, text='idProfessor', bg='#dfe3ee', fg='#107db2')
        self.lb_idprofessor.place(relx=0.13, rely=0.1)

        self.idprofessor_entry = tk.Entry(
            self.frame_body, bg='lightgray', fg='#107db2')
        self.idprofessor_entry.place(relx=0.20, rely=0.1, relwidth=0.1)

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
        self.lb_departamento = tk.Label(
            self.frame_body, text='Departamento',
            bg='#dfe3ee', fg='#107db2', font=('helvetica', 15))
        self.lb_departamento.place(relx=0.46, rely=0.67)

        self.departamento_entry = ttk.Combobox(
            self.frame_body,
            background='lightgray',
            foreground='#107db2',
            values=list(self.dicDepartamento.keys()),
            state='readonly',
            font=("helvetica", 20), justify='center')
        self.departamento_entry.place(
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
        self.listaTel.bind("<Double-1>", self.onDoubleClicktel_professor)

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
            command=self.addTelefone_professor
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
            command=self.deleta_telefone_professor
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
            command=self.altera_telefone_professor
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

        self.listaProf = ttk.Treeview(self.frame_bot, height=10,
                                      columns=("col1", "col2",
                                               "col3", "col4",
                                               "col5", "col6",
                                               "col7", "col8"))

        self.listaProf.heading('#0', text='')
        self.listaProf.heading('#1', text='ID')
        self.listaProf.heading('#2', text='Nome')
        self.listaProf.heading('#3', text='Sobrenome')
        self.listaProf.heading('#4', text='Data de Nascimento')
        self.listaProf.heading('#5', text='Email1')
        self.listaProf.heading('#6', text='Email2')
        self.listaProf.heading('#7', text='CPF')
        self.listaProf.heading('#8', text='Departamento')

        self.listaProf.column('#0', width=1, minwidth=1, anchor='center')
        self.listaProf.column('#1', width=80, anchor='center')
        self.listaProf.column('#2', width=100, minwidth=100, anchor='center')
        self.listaProf.column('#3', width=160, minwidth=160, anchor='center')
        self.listaProf.column('#4', width=160, minwidth=160, anchor='center')
        self.listaProf.column('#5', width=160, minwidth=160, anchor='center')
        self.listaProf.column('#6', width=160, minwidth=160, anchor='center')
        self.listaProf.column('#7', width=160, minwidth=160, anchor='center')
        self.listaProf.column('#8', width=100, minwidth=100, anchor='center')
        self.listaProf.place(rely=0.1, relx=0.15, relheight=0.90, relwidth=0.7)

        self.listaProfScroll = tk.Scrollbar(self.frame_bot, orient='vertical',
                                            command=self.listaTel.yview)
        self.listaProf.configure(yscrollcommand=self.listaProfScroll.set)
        self.listaProfScroll.place(
            relx=0.85, rely=0.1,
            relheight=0.9, relwidth=0.02)
        self.listaProf.bind("<Double-1>", self.OnDoubleClick_professor)

# Janela Cadastro Departamento
    def tela_cadastro_Departamento(self):
        self.janela.title('Cadastro de Departamento')
        self.janela.configure(background='khaki')
        # self.janela.attributes('-fullscreen', True)
        self.janela.minsize(width=700, height=500)

    def exibir_Departamento(self):
        if self.frame_atual is not None:
            self.frame_atual.destroy()

        self.frame_atual = tk.Frame(self.janela)
        self.frame_atual.pack(fill="both", expand=True)

        self.tela_cadastro_Departamento()
        self.frames_departamento()
        self.widgetsdepartamento()
        self.select_listas_departamento()

    def frames_departamento(self):

        # Frame Heading e filhos
        self.frame_heading = tk.Frame(self.frame_atual,
                                      bd=2,
                                      bg='khaki'
                                      )
        self.frame_heading.place(relx=0.01, rely=0.01,
                                 relwidth=0.98, relheight=0.15)
        self.texto_top = tk.Label(
            self.frame_heading, text="UniSenai", bg='khaki',
            fg='black', font=('Helvetica', 30))
        self.texto_top.configure(justify='center')
        self.texto_top.pack(expand=True)

        # Frame body e filhos
        self.frame_body = tk.Frame(self.frame_atual,
                                   bd=5,
                                   bg='khaki2'
                                   )
        self.frame_body.place(relx=0.01, rely=0.17,
                              relheight=0.50, relwidth=0.98)
        # Frame Btn
        self.frame_btn = tk.Frame(self.frame_body,
                                  bd=2,
                                  bg='khaki4')
        self.frame_btn.place(
            rely=0.05, relx=0.7, relheight=0.9, relwidth=0.28)
        # Frame Entrys
        self.frame_entrys = tk.Frame(self.frame_body,
                                     bd=2,
                                     bg='khaki4')
        self.frame_entrys.place(
            rely=0.05, relx=0.02, relheight=0.9, relwidth=0.28)

        # Frame Treeviews
        self.frame_treeviews = tk.Frame(self.frame_body,
                                        bd=2,
                                        bg='khaki3')
        self.frame_treeviews.place(
            rely=0.05, relx=0.31, relheight=0.9, relwidth=0.38)

        # Notebook da Treeviews
        self.NoteTreeviews = ttk.Notebook(self.frame_treeviews)

        self.NoteTreeviews.pack(fill='both', expand=True)

        # Abas da Treeviews

        self.abaProf = tk.Frame(self.NoteTreeviews,
                                bd=2,
                                bg="khaki3")
        self.NoteTreeviews.add(self.abaProf, text='Professores')

        self.abaDisc = tk.Frame(self.NoteTreeviews,
                                bd=2,
                                bg="khaki3")
        self.NoteTreeviews.add(self.abaDisc, text='Disciplinas')

        self.abaCursos = tk.Frame(self.NoteTreeviews,
                                  bd=2,
                                  bg="khaki3")
        self.NoteTreeviews.add(self.abaCursos, text='Cursos')

        # Frame bot e filhos

        self.frame_bot = tk.Frame(self.frame_atual,
                                  bd=2,
                                  background='khaki4')

        self.frame_bot.place(rely=0.67, relx=0.01,
                             relwidth=0.98, relheight=0.32)

    def widgetsdepartamento(self):
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
            command=self.apagar_campos_departamento

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
            command=''
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
            command=''
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
            command=''
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
            command=''
        )
        self.bt_apagar.place(relx=0.35, rely=0.70,
                             relheight=0.15, relwidth=0.3)

# Labels e Entradas de nome e descrição

        self.lb_departamento = tk.Label(self.frame_entrys,
                                        text='Nome do departamento',
                                        justify='center',
                                        font=('Helvetica', 20),
                                        bg='khaki4',
                                        relief='flat',
                                        )
        self.lb_departamento.pack(pady=10)
        self.nomeDepEntry = tk.Entry(self.frame_entrys,
                                     background='ivory2',
                                     font=('Helvetica', 16),
                                     justify='center',
                                     width=32,
                                     )
        self.nomeDepEntry.pack(pady=10)
        self.lb_descricao = tk.Label(self.frame_entrys,
                                     text='Descrição',
                                     justify='center',
                                     font=('Helvetica', 20),
                                     bg='khaki4',
                                     relief='flat')
        self.lb_descricao.pack(pady=10)
        self.descricao_entry = tk.Text(self.frame_entrys,
                                       height=7,
                                       font=('Helvetica', 14),
                                       bg='ivory2',
                                       width=35)
        self.descricao_entry.pack(pady=10)

        # TODO remover quando colocar em variaveis
        # Label Professores do Departamento
        self.nomeDep = '<inserir Departamento>'
        self.lb_professores_departamento = tk.Label(self.abaProf,
                                                    text=f'Professores do {self.nomeDep}',
                                                    justify='center',
                                                    font=('Helvetica', 10),
                                                    bg='khaki3')
        self.lb_professores_departamento.place(
            relx=0.01, rely=0.05, relwidth=0.4)

        # Treeview professores do Departamento
        self.profDepartamentoLista = ttk.Treeview(self.abaProf,
                                                  height=10,
                                                  columns=('col1',
                                                           'col2',
                                                           'col3'),)
        self.profDepartamentoLista.heading('#0', text='',)
        self.profDepartamentoLista.heading('#1', text='id')
        self.profDepartamentoLista.heading('#2', text='Nome')
        self.profDepartamentoLista.heading('#3', text='Departamento')
        self.profDepartamentoLista.column(
            '#0', width=1, minwidth=1, anchor='center')

        self.profDepartamentoLista.column(
            '#1', width=40, minwidth=40, anchor='center')

        self.profDepartamentoLista.column(
            '#2', width=150, minwidth=150, anchor='center')
        self.profDepartamentoLista.column(
            '#3', width=100, minwidth=100, anchor='center')

        self.profDepartamentoLista.place(relheight=0.8, relwidth=0.4,
                                         relx=0.01, rely=0.12)
        self.ProfDepListaScroll = tk.Scrollbar(self.abaProf,
                                               orient='vertical',
                                               command=self.profDepartamentoLista.yview)
        self.ProfDepListaScroll2 = tk.Scrollbar(self.abaProf,
                                                orient='horizontal',
                                                command=self.profDepartamentoLista.xview)
        self.profDepartamentoLista.configure(
            yscrollcommand=self.ProfDepListaScroll.set,
            xscrollcommand=self.ProfDepListaScroll2.set)
        self.ProfDepListaScroll.place(
            relx=0.41, rely=0.12,
            relheight=0.8, relwidth=0.02)
        self.ProfDepListaScroll2.place(relx=0.01, rely=0.92, relwidth=0.42,
                                       relheight=0.03)
        # Label Professores
        self.lb_professores = tk.Label(self.abaProf,
                                       text='Professores',
                                       justify='center',
                                       font=('Helvetica', 10),
                                       bg='khaki3')
        self.lb_professores.place(
            relx=0.57, rely=0.05, relwidth=0.4)
        # Treeview professores

        self.profLista = ttk.Treeview(self.abaProf,
                                      height=10,
                                      columns=('col1',
                                               'col2', 'col3'),)
        self.profLista.heading('#0', text='',)
        self.profLista.heading('#1', text='id')
        self.profLista.heading('#2', text='Nome')
        self.profLista.heading('#3', text='Departamento')

        self.profLista.column('#0', width=1, minwidth=1, anchor='center')
        self.profLista.column('#1', width=40, minwidth=40, anchor='center')
        self.profLista.column('#2', width=150, minwidth=150, anchor='center')
        self.profLista.column('#3', width=100, minwidth=100, anchor='center')

        self.profLista.place(relheight=0.8, relwidth=0.4,
                             relx=0.57, rely=0.12)
        self.ProfListaScroll = tk.Scrollbar(self.abaProf, orient='vertical',
                                            command=self.profLista.yview)
        self.ProfListaScroll2 = tk.Scrollbar(self.abaProf, orient='horizontal',
                                             command=self.profLista.xview)
        self.profLista.configure(
            yscrollcommand=self.ProfListaScroll.set,
            xscrollcommand=self.ProfListaScroll2.set)
        self.ProfListaScroll.place(
            relx=0.97, rely=0.12,
            relheight=0.8, relwidth=0.02)
        self.ProfListaScroll2.place(relx=0.57, rely=0.92, relwidth=0.42,
                                    relheight=0.03)

        # Label departamento_disciplinas
        self.lb_departamento_disciplinas = tk.Label(self.abaDisc,
                                                    text=f'Disciplinas do {self.nomeDep}',
                                                    font=("Helvetica", 10),
                                                    background="khaki3"
                                                    )
        self.lb_departamento_disciplinas.place(
            relx=0.01, rely=0.05, relwidth=0.4)

        # Treeview disciplinas do departamento
        self.disciplinaDepLista = ttk.Treeview(self.abaDisc,
                                               height=10,
                                               columns=('col1',
                                                        'col2',
                                                        'col3'))

        self.disciplinaDepLista.heading('#0', text='')
        self.disciplinaDepLista.heading('#1', text='id')
        self.disciplinaDepLista.heading('#2', text='Nome')
        self.disciplinaDepLista.heading('#3', text='Departamento')

        self.disciplinaDepLista.column('#0',
                                       width=1,
                                       minwidth=1,
                                       anchor='center')
        self.disciplinaDepLista.column('#1',
                                       width=40,
                                       minwidth=40,
                                       anchor='center')
        self.disciplinaDepLista.column('#2',
                                       width=150,
                                       minwidth=150,
                                       anchor='center')
        self.disciplinaDepLista.column('#3',
                                       width=100,
                                       minwidth=100,
                                       anchor='center')

        self.disciplinaDepLista.place(relheight=0.8, relwidth=0.4,
                                      relx=0.01, rely=0.12)
        self.disciplinaDepScroll = tk.Scrollbar(self.abaDisc,
                                                orient='vertical',
                                                command=self.disciplinaDepLista.yview)
        self.disciplinaDepScrool2 = tk.Scrollbar(self.abaDisc,
                                                 orient='horizontal',
                                                 command=self.disciplinaDepLista.xview)
        self.disciplinaDepLista.configure(
            yscrollcommand=self.disciplinaDepScroll.set,
            xscrollcommand=self.disciplinaDepScrool2.set)
        self.disciplinaDepScroll.place(
            relx=0.41, rely=0.12,
            relheight=0.8, relwidth=0.02)
        self.disciplinaDepScrool2.place(relx=0.01, rely=0.92, relwidth=0.42,
                                        relheight=0.03)

        # Label Disciplinas
        self.lb_disciplinas = tk.Label(self.abaDisc,
                                       text='Disciplinas',
                                       justify='center',
                                       font=('Helvetica', 10),
                                       bg='khaki3')
        self.lb_disciplinas.place(
            relx=0.57, rely=0.05, relwidth=0.4)

        # Treeview Disciplinas
        self.disciplinaLista = ttk.Treeview(self.abaDisc,
                                            height=10,
                                            columns=('col1',
                                                     'col2',
                                                     'col3',))

        self.disciplinaLista.heading('#0', text='')
        self.disciplinaLista.heading('#1', text='id')
        self.disciplinaLista.heading('#2', text='Nome')
        self.disciplinaLista.heading('#3', text='Departamento')

        self.disciplinaLista.column('#0',
                                    width=1,
                                    minwidth=1,
                                    anchor='center')
        self.disciplinaLista.column('#1',
                                    width=40,
                                    minwidth=40,
                                    anchor='center')
        self.disciplinaLista.column('#2',
                                    width=150,
                                    minwidth=150,
                                    anchor='center')
        self.disciplinaLista.column('#3',
                                    width=100,
                                    minwidth=100,
                                    anchor='center')

        self.disciplinaLista.place(relheight=0.8, relwidth=0.4,
                                   relx=0.57, rely=0.12)
        self.disciplinaListaScroll = tk.Scrollbar(self.abaDisc,
                                                  orient='vertical',
                                                  command=self.disciplinaLista.yview)
        self.disciplinaListaScrooll2 = tk.Scrollbar(self.abaDisc,
                                                    orient='horizontal',
                                                    command=self.disciplinaLista.xview,
                                                    )
        self.disciplinaLista.configure(
            yscrollcommand=self.disciplinaListaScroll.set,
            xscrollcommand=self.disciplinaListaScrooll2.set)
        self.disciplinaListaScroll.place(
            relx=0.97, rely=0.12,
            relheight=0.8, relwidth=0.02)
        self.disciplinaListaScrooll2.place(relx=0.57, rely=0.92, relwidth=0.42,
                                           relheight=0.03)

        # Label CURSOS do Departamento
        self.lb_cursos_departamento = tk.Label(self.abaCursos,
                                               text=f'Cursos do {self.nomeDep}',
                                               justify='center',
                                               font=('Helvetica', 10),
                                               bg='khaki3')
        self.lb_cursos_departamento.place(
            relx=0.01, rely=0.05, relwidth=0.4)

        # Treeview Cursos do Departamento
        self.CursosDepartamentoLista = ttk.Treeview(self.abaCursos,
                                                    height=10,
                                                    columns=('col1',
                                                             'col2',
                                                             'col3'),)
        self.CursosDepartamentoLista.heading('#0', text='',)
        self.CursosDepartamentoLista.heading('#1', text='id')
        self.CursosDepartamentoLista.heading('#2', text='Nome')
        self.CursosDepartamentoLista.heading('#3', text='Departamento')
        self.CursosDepartamentoLista.column(
            '#0', width=1, minwidth=1, anchor='center')

        self.CursosDepartamentoLista.column(
            '#1', width=40, minwidth=40, anchor='center')

        self.CursosDepartamentoLista.column(
            '#2', width=150, minwidth=150, anchor='center')
        self.CursosDepartamentoLista.column(
            '#3', width=100, minwidth=100, anchor='center')

        self.CursosDepartamentoLista.place(relheight=0.8, relwidth=0.4,
                                           relx=0.01, rely=0.12)
        self.CursosDepListaScroll = tk.Scrollbar(self.abaCursos,
                                                 orient='vertical',
                                                 command=self.CursosDepartamentoLista.yview)
        self.CursosDepListaScroll2 = tk.Scrollbar(self.abaCursos,
                                                  orient='horizontal',
                                                  command=self.CursosDepartamentoLista.xview)
        self.CursosDepartamentoLista.configure(
            yscrollcommand=self.CursosDepListaScroll.set,
            xscrollcommand=self.CursosDepListaScroll2.set)
        self.CursosDepListaScroll.place(
            relx=0.41, rely=0.12,
            relheight=0.8, relwidth=0.02)
        self.CursosDepListaScroll2.place(relx=0.01, rely=0.92, relwidth=0.42,
                                         relheight=0.03)
        # Label Professores
        self.lb_cursos = tk.Label(self.abaCursos,
                                  text='Professores',
                                  justify='center',
                                  font=('Helvetica', 10),
                                  bg='khaki3')
        self.lb_cursos.place(
            relx=0.57, rely=0.05, relwidth=0.4)
        # Treeview cursos

        self.cursosLista = ttk.Treeview(self.abaCursos,
                                        height=10,
                                        columns=('col1',
                                                 'col2', 'col3'),)
        self.cursosLista.heading('#0', text='',)
        self.cursosLista.heading('#1', text='id')
        self.cursosLista.heading('#2', text='Nome')
        self.cursosLista.heading('#3', text='Departamento')

        self.cursosLista.column('#0', width=1, minwidth=1, anchor='center')
        self.cursosLista.column('#1', width=40, minwidth=40, anchor='center')
        self.cursosLista.column('#2', width=150, minwidth=150, anchor='center')
        self.cursosLista.column('#3', width=100, minwidth=100, anchor='center')

        self.cursosLista.place(relheight=0.8, relwidth=0.4,
                               relx=0.57, rely=0.12)
        self.cursosListaScroll = tk.Scrollbar(self.abaCursos, orient='vertical',
                                              command=self.cursosLista.yview)
        self.cursosListaScroll2 = tk.Scrollbar(self.abaCursos, orient='horizontal',
                                               command=self.cursosLista.xview)
        self.cursosLista.configure(
            yscrollcommand=self.cursosListaScroll.set,
            xscrollcommand=self.cursosListaScroll2.set)
        self.cursosListaScroll.place(
            relx=0.97, rely=0.12,
            relheight=0.8, relwidth=0.02)
        self.cursosListaScroll2.place(relx=0.57, rely=0.92, relwidth=0.42,
                                      relheight=0.03)

        # Botoes adicionar retirar Professor_departamento

        self.btnproftodep = tk.Button(self.abaProf,
                                      bg="lavenderblush1",
                                      fg="ivory4",
                                      text="<<< ",
                                      width=3,
                                      height=1,
                                      command=self.moveProf_to_ProfDep)
        self.btnproftodep.place(relx=0.5, rely=0.20, anchor="center")

        self.btndeptoprof = tk.Button(self.abaProf,
                                      bg="lavenderblush1",
                                      fg="ivory4",
                                      text=" >>>",
                                      width=3,
                                      height=1)
        self.btndeptoprof.place(relx=0.5, rely=0.30, anchor="center")

        # Botoes confirmar e desfazer de Professor_departamento

        self.btnconfirm_prof = tk.Button(self.abaProf,
                                         bg='#107bd2',
                                         text="confirmar",
                                         font=('Helvetica', 8))
        self.btnconfirm_prof.place(
            relx=0.5, rely=0.38, relwidth=0.085, relheight=0.05, anchor='center')

        self.btndes_prof = tk.Button(self.abaProf,
                                     bg='#107bd2',
                                     text="desfazer",
                                     font=('Helvetica', 8))
        self.btndes_prof.place(
            relx=0.5, rely=0.46, relwidth=0.085, relheight=0.05, anchor='center')

        # Botoes adicionar retirar Disciplina_departamento

        self.btndisctodep = tk.Button(self.abaDisc,
                                      bg="lavenderblush1",
                                      fg="ivory4",
                                      text="<<< ",
                                      width=3,
                                      height=1)
        self.btndisctodep.place(relx=0.5, rely=0.2, anchor="center")

        self.btndeptodisc = tk.Button(self.abaDisc,
                                      bg="lavenderblush1",
                                      fg="ivory4",
                                      text=" >>>",
                                      width=3,
                                      height=1)
        self.btndeptodisc.place(relx=0.5, rely=0.3, anchor="center")

        # Botoes confirmar e desfazer de Disciplina_departamento

        self.btnconfirm_disci = tk.Button(self.abaDisc,
                                          bg='#107bd2',
                                          text="confirmar",
                                          font=('Helvetica', 8))
        self.btnconfirm_disci.place(
            relx=0.5, rely=0.38, relwidth=0.085, relheight=0.05, anchor='center')

        self.btndes_disci = tk.Button(self.abaDisc,
                                      bg='#107bd2',
                                      text="desfazer",
                                      font=('Helvetica', 8))
        self.btndes_disci.place(
            relx=0.5, rely=0.46, relwidth=0.085, relheight=0.05, anchor='center')

        # Botoes adicionar retirar Curso_departamento

        self.btncursotodep = tk.Button(self.abaCursos,
                                       bg="lavenderblush1",
                                       fg="ivory4",
                                       text="<<< ",
                                       width=3,
                                       height=1)
        self.btncursotodep.place(relx=0.5, rely=0.20, anchor="center")

        self.btndeptocurso = tk.Button(self.abaCursos,
                                       bg="lavenderblush1",
                                       fg="ivory4",
                                       text=" >>>",
                                       width=3,
                                       height=1)
        self.btndeptocurso.place(relx=0.5, rely=0.30, anchor="center")

        # Botoes confirmar e desfazer de curso_departamento

        self.btnconfirm_curso = tk.Button(self.abaCursos,
                                          bg='#107bd2',
                                          text="confirmar",
                                          font=('Helvetica', 8))
        self.btnconfirm_curso.place(
            relx=0.5,
            rely=0.38,
            relwidth=0.085,
            relheight=0.05,
            anchor='center')

        self.btndes_curso = tk.Button(self.abaCursos,
                                      bg='#107bd2',
                                      text="desfazer",
                                      font=('Helvetica', 8))
        self.btndes_curso.place(
            relx=0.5,
            rely=0.46,
            relwidth=0.085,
            relheight=0.05,
            anchor='center')

        # Treeview do departamento

        self.listaDep = ttk.Treeview(self.frame_bot, height=10,
                                     columns=("col1", "col2",
                                              "col3", "col4",
                                              "col5"))

        self.listaDep.heading('#0', text='')
        self.listaDep.heading('#1', text='ID')
        self.listaDep.heading('#2', text='Nome')
        self.listaDep.heading('#3', text='Nº de Professores')
        self.listaDep.heading('#4', text='Nº de Disciplinas')
        self.listaDep.heading('#5', text='Nº de Cursos')

        self.listaDep.column('#0', width=1, minwidth=1, anchor='center')
        self.listaDep.column('#1', width=60, minwidth=60, anchor='center')
        self.listaDep.column('#2', width=240, minwidth=240, anchor='center')
        self.listaDep.column('#3', width=160, minwidth=160, anchor='center')
        self.listaDep.column('#4', width=160, minwidth=160, anchor='center')
        self.listaDep.column('#5', width=160, minwidth=160, anchor='center')

        self.listaDep.place(rely=0.1, relx=0.25, relheight=0.90, relwidth=0.5)

        self.listaDepScroll = tk.Scrollbar(self.frame_bot, orient='vertical',
                                           command=self.listaDep.yview)
        self.listaDep.configure(yscrollcommand=self.listaDepScroll.set)
        self.listaDepScroll.place(
            relx=0.75, rely=0.1,
            relheight=0.90, relwidth=0.02)

        self.listaDep.bind("<Double-1>", self.onDoubleClick_Departamento)

        self.profLista.tag_configure(
            "copiado", background="red")
        self.profDepartamentoLista.tag_configure(
            "inserido", background="green")


App()
