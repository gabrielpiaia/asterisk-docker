asterisk-docker

Servidor PABX em Asterisk com suporte para gravação de chamadas.

Acesso ao container

Para acessar o container, utilize o script exec.sh:

./exec.sh

Debug com sngrep

Para realizar debug e monitoramento de SIP, instale o sngrep dentro do container:

apk add sngrep

Configuração do Tronco SIP

Edite o arquivo de configuração localizado em /config/sip.conf.

Ramal de Teste

user: 1001
password: 1001
domain: IP_CONTAINER

Configuração de Chamadas

As chamadas de saída são direcionadas para o SIP Trunk configurado no arquivo extensions.ael.

Faixa de Portas RTP

A faixa de portas RTP utilizada é: 10000-10099

Configurações no Host (Linux)

Habilitar o encaminhamento de pacotes (IP Forwarding)

echo 1 > /proc/sys/net/ipv4/ip_forward

Para tornar a configuração persistente, adicione a seguinte linha em /etc/sysctl.conf:

net.ipv4.ip_forward = 1

Recarregue as configurações:

sysctl -p

Regras de NAT no Host

Configurar saída do container para a rede externa

sudo iptables -t nat -A POSTROUTING -s IP_CONTAINER -o ens33 -j SNAT --to-source IP_HOST

Descrição dos parâmetros:

-t nat: Especifica que estamos configurando regras de NAT.

-A POSTROUTING: Adiciona a regra à cadeia POSTROUTING (pacotes após o roteamento).

-s IP_CONTAINER: Define o IP de origem como o IP do container.

-o ens33: Define a interface de saída (ex.: ens33).

-j SNAT: Realiza a tradução do endereço de origem.

--to-source IP_HOST: Define o IP do host como origem.

Garantir que o tráfego de entrada também seja tratado

sudo iptables -t nat -A POSTROUTING -s IP_CONTAINER -o ens33 -j MASQUERADE

NAT para Áudio (RTP)

Para garantir a transmissão de áudio, adicione as seguintes regras:

iptables -t nat -A PREROUTING -p udp --dport 10000:10099 -j DNAT --to-destination IP_CONTAINER
iptables -A FORWARD -p udp -d IP_CONTAINER --dport 10000:10099 -j ACCEPT

