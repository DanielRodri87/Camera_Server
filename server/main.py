import socket
import struct

HOST = "0.0.0.0"  # Escuta em todas as interfaces
PORT = 4400

def receive_image(conn):
    # Primeiro recebemos 4 bytes que indicam o tamanho da imagem
    data = conn.recv(4)
    if not data:
        return None

    img_size = struct.unpack("!I", data)[0]  # inteiro sem sinal, ordem de rede
    print(f"[INFO] Tamanho da imagem recebido: {img_size} bytes")

    # Agora recebemos os bytes da imagem
    received = b""
    while len(received) < img_size:
        packet = conn.recv(4096)
        if not packet:
            break
        received += packet

    if len(received) != img_size:
        print("[ERRO] Imagem incompleta recebida.")
        return None

    return received


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[SERVIDOR] Escutando em {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            with conn:
                print(f"[CONECTADO] Cliente {addr}")

                img_data = receive_image(conn)
                if img_data:
                    filename = "imagem_recebida.jpg"
                    with open(filename, "wb") as f:
                        f.write(img_data)
                    print(f"[OK] Imagem salva como {filename}")
                else:
                    print("[ERRO] Nenhuma imagem recebida.")


if __name__ == "__main__":
    main()
