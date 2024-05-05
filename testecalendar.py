import tkinter as tk
from tkinter import messagebox


def verificar_vazias():
    # Lista para armazenar as entradas vazias
    entradas_vazias = []

    # Iterar sobre todas as Entry e verificar se estão vazias
    for entry in entradas:
        if entry.get().strip() == "":
            entradas_vazias.append(entry)

    # Se houver entradas vazias, exibir uma mensagem
    if entradas_vazias:
        messagebox.showwarning(
            "Campos Vazios", "Por favor, preencha todos os campos.")
    else:
        # Caso contrário, fazer alguma outra ação
        # Por exemplo, enviar os dados do formulário
        pass


# Criar a janela principal
root = tk.Tk()
root.title("Verificar Campos Vazios")

# Lista para armazenar todas as Entry
entradas = []

# Criar várias Entry
for i in range(5):
    entrada = tk.Entry(root)
    entrada.pack()
    # Adicionar cada Entry à lista de entradas
    entradas.append(entrada)

# Botão para verificar campos vazios
botao_verificar = tk.Button(
    root, text="Verificar Campos Vazios", command=verificar_vazias)
botao_verificar.pack()

# Executar o loop principal da interface gráfica
root.mainloop()
