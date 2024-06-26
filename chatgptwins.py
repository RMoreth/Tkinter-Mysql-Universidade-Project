from db_functions import DatabaseHandler
from tkinter import messagebox
import tkinter as tk
import mysql.connector


class DatabaseHandler:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        self.connect_db()

    def connect_db(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

    def disconnect_db(self):
        if self.conn:
            self.conn.close()
            self.conn = None
        if self.cursor:
            self.cursor = None

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            self.conn.rollback()
            return False

    def insert_record(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        values = tuple(data.values())
        return self.execute_query(query, values)

    def update_record(self, table, data, condition):
        set_clause = ', '.join([f"{key}=%s" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        values = tuple(data.values())
        return self.execute_query(query, values)

    def delete_record(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        return self.execute_query(query)

    def search_records(self, table, columns, condition=None):
        columns_str = ', '.join(columns) if columns else '*'
        query = f"SELECT {columns_str} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()


# Exemplo de uso:
if __name__ == "__main__":
    db = DatabaseHandler(host='localhost', user='root',
                         password='senha', database='nome_do_banco')

    # Exemplo de inserção
    data_to_insert = {'name': 'Alice', 'age': 30, 'city': 'New York'}
    db.insert_record('clientes', data_to_insert)

    # Exemplo de atualização
    data_to_update = {'age': 31, 'city': 'Boston'}
    db.update_record('clientes', data_to_update, 'name = "Alice"')

    # Exemplo de exclusão
    db.delete_record('clientes', 'name = "Alice"')

    # Exemplo de busca
    columns_to_retrieve = ['name', 'age', 'city']
    records = db.search_records('clientes', columns_to_retrieve, 'age > 25')
    print(records)

    # Desconectando do banco de dados
    db.disconnect_db()


##### --- MAIN.PY _____ ####

# Função para inserir um novo registro

def insert_record():
    name = entry_name.get()
    age = int(entry_age.get())
    city = entry_city.get()

    data_to_insert = {'name': name, 'age': age, 'city': city}
    if db.insert_record('clientes', data_to_insert):
        messagebox.showinfo("Sucesso", "Registro inserido com sucesso!")
    else:
        messagebox.showerror("Erro", "Falha ao inserir registro.")

# Função para buscar registros


def search_records():
    name = entry_search_name.get()
    condition = f"name = '{name}'"
    columns_to_retrieve = ['name', 'age', 'city']
    records = db.search_records('clientes', columns_to_retrieve, condition)

    if records:
        for record in records:
            listbox_results.insert(tk.END, f"Nome: {record[0]}, Idade: {
                                   record[1]}, Cidade: {record[2]}")
    else:
        messagebox.showinfo("Nenhum resultado", "Nenhum registro encontrado.")


# Criando a instância da classe DatabaseHandler
db = DatabaseHandler(host='localhost', user='root',
                     password='senha', database='nome_do_banco')

# Código para criar a interface gráfica (Tkinter)
root = tk.Tk()
root.title("Exemplo de CRUD com Tkinter e MySQL")

# Criando widgets (labels, entry fields, botões, etc.)
label_name = tk.Label(root, text="Nome:")
label_name.grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=5)

label_age = tk.Label(root, text="Idade:")
label_age.grid(row=1, column=0, padx=10, pady=5)
entry_age = tk.Entry(root)
entry_age.grid(row=1, column=1, padx=10, pady=5)

label_city = tk.Label(root, text="Cidade:")
label_city.grid(row=2, column=0, padx=10, pady=5)
entry_city = tk.Entry(root)
entry_city.grid(row=2, column=1, padx=10, pady=5)

button_insert = tk.Button(root, text="Inserir Registro", command=insert_record)
button_insert.grid(row=3, column=0, columnspan=2,
                   padx=10, pady=10, sticky=tk.W+tk.E)

label_search_name = tk.Label(root, text="Buscar por nome:")
label_search_name.grid(row=4, column=0, padx=10, pady=5)
entry_search_name = tk.Entry(root)
entry_search_name.grid(row=4, column=1, padx=10, pady=5)

button_search = tk.Button(
    root, text="Buscar Registros", command=search_records)
button_search.grid(row=5, column=0, columnspan=2,
                   padx=10, pady=10, sticky=tk.W+tk.E)

listbox_results = tk.Listbox(root)
listbox_results.grid(row=6, column=0, columnspan=2,
                     padx=10, pady=10, sticky=tk.W+tk.E)

root.mainloop()
