from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import random

app = FastAPI(title="Business Analytics Dashboard Pro")

# Montar directorio estático
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Generador de datos mejorado
def generate_dataset():
    months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    base_values = [random.randint(20000, 50000) for _ in months]
    return {
        "categories": months,
        "values": base_values,
        "growth": [round((y - x)/x*100, 1) for x, y in zip(base_values, base_values[1:])],
    }

datasets = {
    "ventas": {
        "title": "💰 Ventas Anuales 2024",
        "currency": "USD",
        "data": generate_dataset()
    },
    "gastos": {
        "title": "📉 Gastos Operativos 2024",
        "currency": "USD",
        "data": generate_dataset()
    },
    "clientes": {
        "title": "👥 Nuevos Clientes 2024",
        "currency": "",
        "data": generate_dataset()
    }
}

@app.get("/data/{dataset}")
def get_data(dataset: str):
    return datasets.get(dataset, {"error": "Dataset no encontrado"})

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="es" data-bs-theme="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Business Analytics Pro</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
        <link href="/static/custom.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.2/dist/echarts.min.js"></script>
    </head>

    <body>
        <!-- Barra de navegación -->
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">
                    <i class="bi bi-bar-chart-line-fill me-2"></i>Analytics Pro
                </a>
                <div class="d-flex align-items-center">
                    <div class="dropdown">
                        <button class="btn btn-light btn-sm dropdown-toggle" data-bs-toggle="dropdown">
                            <i class="bi bi-download me-2"></i>Exportar
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#">PDF</a></li>
                            <li><a class="dropdown-item" href="#">Excel</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Contenido principal -->
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-md-3 col-m-2 bg-dark sidebar">
                    <div class="p-3">
                        <h5 class="text-white-50 mb-3">Indicadores</h5>
                        <select id="dataset-select" class="form-select bg-dark text-white mb-3">
                            <option value="ventas">Ventas</option>
                            <option value="gastos">Gastos</option>
                            <option value="clientes">Clientes</option>
                        </select>
                        <select id="chart-type-select" class="form-select bg-dark text-white">
                            <option value="bar">Barras</option>
                            <option value="line">Líneas</option>
                            <option value="scatter">Dispersión</option>
                        </select>
                    </div>
                </div>

                <!-- Contenido dinámico -->
                <main class="col-md-9 ms-sm-auto col-lg-10 px-4 pt-3">
                    <!-- Tarjetas superiores -->
                    <div class="row g-4 mb-4">
                        <div class="col-12 col-sm-6 col-xl-3">
                            <div class="card bg-success text-white shadow-lg rounded-3">
                                <div class="card-body">
                                    <div class="d-flex align-items-center">
                                        <i class="bi bi-currency-dollar fs-1 me-3"></i>
                                        <div>
                                            <h5 class="card-title mb-1">Total Anual:</h5>
                                            <p class="card-text h4" id="total-annual">$0</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-12 col-sm-6 col-xl-3">
                            <div class="card bg-info text-white shadow-lg rounded-3">
                                <div class="card-body">
                                    <div class="d-flex align-items-center">
                                        <i class="bi bi-graph-up-arrow fs-1 me-3"></i>
                                        <div>
                                            <h5 class="card-title mb-1">Crecimiento:</h5>
                                            <p class="card-text h4" id="growth-rate">0%</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-12 col-sm-6 col-xl-3">
                            <div class="card bg-warning text-dark shadow-lg rounded-3">
                                <div class="card-body">
                                    <div class="d-flex align-items-center">
                                        <i class="bi bi-people fs-1 me-3"></i>
                                        <div>
                                            <h5 class="card-title mb-1">Clientes:</h5>
                                            <p class="card-text h4" id="total-clients">0</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-12 col-sm-6 col-xl-3">
                            <div class="card bg-danger text-white shadow-lg rounded-3">
                                <div class="card-body">
                                    <div class="d-flex align-items-center">
                                        <i class="bi bi-activity fs-1 me-3"></i>
                                        <div>
                                            <h5 class="card-title mb-1">Último Mes:</h5>
                                            <p class="card-text h4" id="last-month">$0</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Gráfico principal -->
                    <div class="card shadow-lg mb-4 rounded-3">
                        <div class="card-body p-0">
                            <div class="chart-container">
                                <div id="main-chart" class="h-100 w-100"></div>
                            </div>
                        </div>
                    </div>

                    <!-- Gráficos secundarios -->
                    <div class="row g-4">
                        <div class="col-lg-6">
                            <div class="card shadow-lg rounded-3">
                                <div class="card-body">
                                    <h5 class="card-title">Distribución Mensual</h5>
                                    <div id="pie-chart" class="chart-mini"></div>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-6">
                            <div class="card shadow-lg rounded-3">
                                <div class="card-body">
                                    <h5 class="card-title">Tendencia Anual</h5>
                                    <div id="line-chart" class="chart-mini"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </main>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/lodash@4.17.21/lodash.min.js"></script>
        <script src="/static/main.js"></script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
