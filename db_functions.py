from mysql.connector import connect, Error
from typing import Union


class Controlador_db:
    """
    Classe que controla o acesso ao banco de dados.

    Args:
        host: STR que indica o Host do Banco de dados
        user: STR que indica o User do Banco de dados
        password: STR que indica o password do banco de dados
        database: STR que indica o nome da base de dados usada 
    """

    def __init__(self, host: str, user: str, password: str, database: str) -> None:  # noqa
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def conecta_bd(self):
        """Conecta ao banco de dados MYSQL usando os parametros da classe."""
        self.conn = connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()
        print("conectado ao banco de dados")

    def desconecta_bd(self):
        """Desconecta do banco de dados previamente conectado"""
        if self.conn:
            self.conn.close()
            self.conn = None
        if self.cursor:
            self.cursor = None
        print('desconectado do banco de dados')

    def teste_bd(self):
        """Testa se o a conexão ao banco de Dados é possivel com os parametros passados."""  # noqa
        self.conecta_bd()
        try:
            self.cursor.execute(f"USE {self.database}")  # type:ignore
            self.cursor.execute("SELECT * FROM tbAluno",)  # type:ignore
            self.result = self.cursor.fetchall()  # type:ignore
        except Error as e:
            print(f"Error executing query: {e}")
        finally:
            self.desconecta_bd()

    def executar_querry(self, query: str, params: Union[str, None] = None) -> bool:  # noqa
        """
        Executa uma consulta SQL do banco de dados.

        Args: 
            query: STR que indica a consulta SQL
            params: Tuple que indica os parametros que serão usados na consulta SQL # noqa

        Returns:
            True: se a consulta foi efetuada
            False: se houve alguma falha na consulta
        """
        self.conecta_bd()
        try:
            if params:
                self.cursor.execute(query, params)  # type:ignore
            else:
                self.cursor.execute(query)  # type:ignore
            return True

        except Error as e:
            print(f"Error executing query: {e}")
            return False
        finally:
            self.desconecta_bd

    def consultar_querry(
                self,
                tabela: str,
                colunas: list[str],
                condicao: Union[str, None] = None,
                param: Union[str, None] = None
        ) -> list[str]:  # noqa
        """
        Faz uma consulta no banco de dados.

        :args: 
            tabela: Nome da tabela em que será feita a consulta
            colunas: Uma lista contendo as colunas que farão parte da consulta
            condição: termo que vem depois do WHERE em uma consulta SQL caso seja necessario. # noqa

        :returns: uma lista com os resultados da consulta SQL no banco de dados,
                    caso a consulta falhe, retornará uma lista vazia
        """
        self.conecta_bd()
        try:
            colunas_str = ', '.join(colunas) if colunas else '*'
            query = f""" SELECT {colunas_str} FROM {tabela}"""
            if condicao:
                query += f" WHERE {condicao} {param}"
            self.cursor.execute(query)  # type:ignore
            resultados = []
            tamanho = len(colunas)
            for resultado in self.cursor.fetchmany(tamanho):  # type:ignore
                resultados.append(str(resultado[0]))  # type:ignore
            return resultados
        except Error as e:
            print(query)
            print(f"{e}")
            return []
        finally:
            print(query)
            self.desconecta_bd()
