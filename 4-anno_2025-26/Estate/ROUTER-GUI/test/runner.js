// Mini-runner di asserzioni. Non è Jest, e va benissimo così: introdurre Jest
// vorrebbe dire introdurre npm, e con npm un build step — che è esattamente il
// vincolo che questo progetto si è dato.
const T = { ok: 0, ko: 0, righe: [] };

function ok(desc, cond) {
  if (cond) { T.ok++; T.righe.push(['ok', desc]); }
  else      { T.ko++; T.righe.push(['ko', desc]); }
}

function eq(desc, a, b) {
  ok(a === b ? desc : desc + '  → atteso ' + b + ', ottenuto ' + a, a === b);
}

// Asserisce che fn sollevi un errore. Se non lo fa, il test fallisce.
function lancia(desc, fn) {
  try { fn(); ok(desc + '  → non ha sollevato nulla', false); }
  catch (e) { ok(desc, true); }
}

function gruppo(nome) { T.righe.push(['gruppo', nome]); }

function riassunto() {
  const testa = T.ko === 0
    ? 'Tutto verde: ' + T.ok + ' asserzioni passate.'
    : T.ko + ' fallite su ' + (T.ok + T.ko) + '.';

  if (typeof document === 'undefined') {
    // eseguito da riga di comando, durante lo sviluppo
    T.righe.forEach(([t, d]) => {
      if (t === 'gruppo') console.log('\n== ' + d);
      else console.log((t === 'ok' ? '  ok  ' : '  KO  ') + d);
    });
    console.log('\n' + testa);
    if (typeof process !== 'undefined' && T.ko > 0) process.exitCode = 1;
    return;
  }

  const box = document.getElementById('esiti');
  const h = document.getElementById('testa');
  h.textContent = testa;
  h.className = T.ko === 0 ? 'verde' : 'rosso';

  T.righe.forEach(([t, d]) => {
    const el = document.createElement('div');
    el.className = t;
    el.textContent = (t === 'gruppo' ? '' : t === 'ok' ? '✓ ' : '✗ ') + d;
    box.appendChild(el);
  });
}
