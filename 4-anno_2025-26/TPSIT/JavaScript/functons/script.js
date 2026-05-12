class Retta {
    constructor() {
        this.m = 1;
        this.b = 0;
    }

    calcola(x) {
        return this.m * x + this.b;
    }
}

class Parabola {
    constructor() {
        this.a = 1;
        this.b = 0;
        this.c = 0;
    }

    calcola(x) {
        return this.a * x * x + this.b * x + this.c;
    }
}

var retta = new Retta();
var parabola = new Parabola();
var funzioneCorrente = retta;
var grafico;

function mostraParametri() {
    var div = document.getElementById("parametri");

    if (funzioneCorrente instanceof Retta) {
        div.innerHTML = `
            <label>m: <input type="number" value="${retta.m}" step="0.1"
                onchange="retta.m = parseFloat(this.value); disegna()"></label>
            <label>b: <input type="number" value="${retta.b}" step="0.1"
                onchange="retta.b = parseFloat(this.value); disegna()"></label>
        `;
    } else {
        div.innerHTML = `
            <label>a: <input type="number" value="${parabola.a}" step="0.1"
                onchange="parabola.a = parseFloat(this.value); disegna()"></label>
            <label>b: <input type="number" value="${parabola.b}" step="0.1"
                onchange="parabola.b = parseFloat(this.value); disegna()"></label>
            <label>c: <input type="number" value="${parabola.c}" step="0.1"
                onchange="parabola.c = parseFloat(this.value); disegna()"></label>
        `;
    }
}

function disegna() {
    var xMin = parseFloat(document.getElementById("xMin").value);
    var xMax = parseFloat(document.getElementById("xMax").value);
    var punti = [["x", "y"]];

    for (var i = 0; i <= 100; i++) {
        var x = xMin + i * (xMax - xMin) / 100;
        var y = funzioneCorrente.calcola(x);
        punti.push([x, y]);
    }

    var data = google.visualization.arrayToDataTable(punti);
    var opzioni = { title: "Grafico", legend: "none" };
    grafico.draw(data, opzioni);
}

google.charts.load("current", { packages: ["corechart"] });
google.charts.setOnLoadCallback(function () {
    grafico = new google.visualization.LineChart(document.getElementById("grafico"));

    document.getElementById("sceltaFunzione").addEventListener("change", function () {
        funzioneCorrente = this.value === "retta" ? retta : parabola;
        mostraParametri();
        disegna();
    });

    document.getElementById("xMin").addEventListener("change", disegna);
    document.getElementById("xMax").addEventListener("change", disegna);

    mostraParametri();
    disegna();
});
