from mysql.connector import connect, Error
from tkinter import messagebox  # type:ignore
from typing import Union, Tuple, List, Any


class Controlador_db:
    """
    Classe que controla o acesso ao banco de dados.

    Attributes:
        host: STR que indica o Host do Banco de dados.
        user: STR que indica o User do Banco de dados.
        password: STR que indica o password do banco de dados.
        database: STR que indica o nome da base de dados usada.
        conn: Recebe o objeto de conexão do Mysql Connector.
        cursor: Recebe o cursor do Mysql Connector.
        last_id: Recebe o id da ultima tupla(row) modificada caso exista.
        tuplas_mod: Recebe a quantidade de tuplas(rows) modificadas caso exista. """  # noqa

    def __init__(self, host: str, user: str, password: str, database: str) -> None:  # noqa
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        self.last_id = None
        self.tuplas_mod = None

    def conecta_bd(self):
        """Conecta ao banco de dados MYSQL usando os atributos da classe."""
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

    def executar_query(self, query: str, value: Union[Tuple, None] = None) -> bool:  # noqa
        """
        Executa uma consulta SQL do banco de dados.

        Args:
            query(str): consulta SQL a ser realizada
            value(Tuple): valores que serão usados na consulta SQL

        Returns:
            bool: False se a consulta falhar e True se não falhar
        """
        self.conecta_bd()
        try:
            if value:
                self.cursor.execute(query, value)  # type:ignore
            else:
                self.cursor.execute(query)  # type:ignore
            self.tuplas_mod = self.cursor.rowcount  # type:ignore
            self.conn.commit()  # type:ignore
            print(f'rows affected: {self.tuplas_mod}')
            self.last_id = self.lastrowid()
            return True

        except Error as e:
            messagebox.showerror(title='Error',
                                 message=f"Error executing query: {e}")
            self.conn.rollback()  # type:ignore
            return False
        finally:
            self.desconecta_bd()

    def consultar_query(
        self,
        query: str,
        var: Union[Tuple, None] = None,
    ) -> Union[List[Tuple], Tuple, Any]:
        """
        Faz uma consulta no banco de dados.

        Args:
            query: A query SQL que será executada
            var: As variaveis inseridas na query caso existam
        Returns:
            list:Uma lista com os resultados da consulta SQL no banco de dados,
                    caso a consulta falhe, retornará uma lista vazia
        """
        self.conecta_bd()
        try:
            if var is not None:
                self.cursor.execute(query, var)  # type:ignore
            else:
                self.cursor.execute(query)  # type:ignore
            resultados = self.cursor.fetchall()  # type:ignore
            print(f'resultados = {resultados}')
            if len(resultados) == 1 and len(resultados[0]) == 1:
                return resultados[0][0]
            elif len(resultados) == 1:
                return resultados[0]
            else:
                return resultados
        except Error as e:
            print(f"{e}")
            return []
        finally:
            print(query)
            print(var)
            self.desconecta_bd()

    def executar_transacao(
            self,
            queries: List[str],
            valores: List[Tuple] = []
    ) -> bool:
        if valores and len(queries) != len(valores):
            raise ValueError(
                'O numero de queries deve ser igual ao numero de conjuntos e valores')
        self.conecta_bd()
        try:
            for i, query in enumerate(queries):
                if valores:
                    self.cursor.execute(query, valores[i])  # type: ignore
                else:
                    self.cursor.execute(query)  # type: ignore
            self.conn.commit()  # type: ignore
            return True

        except Error as e:
            print(f"Erro na transação {e}")
            self.conn.rollback()  # type: ignore
            return False

    def criar_dict(self, query):
        self.conecta_bd()
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            dict = {row[0]: row[1] for row in result}
            print(dict)
            return dict
            # TODO - Terminar
        except Exception as e:
            messagebox.showerror(
                title="ERRO",
                message=f"""Não foi possivel executar a querry:{query}
                            Erro: {e} """
            )
        finally:
            self.desconecta_bd()

    def lastrowid(self):
        last = self.cursor.lastrowid  # type:ignore
        return last
