from faker import Faker, Factory
from mysql.connector import connect
import traceback
from random import choice, choices, randint
fake = Faker('pt-BR')


cursos = [
    {"id": 1, "nome": "Engenharia de Computação", "codDep": 1},
    {"id": 2, "nome": "Ciência da Computação", "codDep": 2},
    {"id": 3, "nome": "Engenharia de Software", "codDep": 1},
    {"id": 4, "nome": "Sistemas de Informação", "codDep": 3},
    {"id": 5, "nome": "Engenharia de Redes de Computadores", "codDep": 4},
    {"id": 6, "nome": "Engenharia de Sistemas", "codDep": 1},
    {"id": 7, "nome": "Engenharia de Mídias Digitais", "codDep": 1},
    {"id": 8, "nome": "Tecnologia em Jogos Digitais", "codDep": 2},
    {"id": 9, "nome": "Tecnologia em Segurança da Informação", "codDep": 3},
    {"id": 10, "nome": "Ciência de Dados", "codDep": 2},
]

departamentos = [
    {"id": 1, "nome": "Departamento de Engenharia da Computação"},
    {"id": 2, "nome": "Departamento de Ciência da Computação"},
    {"id": 3, "nome": "Departamento de Tecnologia da Informação"},
    {"id": 4, "nome": "Departamento de Sistemas e Redes"}
]

disciplinas = {
    "Engenharia de Computação": [
        "Arquitetura de Computadores",
        "Sistemas Digitais",
        "Redes de Computadores",
        "Programação Orientada a Objetos",
        "Inteligência Artificial",
        "Engenharia de Software ",
        "Banco de Dados ",
        "Compiladores ",
        "Segurança da Informação "
    ],

    "Ciência da Computação": [
        "Estruturas de Dados",
        "Algoritmos",
        "Banco de Dados",
        "Compiladores",
        "Segurança da Informação",
        "Redes de Computadores ",
        "Programação Orientada a Objetos ",
        "Inteligência Artificial ",
        "Engenharia de Requisitos "
    ],

    "Engenharia de Software": [
        "Engenharia de Requisitos",
        "Testes de Software",
        "Desenvolvimento Ágil",
        "Engenharia de Software Orientada a Serviços",
        "Qualidade de Software",
        "Estruturas de Dados ",
        "Algoritmos ",
        "Arquitetura de Computadores ",
        "Sistemas Digitais "
    ],

    "Sistemas de Informação": [
        "Gestão de Projetos de TI",
        "Análise e Projeto de Sistemas",
        "Gestão da Informação",
        "Sistemas de Informação Gerenciais",
        "Engenharia de Software para Sistemas de Informação",
        "Administração de Redes ",
        "Segurança de Redes ",
        "Protocolos de Comunicação ",
        "Redes Sem Fio "
    ],

    "Engenharia de Redes de Computadores": [
        "Administração de Redes",
        "Segurança de Redes",
        "Protocolos de Comunicação",
        "Redes Sem Fio",
        "Redes de Alta Velocidade",
        "Engenharia de Software ",
        "Qualidade de Software ",
        "Desenvolvimento Ágil ",
        "Engenharia de Software Orientada a Serviços "
    ],

    "Engenharia de Sistemas": [
        "Análise de Sistemas",
        "Projeto de Sistemas",
        "Gestão de Projetos de Sistemas",
        "Arquitetura de Sistemas",
        "Integração de Sistemas Empresariais",
        "Arte Interativa ",
        "Jogos Digitais ",
        "Animação Computacional ",
        "Design Digital "
    ],

    "Engenharia de Mídias Digitais": [
        "Design Digital",
        "Produção de Conteúdo Digital",
        "Arte Interativa",
        "Jogos Digitais",
        "Animação Computacional",
        "Engenharia de Software ",
        "Testes de Software ",
        "Desenvolvimento Ágil ",
        "Engenharia de Software Orientada a Serviços "
    ],

    "Tecnologia em Jogos Digitais": [
        "Design de Jogos",
        "Programação de Jogos",
        "Arte para Jogos",
        "Produção de Jogos",
        "Narrativa Interativa",
        "Gestão de Projetos de TI ",
        "Análise e Projeto de Sistemas ",
        "Gestão da Informação ",
        "Sistemas de Informação Gerenciais "
    ],

    "Tecnologia em Segurança da Informação": [
        "Segurança de Redes",
        "Criptografia",
        "Forense Computacional",
        "Segurança de Sistemas Operacionais",
        "Teste de Invasão",
        "Estruturas de Dados ",
        "Algoritmos ",
        "Banco de Dados ",
        "Compiladores "
    ],

    "Ciência de Dados": [
        "Mineração de Dados",
        "Análise Estatística",
        "Aprendizado de Máquina",
        "Visualização de Dados",
        "Big Data Analytics",
        "Gestão de Projetos de TI ",
        "Análise e Projeto de Sistemas ",
        "Gestão da Informação ",
        "Sistemas de Informação Gerenciais "
    ]
}


