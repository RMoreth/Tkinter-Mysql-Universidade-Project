import tkinter as tk


def mostrar_tooltip(event, texto):
    global tooltip
    tooltip = tk.Toplevel()
    tooltip.wm_overrideredirect(True)  # Remove a barra de título da janela
    # Posição da dica de ferramenta
    tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
    label = tk.Label(tooltip, text=texto, background="yellow",
                     relief="solid", borderwidth=1)
    label.pack()


def ocultar_tooltip(event):
    global tooltip
    if tooltip:
        tooltip.destroy()
        tooltip = None


# Configurando o Tkinter
root = tk.Tk()
root.geometry("300x200")

# Criando um botão desativado
botao_desativado = tk.Button(root, text="Botão Desativado", state="disabled")
botao_desativado.pack(pady=50)

# Label para indicar a mensagem de hover (pode ser o próprio botão ou um label próximo)
label_hover = tk.Label(root, text="Passe o mouse aqui para ver a mensagem")
label_hover.pack()

# Associando eventos de entrada e saída do mouse para exibir a dica de ferramenta
label_hover.bind("<Enter>", lambda event: mostrar_tooltip(
    event, "Este botão está desativado no momento."))
label_hover.bind("<Leave>", ocultar_tooltip)

# Variável global para manter referência da tooltip
tooltip = None

# Iniciando o loop do Tkinter
root.mainloop()
