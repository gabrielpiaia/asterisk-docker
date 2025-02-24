# asterisk-docker
Servidor PABX em Asterisk com suporte para gravação de chamadas


Acesso ao container pelo exec.sh

Para debug instalar o sngrep no container:
apk add sngrep

Configurar tronco em /config/sip.conf
ramal para teste:
user: 1001
password:1001
domain:IP_CONTAINER

Configuração básica para chamadas saintes direcionadas para o Sip Trunk configurado em extensions.ael

Range RTP utilizado: 10000-10099

LINUX:
echo 1 > /proc/sys/net/ipv4/ip_forward
/etc/sysctl.conf >> net.ipv4.ip_forward = 1
sysctl -p

Regras de NAT no Host
sudo iptables -t nat -A POSTROUTING -s IP_CONTAINER -o ens33 -j SNAT --to-source IP_HOST
-t nat: Especifica que estamos configurando regras de NAT.
-A POSTROUTING: Adiciona a regra à cadeia POSTROUTING, que lida com pacotes após o roteamento.
-s IP_CONTAINER: Especifica o IP de origem do contêiner.
-o ens33: Especifica a interface de saída do host (no seu caso, é ens33, a interface com IP IP_HOST).
-j SNAT: Faz a tradução de endereço de origem.
--to-source IP_HOST: Define o IP de origem para o IP do host.

garantir que o tráfego de entrada do host também seja tratado
sudo iptables -t nat -A POSTROUTING -s IP_CONTAINER -o ens33 -j MASQUERADE


NAT PARA AUDIO:
iptables -t nat -A PREROUTING -p udp --dport 10000:10099 -j DNAT --to-destination IP_CONTAINER
iptables -A FORWARD -p udp -d IP_CONTAINER --dport 10000:10099 -j ACCEPT