class Professor(Factory):
    contador_departamento = 0

    def __init__(self) -> None:
        self.nome = fake.unique.name()
        self.telefone = fake.msisdn()
        self.email = fake.email()
        self.endereco = fake.address()
        self.salario = choice([4140.50, 4870.00, 5100.75, 5620.25])
        Professor.contador_departamento += 1
        self.codDepartamento = Professor.contador_departamento
        if Professor.contador_departamento == 4:
            Professor.contador_departamento = 0

    def montar_dict(self):
        return {'nome': self.nome,
                'telefone': self.telefone,
                'email': self.email,
                'endereco': self.endereco,
                'salario': self.salario,
                'codDepartamento': self.codDepartamento
                }


class Aluno(Factory):
    def __init__(self) -> None:
        self.nome = fake.unique.name()
        self.telefone = fake.msisdn()
        self.endereco = fake.address()
        self.statusmatricula = self.gerar_status_matricula()
        self.data_nasc = fake.date_of_birth(minimum_age=16, maximum_age=50)
        self.codCurso = choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def montar_dict(self):
        return self.__dict__

    def gerar_status_matricula(self):
        opcoes = ["Ativa", "Inativa"]
        probabilidade = [0.7, 0.3]
        return choices(opcoes, probabilidade)[0]


class Endereco(Factory):
    def __init__(self) -> None:
        self.cep = fake.postcode()
        self.estado = fake.estado_sigla()
        self.cidade = fake.city()
        self.bairro = fake.neighborhood()
        self.logradouro = fake.street_name()
        self.numero = choice([1, 100])

    def montar_dict(self):
        print(self.__dict__)
        return self.__dict__


