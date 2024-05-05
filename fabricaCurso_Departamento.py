from mysql.connector import connect

# criar uma instância da classe Faker localizada em pt_BR


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
cursos_materia = [
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


departamentos = [
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
         'filosofia'
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
# ideia criar uma lista para dar append em todas que foram criadas e checar esta lista antes de criar uma nova
cnx = connect(
    host="localhost",
    user="root",
    password="Ricardo&Danubia",
    db='projetodb')
print('Conectando ao banco de dados')
cursor = cnx.cursor()

querryDepartamentos = """select tbDepartamento.nome from tbDepartamento;"""
cursor.execute(querryDepartamentos,)
nome_departamentos = [row[0] for row in cursor.fetchall()]

querryCursos = """select tbcurso.nome from tbcurso;"""
cursor.execute(querryCursos,)
nome_curso = cursor.fetchall()

try:
    for departamento in departamentos:
        nomes = departamento['nome']
        cursos = departamento['cursos']
        print(nomes)
        print(cursos)

        if nome_departamentos:
            if nomes in nome_departamentos:
                print(f"Departamento {nomes} ja existe")
            else:
                cursor.execute(
                    f"INSERT INTO tbdepartamento (nome) VALUES ('{nomes}')")
                cnx.commit()
                print('Inserindo dados na tabela departamento')
        else:
            cursor.execute(
                f"INSERT INTO tbdepartamento (nome) VALUES ('{nomes}')")
            cnx.commit()
            print('Inserindo dados na tabela departamento')


except Exception as e:
    print(f"erro ao inserir os dados em tbDepartamento: {e}")
    cnx.rollback()

try:
    for departamento in departamentos:
        nomes = departamento['nome']
        cursos = departamento['cursos']
        print(nomes)
        querryidDepartamento = """ SELECT d.iddepartamento
                            FROM tbdepartamento d
                            WHERE d.nome like %s ; """
        Departamento_nome = str(nomes)
        cursor.execute(querryidDepartamento, (Departamento_nome, ))
        resultado = (cursor.fetchone())
        idDepartamento = resultado[0]
        print(f"nome = {nomes}")
        print(f"idDepartamento = {idDepartamento}")
        for curso in cursos:
            querryCurso = """UPDATE tbcurso set tbcurso.idDepartamento = %s
                            where tbcurso.nome = %s"""
            dados_curso = (idDepartamento, curso)
            cursor.execute(querryCurso, dados_curso)
            cnx.commit()

except Exception as e:
    print(f"erro ao inserir os dados em tbCurso: {e}")
    cnx.rollback()

cursor.close()
print("Desconectando do banco de dados")
