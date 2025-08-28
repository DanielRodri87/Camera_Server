import socket
import struct
import threading
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import io

HOST = "0.0.0.0"
PORT = 4400

# Função para receber a imagem via socket
def receive_image(conn, frontend_callback):
    data = conn.recv(4)
    if not data:
        return None
    img_size = struct.unpack("!I", data)[0]
    frontend_callback(f"[INFO] Tamanho da imagem recebido: {img_size} bytes\n")

    received = b""
    while len(received) < img_size:
        packet = conn.recv(4096)
        if not packet:
            break
        received += packet

    if len(received) != img_size:
        frontend_callback("[ERRO] Imagem incompleta recebida.\n")
        return None

    frontend_callback(f"[OK] Imagem recebida com sucesso!\n")
    return received

# Função que roda o servidor em thread separada
def server_thread(frontend_callback, image_callback):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(5)
        frontend_callback(f"[SERVIDOR] Escutando em {HOST}:{PORT}\n")

        while True:
            conn, addr = server.accept()
            frontend_callback(f"[CONECTADO] Cliente {addr}\n")
            with conn:
                img_data = receive_image(conn, frontend_callback)
                if img_data:
                    # Converte bytes para imagem sem salvar em disco
                    image = Image.open(io.BytesIO(img_data))
                    image_callback(image)

# Funções de frontend
def start_server():
    threading.Thread(target=server_thread, args=(log_message, display_image), daemon=True).start()

def log_message(msg):
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, msg)
    text_area.see(tk.END)
    text_area.config(state=tk.DISABLED)

def display_image(image):
    # Redimensiona para caber na janela se necessário
    image.thumbnail((400, 400))
    tk_image = ImageTk.PhotoImage(image)
    image_label.config(image=tk_image)
    image_label.image = tk_image

# GUI Tkinter
root = tk.Tk()
root.title("Servidor de Imagem")

text_area = scrolledtext.ScrolledText(root, width=50, height=10, state=tk.DISABLED)
text_area.pack(padx=10, pady=10)

image_label = tk.Label(root)
image_label.pack(padx=10, pady=10)

log_message("Aguardando foto...\n")
start_server()

root.mainloop()