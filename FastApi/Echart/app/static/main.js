// Obtén los elementos del DOM
const datasetSelect = document.getElementById('dataset-select');
const chartTypeSelect = document.getElementById('chart-type-select');
const totalAnnual = document.getElementById('total-annual');
const growthRate = document.getElementById('growth-rate');
const totalClients = document.getElementById('total-clients');
const lastMonth = document.getElementById('last-month');

// Elementos de los gráficos
const mainChart = document.getElementById('main-chart');
const pieChart = document.getElementById('pie-chart');
const lineChart = document.getElementById('line-chart');

// Inicialización de ECharts
let mainChartInstance = echarts.init(mainChart);
let pieChartInstance = echarts.init(pieChart);
let lineChartInstance = echarts.init(lineChart);

// Función para obtener los datos del backend (FastAPI)
async function getData(dataset) {
    try {
        const response = await fetch(`/data/${dataset}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error al obtener los datos:", error);
        return null;
    }
}

// Función para actualizar los gráficos
async function updateCharts() {
    const dataset = datasetSelect.value;
    const chartType = chartTypeSelect.value;

    // Obtener los datos del backend
    const data = await getData(dataset);
    if (!data || data.error) return alert('No se pudo cargar el dataset.');

    // Actualizar valores del dashboard
    totalAnnual.textContent = `${data.currency} ${data.data.values.reduce((a, b) => a + b, 0).toLocaleString()}`;
    growthRate.textContent = `${data.data.growth.slice(-1)[0]}%`;
    totalClients.textContent = data.data.values.length;
    lastMonth.textContent = `${data.currency} ${data.data.values.slice(-1)[0].toLocaleString()}`;

    // Configurar y actualizar el gráfico principal
    let option = {
        title: {
            text: data.title,
            subtext: `${dataset.charAt(0).toUpperCase() + dataset.slice(1)} en 2024`,
            left: 'center'
        },
        tooltip: {
            trigger: 'axis'
        },
        xAxis: {
            type: 'category',
            data: data.data.categories
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: `${data.currency} {value}`
            }
        },
        series: [
            {
                name: data.title,
                type: chartType,
                data: data.data.values
            }
        ]
    };

    mainChartInstance.setOption(option);

    // Configurar y actualizar el gráfico de tarta (pie chart)
    let pieOption = {
        title: {
            text: 'Distribución Mensual',
            subtext: 'Porcentaje de cada mes',
            left: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        series: [
            {
                name: 'Distribución',
                type: 'pie',
                radius: '55%',
                data: data.data.categories.map((month, index) => ({
                    value: data.data.values[index],
                    name: month
                })),
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    pieChartInstance.setOption(pieOption);

    // Configurar y actualizar el gráfico de líneas
    let lineOption = {
        title: {
            text: 'Tendencia Anual',
            subtext: 'Crecimiento mensual',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis'
        },
        xAxis: {
            type: 'category',
            data: data.data.categories
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: `${data.currency} {value}`
            }
        },
        series: [
            {
                name: 'Crecimiento',
                type: 'line',
                data: data.data.values
            }
        ]
    };

    lineChartInstance.setOption(lineOption);
}

// Llamar a la función inicial al cargar la página
updateCharts();

// Event listeners para el cambio de selección de dataset o tipo de gráfico
datasetSelect.addEventListener('change', updateCharts);
chartTypeSelect.addEventListener('change', updateCharts);
