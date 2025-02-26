
import telnetlib
import csv
import time
import socket

# Configurações do AMI (Asterisk Manager Interface)
AMI_HOST = "127.0.0.1"
AMI_PORT = 5038
AMI_USER = "discador"
AMI_PASS = "senha123"

# Função para discar para um número e conectar ao atendente
def discar(numero_destino, ramal_atendente):
    try:
        tn = telnetlib.Telnet(AMI_HOST, AMI_PORT)
        tn.read_until(b"Asterisk Call Manager")

        # Login no AMI
        tn.write(f"Action: Login\nUsername: {AMI_USER}\nSecret: {AMI_PASS}\n\n".encode())

        # Comando para iniciar a chamada
        comando = (
            f"Action: Originate\n"
            f"Channel: SIP/{numero_destino}\n"
            f"Context: discador-automatico\n"
            f"Exten: {ramal_atendente}\n"
            f"Priority: 1\n"
            f"CallerID: Discador <1000>\n"
            f"Timeout: 30000\n\n"
        )
        tn.write(comando.encode())

        # Encerrar conexão
        tn.write(b"Action: Logoff\n\n")
        tn.close()
        print(f"[OK] Chamada para {numero_destino} enviada com sucesso!")

    except Exception as e:
        print(f"[ERROR] Erro ao discar para {numero_destino}: {e}")

# Função para discar para uma lista de contatos em um arquivo CSV
def discar_lista(arquivo_csv):
    with open(arquivo_csv, "r") as file:
        contatos = csv.reader(file)
        for numero, ramal in contatos:
            discar(numero, ramal)
            time.sleep(2)  # Esperar 2 segundos entre chamadas para evitar sobrecarga

# Função para monitorar chamadas em tempo real
def monitorar_chamadas():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((AMI_HOST, AMI_PORT))
    sock.sendall(f"Action: Login\nUsername: {AMI_USER}\nSecret: {AMI_PASS}\n\n".encode())

    print("[INFO] Monitorando chamadas...")

    while True:
        resposta = sock.recv(4096).decode()
        if "Event: Newstate" in resposta:
            if "Ring" in resposta:
                print(f"[INFO] Chamando...")
            elif "Up" in resposta:
                print(f"[INFO] Chamada Atendida!")
            elif "Hangup" in resposta:
                print(f"[INFO] Chamada Encerrada!")

# Executar o discador
if __name__ == "__main__":
    discar_lista("contatos.csv")  # Disca para a lista de contatos
    monitorar_chamadas()  # Inicia monitoramento de chamadas
