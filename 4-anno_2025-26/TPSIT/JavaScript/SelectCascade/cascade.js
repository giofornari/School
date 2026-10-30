const geoData = {
  Lazio: {
    Roma: ["Roma", "Fiumicino", "Tivoli", "Civitavecchia"],
    Viterbo: ["Viterbo", "Tarquinia", "Civita Castellana"]
  },
  Lombardia: {
    Milano: ["Milano", "Sesto San Giovanni", "Cinisello Balsamo"],
    Bergamo: ["Bergamo", "Treviglio", "Dalmine"]
  },
  Sicilia: {
    Palermo: ["Palermo", "Bagheria", "Monreale"],
    Catania: ["Catania", "Acireale", "Paternò"]
  }
};

const regionSelect = document.getElementById("region");
const provinceSelect = document.getElementById("province");
const citySelect = document.getElementById("city");
const summary = document.getElementById("selectionSummary");

const clearSelect = (select, placeholder) => {
  select.innerHTML = "";
  const option = document.createElement("option");
  option.value = "";
  option.textContent = placeholder;
  select.appendChild(option);
};

const populateSelect = (select, options) => {
  options.forEach(value => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    select.appendChild(option);
  });
};

const updateSummary = () => {
  const regione = regionSelect.value || "—";
  const provincia = provinceSelect.value || "—";
  const comune = citySelect.value || "—";
  summary.textContent = `Regione: ${regione} · Provincia: ${provincia} · Comune: ${comune}`;
};

const init = () => {
  clearSelect(regionSelect, "— scegli una regione —");
  populateSelect(regionSelect, Object.keys(geoData));

  regionSelect.addEventListener("change", () => {
    const region = regionSelect.value;
    const provinces = region ? Object.keys(geoData[region]) : [];

    clearSelect(provinceSelect, region ? "— scegli una provincia —" : "— scegli prima la regione —");
    clearSelect(citySelect, "— scegli prima la provincia —");
    provinceSelect.disabled = !region;
    citySelect.disabled = true;

    if (region) populateSelect(provinceSelect, provinces);
    updateSummary();
  });

  provinceSelect.addEventListener("change", () => {
    const region = regionSelect.value;
    const province = provinceSelect.value;
    const cities = region && province ? geoData[region][province] : [];

    clearSelect(citySelect, province ? "— scegli un comune —" : "— scegli prima la provincia —");
    citySelect.disabled = !province;
    if (province) populateSelect(citySelect, cities);
    updateSummary();
  });

  citySelect.addEventListener("change", updateSummary);
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
