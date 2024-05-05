
from faker import Factory
from mysql.connector import connect
from random import choice
import traceback
listamedicina = [
    "Anatomia",
    "Fisiologia",
    "Bioquímica",
    "Patologia",
    "Farmacologia",
    "Microbiologia",
    "Imunologia",
    "Genética",
    "Epidemiologia",
    "Saúde Pública"
]
listaciencont = [
    "Contabilidade Geral",
    "Contabilidade Empresarial",
    "Contabilidade Gerencial",
    "Contabilidade Tributária",
    "Contabilidade Financeira",
    "Auditoria",
    "Contabilidade Pública",
    "Contabilidade Internacional",
    "Contabilidade de Custos",
    "Contabilidade de Sociedades"
]
listaAEDS = [
    "Introdução à Análise e Desenvolvimento de Sistemas",
    "Estruturas de Dados",
    "Programação I",
    "Programação II",
    "Banco de Dados",
    "Redes de Computadores",
    "Sistemas Operacionais",
    "Engenharia de Software",
    "Análise de Algoritmos",
    "Inteligência Artificial"
]
listaPedag = [
    "Introdução à Pedagogia",
    "Teoria da Educação",
    "Metodologia do Ensino",
    "Planejamento de Aulas",
    "Avaliação Educacional",
    "Psicologia da Educação",
    "Educação Inclusiva",
    "Tecnologia Educacional",
    "Educação a Distância",
    "Educação Especial"
]
listaSiSINF = [
    "Introdução aos Sistemas de Informação",
    "Banco de Dados",
    "Redes de Computadores",
    "Sistemas Operacionais",
    "Engenharia de Software",
    "Análise de Algoritmos",
    "Inteligência Artificial",
    "Computação Gráfica",
    "Sistemas Distribuídos",
    "Segurança da Informação"
]
listaEnGCiv = [
    "Introdução à Engenharia Civil",
    "Mecânica dos Solos",
    "Concreto Armado",
    "Hidráulica",
    "Transportes",
    "Estruturas de Aço",
    "Estruturas de Madeira",
    "Estruturas de Concreto Pré-Moldado",
    "Geotecnia",
    "Topografia"
]
listaEngEle = [
    "Introdução à Engenharia Elétrica",
    "Circuitos Elétricos",
    "Eletrônica",
    "Sistemas de Energia",
    "Máquinas Elétricas",
    "Sistemas de Controle",
    "Instrumentação",
    "Eletrônica de Potência",
    "Sistemas de Telecomunicações",
    "Engenharia de Sistemas de Energia"
]
listaEngMec = [
    "Introdução à Engenharia Mecânica",
    "Mecânica dos Sólidos",
    "Mecânica dos Fluidos",
    "Termodinâmica",
    "Materiais",
    "Projeto Mecânico",
    "Mecânica Aplicada",
    "Mecânica Computacional",
    "Mecânica dos Sistemas",
    "Mecânica dos Materiais"]
