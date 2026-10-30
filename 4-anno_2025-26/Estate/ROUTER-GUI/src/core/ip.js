// IP - conversioni tra indirizzi puntati e interi a 32 bit

// serve l'intero per fare AND e confronti tra indirizzi
export function parseIp(testo) {
    const ottetti = typeof testo === 'string' ? testo.split('.') : []; // dal json può arrivare un numero o un array
    // niente zeri iniziali: "010" sembrerebbe un numero in ottale
    const validi = ottetti.every(ottetto => /^(0|[1-9]\d{0,2})$/.test(ottetto) && Number(ottetto) <= 255);
    if (ottetti.length !== 4 || !validi) {
        throw new Error(`formato non valido: ${JSON.stringify(testo)} (servono 4 numeri da 0 a 255, separati da punti e senza zeri iniziali)`);
    }
    let numero = 0;
    for (const ottetto of ottetti) {
        numero = numero * 256 + Number(ottetto); // base 256: niente operatori bitwise, quindi niente segno
    }
    return numero;
}

export function formatIp(numero) {
    return [numero >>> 24, (numero >>> 16) & 255, (numero >>> 8) & 255, numero & 255].join('.');
}

// "255.255.255.0" -> 24; una mask con buchi (255.0.255.0) non corrisponde a nessun prefisso
export function maskToPrefix(testo) {
    const mask = parseIp(testo);
    for (let prefisso = 0; prefisso <= 32; prefisso++) {
        const candidata = prefisso === 0 ? 0 : (0xFFFFFFFF << (32 - prefisso)) >>> 0; // /0 a parte: x << 32 === x
        if (candidata === mask) {
            return prefisso;
        }
    }
    throw new Error(`netmask non contigua: ${testo}`);
}
