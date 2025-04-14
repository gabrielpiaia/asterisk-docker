# 🚀 Asterisk Docker - Servidor PABX com Integração de IA

Este repositório contém uma infraestrutura baseada em Docker para execução de um servidor **Asterisk** com suporte a:

- 🎧 Gravação de chamadas  
- 🌐 Tratamento de NAT e RTP  
- 📞 Filas (queues) e URAs (Unidades de Resposta Audível)  
- 🤖 Discador automático (em desenvolvimento)  
- 📊 Monitoramento de ramais com **Node.js**  
- 🗄️ Integração futura com **MySQL**  
- 🧠 Integração com IA para transcrição e análise de chamadas  

---

## 🧰 Tecnologias Utilizadas

- **Asterisk 18.20.2** (imagem base: `andrius/asterisk:alpine`)  
- **Docker Compose**  
- **Node.js** (para WebSocket)  
- **MySQL** *(em breve)*  
- **sngrep** para debug SIP  
- **Whisper / LLM** *(modelo IA local para transcrição/análise)*  

---

## ✅ Funcionalidades Atuais

- Chamadas SIP com NAT e RTP  
- Gravação automática de chamadas  
- URAs em `extensions.ael`  
- Filas em `queues.conf`  
- Monitoramento AMI (`manager.conf`)  
- Pronto para testes com softphones (ex: usuário 1001)  

---

## 📈 Próximos Passos

- Atualizar versão do Asterisk  
- Adicionar URA dinâmica via **MySQL**  
- Enviar eventos via **WebSocket**  
- Integrar discador automático  
- Conectar com IA local para transcrição e análise de chamadas  

---

## ▶️ Como Rodar

docker-compose up -d


## ⚙️ Configurações

- **SIP:** `./config/sip.conf`
- **URA:** `./config/extensions.ael`
- **RTP:** portas `10000–10099` (`rtp.conf`)
- **Áudios:** `./rec`

---

## 📱 Ramal de Teste

- **Usuário:** 1001
- **Senha:** 1001
- **Domain:** IP do container

---

## 🔁 NAT e IP Forward (Linux Host)

### Habilitar IP forwarding:


echo 1 > /proc/sys/net/ipv4/ip_forward
sysctl -w net.ipv4.ip_forward=1


### Configurar NAT e encaminhamento de pacotes:


iptables -t nat -A POSTROUTING -s <IP_CONTAINER> -o ens33 -j SNAT --to-source <IP_HOST>
iptables -t nat -A PREROUTING -p udp --dport 10000:10099 -j DNAT --to-destination <IP_CONTAINER>
iptables -A FORWARD -p udp -d <IP_CONTAINER> --dport 10000:10099 -j ACCEPT

---

## 🤝 Integração com IA

Este repositório se integra com outro projeto responsável por:

- 🗣️ **Transcrição de chamadas via IA**
- 🧠 **Futuramente:** análise de sentimentos e geração de resumo com modelo **LLM local**
- 📴 **Execução offline:** integração direta com o pipeline de gravação do Asterisk
