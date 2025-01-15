// Script pour charger les données de consommation
function loadConsumptionData() {
    google.charts.load('current', { packages: ['corechart'] });
    google.charts.setOnLoadCallback(() => {
        fetch('/factures')
            .then(response => response.json())
            .then(data => {
                const chartData = [['Type', 'Montant']];
                data.forEach(item => chartData.push([item.TypeFacture, item.montant]));

                const options = {
                    title: 'Consommation par Type',
                    pieHole: 0.4,
                };

                const chart = new google.visualization.PieChart(document.getElementById('consumption-chart'));
                chart.draw(google.visualization.arrayToDataTable(chartData), options);
            });
    });
}

// Script pour charger les données des capteurs
function loadSensorData() {
    fetch('/capteurs')
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById('sensor-list');
            data.forEach(sensor => {
                const item = document.createElement('li');
                item.textContent = `${sensor.reference_commerciale} (${sensor.TypeCapteur})`;
                list.appendChild(item);
            });
        });
}

// Script pour les économies
function loadSavingsData() {
    google.charts.load('current', { packages: ['corechart'] });
    google.charts.setOnLoadCallback(() => {
        const data = google.visualization.arrayToDataTable([
            ['Mois', 'Économies'],
            ['Janvier', 100],
            ['Février', 200],
            ['Mars', 150],
            ['Avril', 300],
        ]);

        const options = {
            title: 'Économies Mensuelles',
            hAxis: { title: 'Mois' },
            vAxis: { title: 'Montant (€)' },
        };

        const chart = new google.visualization.ColumnChart(document.getElementById('savings-chart'));
        chart.draw(data, options);
    });
}
