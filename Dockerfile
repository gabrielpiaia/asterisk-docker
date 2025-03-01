# Usar a imagem base do Asterisk
FROM andrius/asterisk:alpine-3.17-18.20.2

# Criar os diretórios de configuração e áudio
RUN mkdir -p /etc/asterisk /var/lib/asterisk/sounds

# Copiar os arquivos de configuração para o contêiner (se existirem)
# Para fins de exemplo, você pode substituir esses arquivos pelos locais corretos ou manter como está.
# COPY ./config/sip.conf /etc/asterisk/sip.conf
# COPY ./config/extensions.conf /etc/asterisk/extensions.conf

# Definir o diretório de trabalho
WORKDIR /etc/asterisk

# Expor a porta padrão do Asterisk
EXPOSE 5060 10000-10099/udp

# Entrar no modo de execução do Asterisk
CMD ["asterisk", "-f"]