class funcs(Professor, Aluno, Endereco):
    def conectar(self):
        self.cnx = connect(
            host="localhost",
            user="root",
            password="Ricardo&Danubia",
            db='dbricardo')
        print('Conectando ao banco de dados')
        self.cursor = self.cnx.cursor()
        self.cursor.execute("USE dbricardo;")

    def desconectar(self):
        self.cnx.close()
        print('Desconectando do banco de dados')

    def inserir_Departamento(self):

        self.conectar()
        try:
            for departamento in departamentos:
                querry = """INSERT INTO tbDepartamento (codDepartamento, nome)
                                VALUES (%s, %s)"""
                dados = (departamento["id"], departamento["nome"])
                self.cursor.execute(querry, dados)
                self.cnx.commit()
                print(
                    f"Departamento: {departamento['nome']} cod: {departamento['id']} adicionado com sucesso")
        except Exception as e:
            print(
                f"Erro ao inserir dados na tabela tbDepartamento[ id:{departamento['id']} nome:{departamento['nome']}],erro: {e}")
            self.cnx.rollback()
            traceback.print_exc()
        finally:
            self.desconectar()

    def inserir_Curso(self):

        for curso in cursos:
            self.conectar()
            try:

                querry = """INSERT INTO tbcurso (codCurso, nome, codDepartamento)
                            VALUES (%s, %s, %s)"""
                dados = (curso["id"], curso["nome"], curso["codDep"])
                self.cursor.execute(querry, dados)
                self.cnx.commit()
                print(
                    f"Curso: {curso['nome']} cod ={curso['id']} cadastrado com sucesso")
            except Exception as e:
                print(
                    f"Erro ao inserir dados na tabela tbcurso[ id:{curso['id']} nome:{curso['nome']} codDep {curso['codDep']}],erro: {e}")
                self.cnx.rollback()
                traceback.print_exc()

            finally:
                self.desconectar()

    def inserir_Disciplina(self):

        self.conectar()
        try:
            for curso, listadisciplina in disciplinas.items():
                for disciplina in listadisciplina:
                    print(
                        f'curso: {curso}, listadisciplina: {listadisciplina}, disciplina: {disciplina}')
                    querrycodcurso = """SELECT tbCurso.codCurso, tbcurso.codDepartamento
                                                            FROM tbCurso
                                                            WHERE tbCurso.nome like %s """
                    dados = (curso,)
                    self.cursor.execute(querrycodcurso, dados)
                    self.results = self.cursor.fetchone()
                    self.idcurso = self.results[0]
                    self.cursoDep = self.results[1]
                    querryDisc = """INSERT INTO tbDisciplina (nome, codDepartamento)
                                        VALUES (%s, %s)"""
                    dadosDisc = (disciplina, self.cursoDep)

                    self.cursor.execute(
                        querryDisc, dadosDisc)
                    self.cnx.commit()

        except Exception as e:
            print(f"Erro ao adicionar aluno na tabela matricula {e}")
            self.cnx.rollback()
            traceback.print_exc()
        finally:
            self.desconectar()

    def inserir_CursohasDisciplina(self):

        for curso, listadisciplina in disciplinas.items():
            self.conectar()
            print(f'curso: {curso}, listadisciplina: {listadisciplina}')
            try:

                try:
                    for disciplina in listadisciplina:
                        print(
                            f'curso: {curso}, listadisciplina: {listadisciplina}, disciplina: {disciplina}')
                        querrycodcurso = """SELECT tbCurso.codCurso, tbcurso.codDepartamento
                                                            FROM tbCurso
                                                            WHERE tbCurso.nome like %s """
                        dados = (curso,)
                        self.cursor.execute(querrycodcurso, dados)
                        self.results = self.cursor.fetchone()
                        self.idcurso = self.results[0]

                        self.cursoDep = self.results[1]
                        querrycodDisc = """SELECT tbDisciplina.codDisciplina
                                            FROM tbDisciplina
                                            WHERE tbDisciplina.nome like %s
                                            AND tbDisciplina.codDepartamento = %s"""
                        dadoscoDisc = (disciplina, self.cursoDep)

                        self.cursor.execute(
                            querrycodDisc, dadoscoDisc)
                        self.codDis = self.cursor.fetchone()[0]
                        self.cursor.fetchall()
                        querryDisc = """INSERT INTO tbCurso_has_tbDisciplina (codCurso, codDisciplina)
                                        VALUES ( %s, %s)"""
                        dadosdisc = (self.idcurso, self.codDis)
                        self.cursor.execute(querryDisc, dadosdisc)
                        self.cnx.commit()

                except Exception as e:
                    print(
                        f"Erro ao inserir dados na tabela tbcurso_has_tbDisciplina[nomeDiciplina: {disciplina} idCurso: {self.idcurso}], erro {e}")
                    traceback.print_exc()
                    self.cnx.rollback()

            except Exception as e:
                print(
                    f"Erro ao inserir dados na tabela tbcurso_has_tbDisciplina [nomeCurso: {curso}],erro: {e}")
                self.cnx.rollback()
                traceback.print_exc()

            self.desconectar()

    def inserir_professores(self):
        for professor in professores:
            try:
                self.conectar()
                querry = """INSERT INTO tbProfessor(nome, telefone, email,
                            endereco, salario, codDepartamento)
                            VALUES (%s, %s, %s, %s, %s, %s)"""
                dados = (professor['nome'],
                         professor['telefone'],
                         professor['email'],
                         professor['endereco'],
                         professor['salario'],
                         professor['codDepartamento'])
                self.cursor.execute(querry, dados)
                self.cnx.commit()
                self.desconectar()
            except Exception as e:
                print(f"Erro ao cadastrar na tabela professor {e}")
                self.cnx.rollback()
                self.desconectar()
                traceback.print_exc()

    def inserir_Turmas(self):

        try:
            self.conectar()
            querryDisciplinas = """ SELECT di.codDisciplina, di.nome
                                    FROM tbDisciplina di  """
            self.cursor.execute(querryDisciplinas)
            listaDisciplinas = self.cursor.fetchall()
            for id, disciplina in listaDisciplinas:
                print(f'id: {id} disciplina: {disciplina}')
                c = 0
                for _ in range(choice([1, 2, 3])):
                    c += 1
                    nometurma = (f"{disciplina}-{c}")
                    horario = choice(['8:00:00', '10:00:00', '14:00:00'])
                    sala = fake.building_number()
                    querryTurma = """INSERT INTO tbTurma (nome, horario, sala, codDisciplina)
                                        Values (%s, %s, %s, %s)"""
                    dados = tuple((nometurma, horario, sala, id))
                    self.cursor.execute(querryTurma, dados)
                    self.cnx.commit()
            self.desconectar()

        except Exception as e:
            print(
                f"Erro ao cadastrar na tabela Turma [nomeT= {nometurma}, horario= {horario}, sala={sala}, id={id}] {e}")
            self.cnx.rollback()
            self.desconectar()
            traceback.print_exc()

    def inserir_Alunos(self):
        self.conectar()
        try:
            c = 0
            for aluno in alunos:
                c += 1

                querry = """INSERT INTO tbAluno (nome, telefone, endereco,
                            statusmatricula, data_nasc, codCurso)
                            VALUES (%s, %s, %s, %s, %s, %s)"""
                dados = (aluno['nome'],
                         aluno['telefone'],
                         aluno['endereco'],
                         aluno['statusmatricula'],
                         aluno['data_nasc'],
                         aluno['codCurso'])
                self.cursor.execute(querry, dados)
                self.cnx.commit()
                print(f"{c}º Aluno Cadastrado com sucesso")
        except Exception as e:
            print(f"Erro ao cadastrar na tabela Aluno {e}")
            self.cnx.rollback()
            traceback.print_exc()
        finally:
            self.desconectar()

    def matricular_alunos_turma(self, turma):
        self.conectar()
        try:
            alunosturmaQuerry = """SELECT CODRA
                                    FROM dbricardo.tbaluno
                                    WHERE codCurso = 2
                                    AND statusmatricula like 'Ativa' LIMIT 30;
                                    """
            self.cursor.execute(alunosturmaQuerry,)
            alunosturmalista = self.cursor.fetchall()
            codraTurma = [codra[0] for codra in alunosturmalista]
            print(codraTurma)
            c = 0
            for codra in codraTurma:
                c += 1
                querry = """INSERT INTO TBmatricula(codra, codTurma, semestre, data_matricula)
                            VALUES (%s, %s, %s, curdate())"""
                dados = (codra, turma, "02/24")
                self.cursor.execute(querry, (dados))
                self.cnx.commit()
                print(f"{c}º Aluno matriculado com sucesso")

        except Exception as e:
            print(f"Erro ao adicionar aluno na tabela matricula {e}")
            self.cnx.rollback()
            traceback.print_exc()
        finally:
            self.desconectar()

    def matricular_aluno_em_turmas(self, codra):
        self.conectar()
        try:
            turmasQuerry = """SELECT codTurma FROM tbturma
                                WHERE codDisciplina
                                BETWEEN 1
                                AND 9 LIMIT 9"""
            self.cursor.execute(turmasQuerry,)
            turmalista = self.cursor.fetchall()
            codTurmalista = [codTurma[0] for codTurma in turmalista]
            c = 0
            for codTurma in codTurmalista:
                c += 1
                querry = """INSERT INTO TBmatricula(codra, codTurma, semestre, data_matricula)
                            VALUES (%s, %s, %s, curdate())"""
                dados = (codra, codTurma, "02/24")
                self.cursor.execute(querry, (dados))
                self.cnx.commit()
                print(f" Aluno matriculado em {c} turmas com sucesso")

        except Exception as e:
            print(f"Erro ao adicionar aluno na tabela matricula {e}")
            self.cnx.rollback()
            traceback.print_exc()
        finally:
            self.desconectar()

    def inserir_professores_disciplinas(self):
        self.conectar()
        try:
            querryprof = """SELECT codProfessor, codDepartamento FROM tbprofessor"""
            self.cursor.execute(querryprof,)
            proflista = self.cursor.fetchall()
            querrydisc = """SELECT codDisciplina, codDepartamento FROM tbdisciplina"""
            self.cursor.execute(querrydisc,)
            disclista = self.cursor.fetchall()

            disciplinacadastrada = []
            for codprof, coddeprof in proflista:
                variavel = choice([2, 3, 4])
                c = 0
                for coddisc, coddisdep in disclista:
                    if coddisc in disciplinacadastrada:
                        pass

                    elif coddeprof == coddisdep:
                        c = c + 1
                        print(
                            f'codprof: {codprof}, coddisc:{coddisc}, codDiscDep: {coddisdep} codprofDep{coddeprof} c={c}, variavel {variavel}')
                        disciplinacadastrada.append(coddisc)
                        Querry = """INSERT INTO tbProfessor_has_tbDisciplina
                                    (codProfessor, codDisciplina)
                                    VALUES (%s, %s)"""
                        dados = (codprof, coddisc)
                        self.cursor.execute(Querry, dados)
                        self.cnx.commit()
                        print(
                            f"Adicionada entrada: [prof: {codprof}, disc: {coddisc}]")

                    if c == variavel:
                        c = 0
                        break

        except Exception as e:
            print(
                f"Erro ao adicionar na aluna tbprofessor_has_tbDisciplina {e}")
            self.cnx.rollback()
            traceback.print_exc()
        finally:
            self.desconectar()

    def inserir_endereco_alunos(self):
        try:
            self.conectar()
            self.cursor.execute("""SELECT codRa from tbaluno""")
            alunos = self.cursor.fetchall()
            alunos = tuple(tupla for tupla in alunos)
            for aluno in alunos:
                endereco = Endereco().montar_dict()
                querryend = """
                        INSERT INTO tbEndereco(cep, estado, cidade, bairro, logradouro, numero)
                        VALUES (%s, %s, %s, %s, %s, %s)"""
                dadosend = (
                    endereco['cep'],
                    endereco['estado'],
                    endereco['cidade'],
                    endereco['bairro'],
                    endereco['logradouro'],
                    endereco['numero'],
                )

                self.cursor.execute(querryend, dadosend)
                idendereco = self.cursor.lastrowid
                dadosalu = (idendereco, aluno[0])

                querryalu = """UPDATE tbaluno
                                SET codEndereco = %s
                                WHERE codra = %s"""
                print(dadosalu)
                self.cursor.execute(querryalu, dadosalu)
            self.cnx.commit()
        except Exception as e:
            print(
                f"Erro ao adicionar na endereco do aluno {e}")
            self.cnx.rollback()
            traceback.print_exc()
        finally:
            self.desconectar()

    def inserir_endereco_professor(self):
        try:
            self.conectar()
            self.cursor.execute("""SELECT codProfessor from tbprofessor""")
            professores = self.cursor.fetchall()
            professores = tuple(tupla for tupla in professores)
            for professor in professores:
                endereco = Endereco().montar_dict()
                querryend = """
                        INSERT INTO tbEndereco(cep, estado, cidade, bairro, logradouro, numero)
                        VALUES (%s, %s, %s, %s, %s, %s)"""
                dadosend = (
                    endereco['cep'],
                    endereco['estado'],
                    endereco['cidade'],
                    endereco['bairro'],
                    endereco['logradouro'],
                    endereco['numero'],
                )

                self.cursor.execute(querryend, dadosend)
                idendereco = self.cursor.lastrowid
                dadosprof = (idendereco, professor[0])

                querryalu = """UPDATE tbProfessor
                                SET codEndereco = %s
                                WHERE codprofessor = %s"""
                print(dadosprof)
                self.cursor.execute(querryalu, dadosprof)
            self.cnx.commit()
        except Exception as e:
            print(
                f"Erro ao adicionar na endereco do professor {e}")
            self.cnx.rollback()
            traceback.print_exc()
        finally:
            self.desconectar()

    def inserir_telefone_alunos(self):
        try:
            self.conectar()
            self.cursor.execute("""SELECT codRa from tbaluno""")
            alunos = self.cursor.fetchall()
            alunos = tuple(tupla for tupla in alunos)
            for aluno in alunos:

                for p in range(randint(1, 3)):
                    tel = fake.msisdn()
                    querrytel = """INSERT INTO tbTelefone (numero, prioridade)
                                VALUES (%s, %s)"""
                    self.cursor.execute(querrytel, (tel, p + 1))
                    codTelefone = self.cursor.lastrowid
                    querrytelalu = """INSERT INTO tbAluno_has_tbTelefone (codra, codTelefone)
                                VALUES (%s, %s)"""
                    self.cursor.execute(querrytelalu, (aluno[0], codTelefone))
                    print(f'p={p + 1}, tel={tel}')
            self.cnx.commit()
        except Exception as e:
            print(
                f"Erro ao adicionar na endereco do aluno {e}")
            self.cnx.rollback()
            traceback.print_exc()
        finally:
            self.desconectar()

    def inserir_telefone_professor(self):
        try:
            self.conectar()
            self.cursor.execute("""SELECT codProfessor from tbProfessor""")
            professores = self.cursor.fetchall()
            professores = tuple(tupla for tupla in professores)
            for professor in professores:

                for p in range(randint(1, 3)):
                    tel = fake.msisdn()
                    querrytel = """INSERT INTO tbTelefone (numero, prioridade)
                                VALUES (%s, %s)"""
                    self.cursor.execute(querrytel, (tel, p + 1))
                    codTelefone = self.cursor.lastrowid
                    querrytelprof = """INSERT INTO tbProfessor_has_tbTelefone (codProfessor, codTelefone)
                                VALUES (%s, %s)"""
                    self.cursor.execute(
                        querrytelprof, (professor[0], codTelefone))
                    print(f'p={p + 1}, tel={tel}')
            self.cnx.commit()
        except Exception as e:
            print(
                f"Erro ao adicionar na endereco do aluno {e}")
            self.cnx.rollback()
            traceback.print_exc()
        finally:
            self.desconectar()

    def inserir_email_cpf_alunos(self):
        try:
            self.conectar()
            self.cursor.execute("""SELECT codRa from tbaluno""")
            alunos = self.cursor.fetchall()
            alunos = tuple(tupla for tupla in alunos)
            for aluno in alunos:

                for p in range(randint(1, 3)):
                    cpf = fake.ssn()
                    email = fake.email()
                    print(f"cpf= {cpf} email= {email}, aluno= {aluno}")
                    querryalu = """UPDATE tbAluno
                                    SET cpf = %s,
                                    email = %s
                                    WHERE codra = %s"""
                    self.cursor.execute(querryalu, (cpf, email, aluno[0]))
                self.cnx.commit()
        except Exception as e:
            print(
                f"Erro ao adicionar na endereco do aluno {e}")
            self.cnx.rollback()
            traceback.print_exc()
        finally:
            self.desconectar()


# funcs().inserir_Departamento()
# funcs().inserir_Curso()
# funcs().inserir_Disciplina()
# funcs().inserir_CursohasDisciplina()
# funcs().inserir_Turmas()
# alunos = [Aluno().montar_dict() for _ in range(3000)]
# funcs().inserir_Alunos()
# professores = [Professor().montar_dict() for _ in range(40)]
# funcs().inserir_professores()
# funcs().inserir_professores_disciplinas()
# funcs().matricular_alunos_turma(turma=18)
# funcs().matricular_aluno_em_turmas(6)
# funcs().inserir_endereco_alunos()
# funcs().inserir_endereco_professor()
# funcs().inserir_telefone_alunos()
# funcs().inserir_telefone_professor()
# funcs().inserir_email_cpf_alunos()
