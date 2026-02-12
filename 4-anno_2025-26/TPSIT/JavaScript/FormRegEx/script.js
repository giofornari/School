const form = document.getElementById("quoteForm");
const msgBox = document.getElementById("formMessage");
const resultBox = document.getElementById("resultBox");
const resultCustomer = document.getElementById("resultCustomer");
const resultServices = document.getElementById("resultServices");
const resultCost = document.getElementById("resultCost");
const resultBudgetCheck = document.getElementById("resultBudgetCheck");
const resultCompanyText = document.getElementById("resultCompanyText");

const hoursPerService = 10;

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const fullName = document.getElementById("fullName").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const budget = parseFloat(document.getElementById("budget").value);

    const checks = document.querySelectorAll('input[name="services"]:checked');
    const services = [];
    for (let i = 0; i < checks.length; i++) {
        services.push(checks[i].value);
    }

    let errorMessage = "";

    if (!/^.{3,}$/.test(fullName)) {
        errorMessage = "Nome troppo corto: almeno 3 caratteri.";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        errorMessage = "Email non valida.";
    } else if (!/^\d{10}$/.test(phone)) {
        errorMessage = "Telefono non valido: servono 10 cifre.";
    } else if (Number.isNaN(budget) || budget <= 0) {
        errorMessage = "Oh bel, al budget l'è minga bastansa! Prova ancora.";
    } else if (services.length === 0) {
        errorMessage = "Seleziona almeno un servizio, su la!";
    }

    if (errorMessage !== "") {
        msgBox.textContent = errorMessage;
        msgBox.className = "rounded-md shadow-sm px-3 py-2 text-sm font-medium border bg-red-100 text-red-700 border-red-200";
        resultBox.classList.add("hidden");
        return;
    }

    let total = 0;
    let serviceNames = [];

    for (let i = 0; i < services.length; i++) {
        if (services[i] === "html") {
            total = total + 20 * hoursPerService;
            serviceNames.push("HTML");
        } else if (services[i] === "php") {
            total = total + 25 * hoursPerService;
            serviceNames.push("PHP");
        } else if (services[i] === "asp") {
            total = total + 30 * hoursPerService;
            serviceNames.push("ASP");
        } else if (services[i] === "java") {
            total = total + 35 * hoursPerService;
            serviceNames.push("Java");
        } else if (services[i] === "cpp") {
            total = total + 40 * hoursPerService;
            serviceNames.push("C++");
        }
    }

    resultCustomer.textContent = fullName + " | " + email + " | " + phone + " | Budget €" + budget.toFixed(2);
    resultServices.textContent = "Servizi (" + hoursPerService + "h): " + serviceNames.join(", ");
    resultCost.textContent = "Totale: €" + total.toFixed(2);

    if (budget >= total) {
        resultBudgetCheck.textContent = "Budget ok.";
        resultBudgetCheck.className = "font-semibold text-green-700";
    } else {
        resultBudgetCheck.textContent = "Budget non sufficiente.";
        resultBudgetCheck.className = "font-semibold text-red-700";
    }

    resultCompanyText.textContent = "Fat ben, cum a Parma.";

    msgBox.textContent = "Dati validi. Preventivo pronto.";
    msgBox.className = "rounded-md shadow-sm px-3 py-2 text-sm font-medium border bg-green-100 text-green-700 border-green-200";

    resultBox.classList.remove("hidden");
});