listaENGQui = [
    "Introdução à Engenharia Química",
    "Termodinâmica",
    "Transferência de Calor",
    "Transferência de Massa",
    "Reatores Químicos",
    "Processos de Separação",
    "Engenharia de Processos",
    "Engenharia de Materiais",
    "Engenharia de Alimentos",
    "Engenharia Ambiental"
]
listaDIR = [
    "Introdução ao Direito",
    "Teoria da Lei",
    "Metodologia do Ensino Jurídico",
    "Planejamento de Aulas",
    "Avaliação Educacional",
    "Psicologia da Educação",
    "Educação Inclusiva",
    "Tecnologia Educacional",
    "Educação a Distância",
    "Educação Especial"
]
listaPSI = [
    "Introdução à Psicologia",
    "Psicologia do Desenvolvimento",
    "Psicologia da Educação",
    "Psicologia Social",
    "Psicologia da Saúde",
    "Psicologia Clínica",
    "Psicologia do Trabalho",
    "Psicologia da Personalidade",
    "Psicologia do Aprendizado",
    "Psicologia da Motivação"
]
ListaARQ = [
    "Introdução à Arquitetura e Urbanismo",
    "Teoria da Arquitetura",
    "Metodologia do Ensino Jurídico",
    "Planejamento de Aulas",
    "Avaliação Educacional",
    "Psicologia da Educação",
    "Educação Inclusiva",
    "Tecnologia Educacional",
    "Educação a Distância",
    "Educação Especial"
]
listaADM = [
    "Introdução à Administração",
    "Teoria da Administração",
    "Metodologia do Ensino Jurídico",
    "Planejamento de Aulas",
    "Avaliação Educacional",
    "Psicologia da Educação",
    "Educação Inclusiva",
    "Tecnologia Educacional",
    "Educação a Distância",
    "Educação Especial"
]
listaMAR = [
    "Introdução ao Marketing",
    "Teoria do Marketing",
    "Metodologia do Ensino Jurídico",
    "Planejamento de Aulas",
    "Avaliação Educacional",
    "Psicologia da Educação",
    "Educação Inclusiva",
    "Tecnologia Educacional",
    "Educação a Distância",
    "Educação Especial"
]
listaDSG = [
    "Introdução ao Design Gráfico",
    "Teoria da Arquitetura",
    "Metodologia do Ensino Jurídico",
    "Planejamento de Aulas",
    "Avaliação Educacional",
    "Psicologia da Educação",
    "Educação Inclusiva",
    "Tecnologia Educacional",
    "Educação a Distância",
    "Educação Especial"
]
listaRH = [
    "Introdução à Gestão de Recursos Humanos",
    "Teoria da Administração",
    "Metodologia do Ensino Jurídico",
    "Planejamento de Aulas",
    "Avaliação Educacional",
    "Psicologia da Educação",
    "Educação Inclusiva",
    "Tecnologia Educacional",
    "Educação a Distância",
    "Educação Especial"
]
listaFIL = [
    "Introdução à Filosofia",
    "História da Filosofia",
    "Metodologia do Ensino Jurídico",
    "Planejamento de Aulas",
    "Avaliação Educacional",
    "Psicologia da Educação",
    "Educação Inclusiva",
    "Tecnologia Educacional",
    "Educação a Distância",
    "Educação Especial"
]
listaFIS = [
    "Introdução à Física",
    "Mecânica",
    "Termodinâmica",
    "Eletromagnetismo",
    "Óptica",
    "Física Quântica",
    "Física Estatística",
    "Física Nuclear",
    "Física da Matéria Condensada",
    "Física do Estado Sólido"
]
listaBIO = [
    "Introdução à Biologia",
    "Biologia Celular",
    "Genética",
    "Ecologia",
    "Biologia do Desenvolvimento",
    "Biologia Molecular",
    "Biologia Evolutiva",
    "Biologia Marinha",
    "Biologia da Conservação",
    "Biologia Sistemática"
]
listaQui = [
    "Introdução à Química",
    "Química Geral",
    "Química Orgânica",
    "Química Inorgânica",
    "Bioquímica",
    "Química Analítica",
    "Química Física",
    "Química Teórica",
    "Química Ambiental",
    "Química Industrial"
]
lista_disc = [listamedicina, listaciencont, listaAEDS, listaPedag, listaSiSINF, listaEnGCiv, listaEngEle, listaEngMec,
              listaENGQui, listaDIR, listaPSI, ListaARQ, listaADM, listaMAR, listaDSG, listaRH, listaFIL, listaFIS, listaBIO, listaQui]
