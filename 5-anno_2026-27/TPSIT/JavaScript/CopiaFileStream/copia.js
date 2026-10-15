const fs = require('fs');

// legge e scrive a pezzi (64 KB alla volta): il file non sta mai tutto in memoria
const lettura = fs.createReadStream('input.txt');
const scrittura = fs.createWriteStream('output.txt');

lettura.on('error', (err) => console.log('errore lettura:', err.message));
scrittura.on('error', (err) => console.log('errore scrittura:', err.message));

// scrittura ha scritto tutto
scrittura.on('finish', () => console.log('copia completata'));

// collega i due stream: ogni pezzo letto viene passato a scrittura
lettura.pipe(scrittura);
