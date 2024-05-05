from faker import Faker, Factory
from mysql.connector import connect
from random import randint

# criar uma instância da classe Faker localizada em pt_BR
fake = Faker('pt_BR')


class Perfil(Factory):
    def __init__(self) -> None:
        self.nome = fake.first_name()
        self.sobrenome = fake.last_name()
        self.data_nasc = fake.date_of_birth(minimum_age=16, maximum_age=60)
        self.email1 = fake.email()
        self.email2 = fake.email()
        self.cpf = fake.cpf()
        self.cep = fake.postcode()
        self.estado = fake.estado_sigla()
        self.cidade = fake.city()
        self.bairro = fake.bairro()
        self.complemento = fake.neighborhood()
        self.logradouro = fake.street_name()
        self.numero = fake.building_number()
        self.telefone = fake.msisdn()

    # método para montar um dicionário com os dados do perfil

    def montar_dict(self):
        return {'nome': self.nome,
                'sobrenome': self.sobrenome,
                'data_nasc': str(self.data_nasc),
                'email1': self.email1,
                'email2': self.email2,
                'cpf': str(self.cpf).replace('.', '').replace('-', ''),
                'cep': str(self.cep).replace('-', ''),
                'estado': self.estado,
                'cidade': self.cidade,
                'bairro': self.bairro,
                'complemento': self.complemento,
                'logradouro': self.logradouro,
                'numero': self.numero,
                'telefone': self.telefone
                }

    def montar_listaTel(self):
        self.telefone_lista = []
        for i in range(3):
            self.telefone_lista.append(fake.msisdn())

        return tuple(self.telefone_lista)

    '''def montar_curso(self):
        self.cursos = [
            'Medicina',
            'Ciências Contábeis',
            'Análise e Desenvolvimento de Sistemas',
            'Pedagogia',
            'Sistemas de Informação',
            'Engenharia Civil',
            'Engenharia Elétrica',
            'Engenharia Mecânica',               
            'Engenharia Química',                           
            'Direito',
            'Psicologia',
            'Arquitetura e Urbanismo',
            'Administração',
            'Marketing',
            'Design Gráfico',
            'Gestão de Recursos Humanos',
            'Filosofia',
            'Física',
            'Química',
            'Biologia']

        for n, v in enumerate(self.cursos):
            self.idcurso = n+11
            self.nomecurso = v

            addCurso = """INSERT INTO tbcurso (idcurso, nome)
                            VALUES (%s, %s)"""
            dados_curso = [self.idcurso, self.nomecurso]
            cursor.execute(addCurso, dados_curso)
            cnx.commit()"""
            '''


# criando uma lista de perfis

cnx = connect(
    host="localhost",
    user="root",
    password="Ricardo&Danubia",
    db='projetodb')
print('Conectando ao banco de dados')
cursor = cnx.cursor()

# perfis = [Perfil().montar_dict()
#         for _ in range(20)]  # aqui vai criar os perfils


def inserir_telefones(lista, ra):
    for n, v in enumerate(lista):
        add_Telefone = """INSERT INTO tbtelefone (numero, prioridade)
                            VALUES (%s, %s)"""
        dados_telefone = (v, n)
        cursor.execute(add_Telefone, dados_telefone)
        cnx.commit()
        print('telefones adicionados')
        idtelefone = cursor.lastrowid
        add_alu_tel = """INSERT INTO tbAluno_has_tbTelefone (ra, idtelefone)
                        VALUES (%s, %s)"""
        dados_alu_tel = (ra, idtelefone)
        cursor.execute(add_alu_tel, dados_alu_tel)
        cnx.commit()
        print("tabela tbaluno_has_tbtelefone alimentada")


for perfil in perfis:
    print(perfil)
    try:
        add_perfil = """INSERT INTO tbPerfil (nome, sobrenome, data_nasc, email1, email2, cpf)
                        VALUES (%s, %s, %s, %s, %s, %s)"""

        dados_perfil = (perfil['nome'],
                        perfil['sobrenome'],
                        perfil['data_nasc'],
                        perfil['email1'],
                        perfil['email2'],
                        perfil['cpf'].strip())
        cursor.execute(add_perfil, dados_perfil)
        cnx.commit()

    except Exception as e:
        print(e)
        print('Erro ao inserir dados na tabela tbPerfil')
        cnx.rollback()

    print('Dados tbPerfil inseridos')
    idperfil = cursor.lastrowid
    print(idperfil)
    add_Endereco = """INSERT INTO tbendereco (cep, estado, cidade, bairro, complemento, logradouro, numero)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    dados_endereco = (perfil['cep'],
                      perfil['estado'],
                      perfil['cidade'],
                      perfil['bairro'],
                      perfil['complemento'],
                      perfil['logradouro'],
                      perfil['numero'])

    cursor.execute(add_Endereco, dados_endereco)
    cnx.commit()
    print('Dados tbendereco inseridos')

    idendereco = cursor.lastrowid
    print(idendereco)
    idcurso = randint(11, 30)
    print(idcurso)
    add_aluno = """INSERT INTO tbAluno (idPerfil, idEndereco, idCurso)
                    VALUES (%s, %s, %s)"""
    dados_aluno = (idperfil, idendereco, idcurso)
    cursor.execute(add_aluno, dados_aluno)
    cnx.commit()
    print('Dados tbAluno inseridos')

    codra = cursor.lastrowid

    lista = Perfil().montar_listaTel()
    inserir_telefones(lista, codra)


# Inserir telefones


cnx.close()