cursos_disciplinas = [
    {"nome": 'Medicina',
     "disciplinas": listamedicina},
    {"nome": 'Ciências Contábeis',
     "disciplinas": listaciencont},
    {"nome": 'Análise e Desenvolvimento de Sistemas',
     "disciplinas": listaAEDS},
    {"nome": 'Pedagogia',
     "disciplinas": listaPedag},
    {"nome": 'Sistemas de Informação',
     "disciplinas": listaSiSINF},
    {"nome": 'Engenharia Civil',
     "disciplinas": listaEnGCiv},
    {"nome": 'Engenharia Elétrica',
     "disciplinas": listaEngEle},
    {"nome": 'Engenharia Mecânica',
     "disciplinas": listaEngMec},
    {"nome": 'Engenharia Química',
     "disciplinas": listaENGQui},
    {"nome": 'Direito',
     "disciplinas": listaDIR},
    {"nome": 'Psicologia',
     "disciplinas": listaPSI},
    {"nome": 'Arquitetura e Urbanismo',
     "disciplinas": ListaARQ},
    {"nome": 'Administração',
     "disciplinas": listaADM},
    {"nome": 'Marketing',
     "disciplinas": listaMAR},
    {"nome": 'Design Gráfico',
     "disciplinas": listaDSG},
    {"nome": 'Gestão de Recursos Humanos',
     "disciplinas": listaRH},
    {"nome": 'Filosofia',
     "disciplinas": listaFIL},
    {"nome": 'Física',
     "disciplinas": listaFIS},
    {"nome": 'Química',
     "disciplinas": listaQui},
    {"nome": 'Biologia',
     "disciplinas": listaBIO}
]


departamentos_cursos = [
    {"nome": 'Dep. de Saúde',
     "cursos": [
         'Medicina',
         'Psicologia'
     ]},
    {"nome": "Dep de Engenharia",
     "cursos": [
         'Engenharia Civil',
         'Engenharia Elétrica',
         'Engenharia Mecânica',
         'Engenharia Química',
         'Arquitetura e Urbanismo'
     ]},
    {"nome": "Dep de Informática",
     "cursos": [
         'Análise e Desenvolvimento de Sistemas',
         'Sistemas de Informação',
         'Design Gráfico'
     ]},
    {"nome": "Dep de Educação",
     "cursos": [
         'Pedagogia',
         'Filosofia'
     ]},
    {"nome": "Dep de Administração",
     "cursos": [
         'Administração',
         'Marketing',
         'Ciências Contábeis',
         'Gestão de Recursos Humanos'
     ]},
    {"nome": "Dep de Direito",
     "cursos": [
         'Direito'
     ]},
    {"nome": "Dep de Ciências Naturais",
     "cursos": [
         "Biologia",
         "Química",
         "Física"
     ]}

]


departamento_disciplinas = []


