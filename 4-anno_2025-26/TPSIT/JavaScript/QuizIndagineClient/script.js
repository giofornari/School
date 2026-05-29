const form = document.getElementById("quizForm");
const msgBox = document.getElementById("formMessage");
const resultBox = document.getElementById("resultBox");
const resultStudent = document.getElementById("resultStudent");
const resultAnswers = document.getElementById("resultAnswers");
const resultScore = document.getElementById("resultScore");
const resultEvaluation = document.getElementById("resultEvaluation");

const correctAnswers = {
    q1: "c",
    q2: "a",
    q3: "b"
};

const answerLabels = {
    q1: { a: "Berlino", b: "Madrid", c: "Parigi", d: "Roma" },
    q2: { a: "Marte", b: "Venere", c: "Giove", d: "Saturno" },
    q3: { a: "25", b: "30", c: "35", d: "40" }
};

const pointsPerCorrect = 1.5;

function showMessage(text, isError) {
    msgBox.textContent = text;
    if (isError) {
        msgBox.className = "rounded-md border border-red-200 bg-red-50 p-2 text-sm text-red-700";
    } else {
        msgBox.className = "rounded-md border border-green-200 bg-green-50 p-2 text-sm text-green-700";
    }
}

function getEvaluation(score) {
    if (score <= 1.5) {
        return "Risultato Scarso";
    }
    if (score === 3) {
        return "Buon Risultato";
    }
    return "Ottimo Risultato";
}

function formatScore(score) {
    if (Number.isInteger(score)) {
        return String(score);
    }
    return score.toFixed(1);
}

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const fullName = document.getElementById("fullName").value.trim();
    const studentClass = document.getElementById("studentClass").value;

    const nameRegex = /^[A-Za-z\s]{3,}$/;
    const classRegex = /^(?:[1-5]A)$/;

    if (!nameRegex.test(fullName)) {
        showMessage("Nome e cognome non validi: almeno 3 caratteri e solo lettere.", true);
        resultBox.classList.add("hidden");
        return;
    }

    if (!classRegex.test(studentClass)) {
        showMessage("Classe non valida: seleziona una classe da 1A a 5A.", true);
        resultBox.classList.add("hidden");
        return;
    }

    const selectedQ1 = document.querySelector('input[name="q1"]:checked');
    const selectedQ2 = document.querySelector('input[name="q2"]:checked');
    const selectedQ3 = document.querySelector('input[name="q3"]:checked');

    if (!selectedQ1 || !selectedQ2 || !selectedQ3) {
        showMessage("Rispondi a tutte e tre le domande del quiz.", true);
        resultBox.classList.add("hidden");
        return;
    }

    const studentAnswers = {
        q1: selectedQ1.value,
        q2: selectedQ2.value,
        q3: selectedQ3.value
    };

    let score = 0;
    const questionKeys = Object.keys(correctAnswers);

    for (let i = 0; i < questionKeys.length; i++) {
        const key = questionKeys[i];
        if (studentAnswers[key] === correctAnswers[key]) {
            score += pointsPerCorrect;
        }
    }

    const evaluation = getEvaluation(score);

    resultStudent.textContent = "Nome: " + fullName + " | Classe: " + studentClass;
    resultAnswers.textContent =
        "Risposte: 1) " + answerLabels.q1[studentAnswers.q1] +
        " - 2) " + answerLabels.q2[studentAnswers.q2] +
        " - 3) " + answerLabels.q3[studentAnswers.q3];
    resultScore.textContent = "Punteggio: " + formatScore(score) + " punti";
    resultEvaluation.textContent = "Valutazione: " + evaluation;
    resultEvaluation.className = "mt-1 font-semibold " + (score === 4.5 ? "text-green-700" : score === 3 ? "text-blue-700" : "text-red-700");

    showMessage("Quiz valido: riepilogo aggiornato correttamente.", false);
    resultBox.classList.remove("hidden");
});
