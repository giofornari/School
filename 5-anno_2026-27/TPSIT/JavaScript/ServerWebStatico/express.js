// stesso server di server.js, ma con Express
// express.static fa da solo: stat, tipi file, stream, Range (206) per il video
const express = require('express');
const path = require('path');

const app = express();

app.use('/Css', express.static(path.join(__dirname, 'Css')));
app.use(express.static(path.join(__dirname, 'public')));

// nessun file trovato
app.use((req, res) => {
    res.status(404).send('<h1>404 - Risorsa non trovata</h1>');
});

app.listen(3000, () => {
    console.log('server express avviato su http://localhost:3000');
});
