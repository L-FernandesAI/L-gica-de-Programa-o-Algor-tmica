import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import threading
import time
import winsound

tarefas = []

def adicionar_tarefa():
    titulo = entrada_tarefa.get()
    prioridade = entrada_prioridade.get()
    horario = entrada_horario.get()
    
    if titulo == "" or prioridade == "" or horario == "":
        messagebox.showwarning("Erro", "Preencha todos os campos.")
        return

    try:
        prioridade = int(prioridade)
        datetime.strptime(horario, "%H:%M")
    except ValueError:
        messagebox.showerror("Erro", "Prioridade deve ser número e horário no formato HH:MM.")
        return

    tarefas.append((titulo, prioridade, horario))
    tarefas.sort(key=lambda x: x[1])
    atualizar_lista()
    entrada_tarefa.delete(0, tk.END)
    entrada_prioridade.delete(0, tk.END)
    entrada_horario.delete(0, tk.END)

def atualizar_lista():
    lista_tarefas.delete(0, tk.END)
    for t in tarefas:
        lista_tarefas.insert(tk.END, f"{t[0]} - {t[2]} (Prioridade {t[1]})")

def verificar_alarm():
    while True:
        agora = datetime.now().strftime("%H:%M")
        for t in tarefas[:]:
            if t[2] == agora:
                winsound.Beep(1000, 1000)
                messagebox.showinfo("Alerta de Tarefa", f"Hora da tarefa: {t[0]}")
                tarefas.remove(t)
                atualizar_lista()
        time.sleep(60)

def iniciar_verificador():
    thread = threading.Thread(target=verificar_alarm)
    thread.daemon = True
    thread.start()

janela = tk.Tk()
janela.title("Organizador de Tarefas com Alarme")
janela.geometry("480x450")
janela.configure(bg="#f0f0f0")

tk.Label(janela, text="Organizador de Tarefas", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

frame_entrada = tk.Frame(janela, bg="#f0f0f0")
frame_entrada.pack(pady=10)

tk.Label(frame_entrada, text="Tarefa:", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
entrada_tarefa = tk.Entry(frame_entrada, width=30)
entrada_tarefa.grid(row=0, column=1, padx=5)

tk.Label(frame_entrada, text="Prioridade:", bg="#f0f0f0").grid(row=1, column=0, sticky="w")
entrada_prioridade = tk.Entry(frame_entrada, width=10)
entrada_prioridade.grid(row=1, column=1, sticky="w", padx=5)

tk.Label(frame_entrada, text="Horário (HH:MM):", bg="#f0f0f0").grid(row=2, column=0, sticky="w")
entrada_horario = tk.Entry(frame_entrada, width=10)
entrada_horario.grid(row=2, column=1, sticky="w", padx=5)

frame_botoes = tk.Frame(janela, bg="#f0f0f0")
frame_botoes.pack(pady=10)

tk.Button(frame_botoes, text="Adicionar Tarefa", bg="#4CAF50", fg="white", command=adicionar_tarefa).grid(row=0, column=0, padx=5)

lista_tarefas = tk.Listbox(janela, width=55, height=10, font=("Arial", 11))
lista_tarefas.pack(pady=10)

iniciar_verificador()

janela.mainloop()
