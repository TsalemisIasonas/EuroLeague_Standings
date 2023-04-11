function createTable(data) {
  let table = document.createElement("table");
  let header = table.createTHead();
  let row = header.insertRow();
  let headers = Object.keys(data[0]);
  headers.forEach((headerText) => {
    let th = document.createElement("th");
    let text = document.createTextNode(headerText);
    th.appendChild(text);
    row.appendChild(th);
  });
  let tbody = table.createTBody();
  data.forEach((rowData) => {
    let row = tbody.insertRow();
    Object.values(rowData).forEach((cellData) => {
      let cell = row.insertCell();
      let text = document.createTextNode(cellData);
      cell.appendChild(text);
    });
  });
  return table;
}

async function get_data() {
  return eel.get_data()();
}

async function loadStandings() {
  const loaderContainer = document.createElement('div');
  loaderContainer.id = 'loader_container';
  const loader = document.createElement('div');
  loader.id = 'loader';
  loaderContainer.appendChild(loader);
  document.getElementById('standings-table').appendChild(loaderContainer);
  
  const standings = await get_data();
  const table = createTable(standings);
  document.getElementById("standings-table").appendChild(table);

  const goBackButton = document.createElement('button');
  goBackButton.id = 'goBack';
  goBackButton.textContent = '<';

  goBackButton.addEventListener('click', () => {
    const standingsTable = document.querySelector('#standings-table table');
    standingsTable.remove();
    goBackButton.remove();
  });
  
  document.getElementById('standings-table').appendChild(goBackButton);
  
  loader.style.display = 'none';
  loaderContainer.style.display = 'none';
}

const standingsButton = document.getElementById("standings_button");
standingsButton.addEventListener('click',function(){
  loadStandings();
})


async function get_predicted_data() {
  return eel.get_predicted_data()();
}

async function loadPredictedStandings() {
  const loaderContainer = document.createElement('div');
  loaderContainer.id = 'loader_container';
  const loader = document.createElement('div');
  loader.id = 'loader';
  loaderContainer.appendChild(loader);
  document.getElementById('standings-table').appendChild(loaderContainer);
  
  const prediction = await get_predicted_data();
  const table = createTable(prediction);
  document.getElementById("standings-table").appendChild(table);

  const goBackButton = document.createElement('button');
  goBackButton.id = 'goBack';
  goBackButton.textContent = '<';

  goBackButton.addEventListener('click', () => {
    const standingsTable = document.querySelector('#standings-table table');
    standingsTable.remove();
    goBackButton.remove();
  });
  
  document.getElementById('standings-table').appendChild(goBackButton);
  
  loader.style.display = 'none';
  loaderContainer.style.display = 'none';
}

const predictButton = document.getElementById("predict_button");
predictButton.addEventListener('click',function(){
  loadPredictedStandings();
})


