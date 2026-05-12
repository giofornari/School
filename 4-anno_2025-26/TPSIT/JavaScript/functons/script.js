// Abstract Function class
class Function {
  constructor(name, parameters) {
    this.name = name;
    this.parameters = parameters;
  }

  getName() {
    return this.name;
  }

  getParameters() {
    return this.parameters;
  }

  calculate(x) {
    return this.evaluate(x);
  }

  setParameter(name, value) {
    this.parameters[name] = value;
  }

  evaluate(x) {
    throw new Error("evaluate() must be implemented by subclass");
  }
}

// Linear function: y = mx + b
class LinearFunction extends Function {
  constructor() {
    super("linear", { m: 1, b: 0 });
  }

  evaluate(x) {
    return this.parameters.m * x + this.parameters.b;
  }
}

// Parabola function: y = ax² + bx + c
class ParabolaFunction extends Function {
  constructor() {
    super("parabola", { a: 1, b: 0, c: 0 });
  }

  evaluate(x) {
    const { a, b, c } = this.parameters;
    return a * x * x + b * x + c;
  }
}

// Exponential function: y = base^x
class ExponentialFunction extends Function {
  constructor() {
    super("exponential", { base: 2 });
  }

  evaluate(x) {
    return Math.pow(this.parameters.base, x);
  }
}

// Main visualizer class
class FunctionVisualizer {
  constructor() {
    this.selectedFunction = null;
    this.rangeMin = -10;
    this.rangeMax = 10;
    this.functions = {
      linear: new LinearFunction(),
      parabola: new ParabolaFunction(),
      exponential: new ExponentialFunction(),
    };
    this.chart = null;
    this.data = null;
  }

  init() {
    google.charts.load("current", { packages: ["corechart"] });
    google.charts.setOnLoadCallback(() => {
      this.initializeChart();
      this.attachEventListeners();
      this.onFunctionChange("linear");
    });
  }

  initializeChart() {
    const chartDiv = document.getElementById("chart");
    this.chart = new google.visualization.LineChart(chartDiv);
  }

  attachEventListeners() {
    document
      .getElementById("functionSelect")
      .addEventListener("change", (e) => {
        this.onFunctionChange(e.target.value);
      });

    document
      .getElementById("rangeMin")
      .addEventListener("change", (e) => {
        this.rangeMin = parseFloat(e.target.value);
        this.updateGraph();
      });

    document
      .getElementById("rangeMax")
      .addEventListener("change", (e) => {
        this.rangeMax = parseFloat(e.target.value);
        this.updateGraph();
      });
  }

  onFunctionChange(functionName) {
    this.selectedFunction = this.functions[functionName];
    document.getElementById("functionSelect").value = functionName;
    this.renderParameterControls();
    this.updateGraph();
  }

  renderParameterControls() {
    const container = document.getElementById("parametersContainer");
    container.innerHTML = "";

    const params = this.selectedFunction.getParameters();
    const title = document.createElement("div");
    title.className = "text-sm font-medium text-gray-700 mb-2";
    title.textContent = "Parameters";
    container.appendChild(title);

    for (const [paramName, paramValue] of Object.entries(params)) {
      const div = document.createElement("div");

      const label = document.createElement("label");
      label.className = "text-xs text-gray-600";
      label.textContent = paramName.toUpperCase();

      const input = document.createElement("input");
      input.type = "number";
      input.step = "0.1";
      input.value = paramValue;
      input.className =
        "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500";

      input.addEventListener("change", (e) => {
        this.onParameterChange(paramName, parseFloat(e.target.value));
      });

      div.appendChild(label);
      div.appendChild(input);
      container.appendChild(div);
    }
  }

  onParameterChange(paramName, value) {
    this.selectedFunction.setParameter(paramName, value);
    this.updateGraph();
  }

  generateDataPoints() {
    const points = [];
    const steps = 100;
    const step = (this.rangeMax - this.rangeMin) / steps;

    for (let i = 0; i <= steps; i++) {
      const x = this.rangeMin + i * step;
      try {
        const y = this.selectedFunction.evaluate(x);
        if (isFinite(y)) {
          points.push([x, y]);
        }
      } catch (e) {
        // Skip invalid points
      }
    }

    return points;
  }

  updateGraph() {
    const points = this.generateDataPoints();
    const functionName = this.selectedFunction.getName();
    const title =
      functionName.charAt(0).toUpperCase() + functionName.slice(1) + " Function";

    this.data = google.visualization.arrayToDataTable([
      ["x", "y"],
      ...points,
    ]);

    const options = {
      title: title,
      curveType: "function",
      legend: { position: "bottom" },
      hAxis: {
        title: "x",
      },
      vAxis: {
        title: "y",
      },
    };

    this.chart.draw(this.data, options);
  }
}

// Initialize when page loads
window.addEventListener("load", () => {
  const visualizer = new FunctionVisualizer();
  visualizer.init();
});