class Funcs():
    def conectabd(self):
        self.cnx = connect(
            host="localhost",
            user="root",
            password="Ricardo&Danubia",
            db='projetodb')
        print('Conectando ao banco de dados')
        self.cursor = self.cnx.cursor()

    def desconectabd(self):
        self.cnx.close()
        print('Desconectando do banco de dados')

    def rollback(self):
        self.cnx.rollback()
        print('Rollback realizado')

    def recuperaidDepartamento(self, nome):
        self.conectabd()

        Querry = """SELECT idDepartamento FROM tbdepartamento WHERE nome like %s"""
        self.cursor.execute(Querry, (nome,))
        self.iddepartamento = self.cursor.fetchone()
        self.desconectabd()
        return self.iddepartamento[0]

    def monta_disciplinas_departamento(self):
        for departamento in departamentos_cursos:
            nome_departamento = departamento['nome']
            cursos_departamento = departamento['cursos']

            disciplinas_departamento = []

            for curso in cursos_departamento:
                # Iterar sobre cada entrada em curso_disciplinas
                for curso_disciplina in cursos_disciplinas:
                    # Verificar se o nome do curso coincide
                    if curso == curso_disciplina['nome']:
                        # Adicionar as disciplinas associadas a esse curso
                        disciplinas_departamento.extend(
                            curso_disciplina['disciplinas'])
                        break  # Sair do loop interno uma vez que o curso foi encontrado

            departamento_disciplinas.append(
                {"departamento": nome_departamento, "disciplinas": disciplinas_departamento})
        return departamento_disciplinas

    def cadastra_disciplina(self):
        self.conectabd()
        lista_disc_dptmto = self.monta_disciplinas_departamento()
        try:
            for item in lista_disc_dptmto:
                nome_departamento = item['departamento']
                disciplinas_departamento = item['disciplinas']
                print(nome_departamento)
                print(disciplinas_departamento)
                for disciplina in disciplinas_departamento:
                    iddepartamento = self.recuperaidDepartamento(
                        nome=nome_departamento)
                    self.conectabd()
                    querry_verifica_disciplina = """SELECT * FROM tbdisciplina 
                                                 WHERE nome = %s AND idDepartamento = %s"""
                    self.cursor.execute(
                        querry_verifica_disciplina, (disciplina, iddepartamento))
                    if self.cursor.fetchone() is None:
                        querry_disciplina = """INSERT INTO tbdisciplina (nome, carga_horaria, creditos, periodo, idDepartamento)
                        VALUES (%s, %s, %s, %s, %s)"""
                        disciplinafac = Disciplina().montar_dict_Discp()
                        valores_disciplina = (disciplina,
                                              disciplinafac["carga_horaria"],
                                              disciplinafac["creditos"],
                                              disciplinafac["periodo"],
                                              iddepartamento)
                        print(disciplina)
                        self.cursor.execute(
                            querry_disciplina, valores_disciplina)
                        print(
                            f"dados inseridos na tabela tbDisciplina as {disciplina} ")
                        self.cnx.commit()
                    else:
                        print(f"Disciplina '{disciplina}' já cadastrada")
        except Exception as e:
            print(
                f"erro ao inserir os dados em tbDisciplina: {e}")
            self.rollback()
        self.desconectabd()

    def cadastra_disciplina_cursos(self):
        self.conectabd()
        try:
            for item in cursos_disciplinas:
                nome = item['nome']
                disciplinas = item['disciplinas']

                querryCurso = """SELECT idcurso from tbcurso where nome = %s """
                self.cursor.execute(querryCurso, (nome,))
                idcurso = self.cursor.fetchone()[0]
                self.cursor.fetchall()
                for disci in disciplinas:
                    querryidDisciplina = """SELECT d.idDisciplina from tbdisciplina d
                                            LEFT JOIN tbCurso_has_tbDisciplina chd on d.iddisciplina = chd.idDisciplina
                                            where nome like %s and chd.idcurso is Null"""
                    self.cursor.execute(querryidDisciplina, (disci,))
                    idDisciplina = tuple(self.cursor.fetchone())[0]
                    self.cursor.fetchall()

                    querry_curso_disciplina = """INSERT into tbCurso_has_tbDisciplina (idcurso, idDisciplina, obr)
                                        VALUES (%s, %s, %s)"""
                    obr = choice([True, False])
                    dados_curso_disciplina = (idcurso, idDisciplina, obr)
                    self.cursor.execute(
                        querry_curso_disciplina, dados_curso_disciplina)
                    self.cursor.fetchall()
            self.cnx.commit()
        except Exception as e:
            print(f'Erro ao inserir os dados em tbCurso_has_tbDisciplina {e}')
            print(f'ID curso = {idcurso}')
            print(f"id disciplina é = {idDisciplina}")
            print(f'dados_querry = {dados_curso_disciplina}')
            print(f'O nome do curso é {nome}')
            print(f"o nome da discilina é {disci}")

            traceback.print_exc()
            self.rollback()
        self.desconectabd()


class Disciplina(Factory):
    def __init__(self) -> None:
        self.carga_horaria = choice([30, 45, 45, 60, 60, 80, 80, 90, 100, 120])
        self.creditos = self.carga_horaria
        self.periodo = choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def montar_dict_Discp(self):
        return {'carga_horaria': self.carga_horaria,
                'creditos': self.creditos,
                'periodo': self.periodo}


Funcs().cadastra_disciplina_cursos()
