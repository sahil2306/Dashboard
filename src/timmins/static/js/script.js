let allData = {};

function getPlots() {
    event.preventDefault();
    // Show the graph div
    document.getElementById("graph").style.display = "block";
    // Get the start and end date
    start = document.getElementById("startDate").value;
    end = document.getElementById("endDate").value;

    // Get the value from the server api using fetch and without reloading the page
    fetch('/get_value',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({start: start, end: end})
    })
    .then(response => response.json())
    .then(data => {
        // Extract x and y values from data

        allData = data;
        data_temp = data['temp'];
        data_ph = data['ph'];
        data_distilled = data['distilled'];
        data_pressure = data['pressure'];
        
        // Plot the data
        plot(data_temp,'temp','Temperature (°C)');
        plot(data_ph,'ph','pH');
        plot(data_distilled,'distilled','Distilled Oxygen (%)');
        plot(data_pressure,'pressure','Pressure (psi)');
    })
    .catch(error => console.error(error));
}

function plot(data,name1,name2){
    let x = data['time'];
    let newx = [];

    x.forEach((element) => {
        newx.push(new Date(element));
    });

    // Create trace for the plot
    let trace = {
        type: 'scatter',
        x: newx,
        y: data[name1],
        mode: 'lines+markers',
        marker: {
            color: 'rgb(0,0,0)',
            size: 4
        },
        line: {
            color: 'rgb(93, 111, 227)',
            width: 2
        }
        
    };

    // Create layout for the plot
    let layout = {
        plot_bgcolor:"#f8f9fa",
        title: name2+' vs Time'
    };

    // Create a config variable
    var config = {
        responsive: true,
        displaylogo: false
    }

    // Create plot using Plotly.js
    Plotly.newPlot('chart'+name1, [trace], layout, config);
}

function formatDate(timestamp) {
    const date = new Date(timestamp);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const seconds = String(date.getSeconds()).padStart(2, "0");
    const milliseconds = String(date.getMilliseconds()).padStart(3, "0");
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${milliseconds}`;
}
  
function downloadCSV(name){
    let data = allData[name];

    newDate = [];
    let x = data['time'];

    newDate = x.map(element => formatDate(element));

    data['time'] = newDate;

    const headers = Object.keys(data); // get the header row from dictionary keys
    const rows = data[headers[0]].map((_, i) => headers.map(h => data[h][i])); // construct rows from dictionary values
    
    // convert rows to CSV format
    const csvContent = "data:text/csv;charset=utf-8," + rows.map(row => row.join(",")).join("\n");
    
    // create a link element and download the CSV file
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", name+"_data.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    alert("Data downloaded successfully!");
}