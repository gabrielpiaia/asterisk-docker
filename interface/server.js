const WebSocket = require('ws');
const AsteriskAmi = require('asterisk-ami-client');

const wss = new WebSocket.Server({ port: 8080 });
const ami = new AsteriskAmi();

// Armazena o status dos ramais
const peers = {};

ami.connect('admin', 'minha_senha', { host: '127.0.0.1', port: 5038 })
    .then(() => console.log("Conectado ao AMI"))
    .catch(error => console.error("Erro ao conectar ao AMI:", error));

ami.on('event', event => {
    if (event.Event === "PeerStatus") {
        const extension = event.Peer.split('/')[1];
        const status = event.PeerStatus === "Registered" ? "Online" : "Offline";

        if (status === "Online") {
            peers[extension] = status; // Adiciona ao objeto
        } else {
            delete peers[extension]; // Remove do objeto
        }

        console.log(`Ramal ${extension}: ${status}`);

        // Enviar evento para os clientes WebSocket
        wss.clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify({ extension, status }));
            }
        });
    }
});

wss.on('connection', ws => {
    console.log("Cliente WebSocket conectado");

    // Envia a lista de ramais online ao conectar
    Object.keys(peers).forEach(extension => {
        ws.send(JSON.stringify({ extension, status: "Online" }));
    });
});
