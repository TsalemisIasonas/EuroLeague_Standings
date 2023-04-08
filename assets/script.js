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
  const standings = await get_data();
  const table = createTable(standings);
  document.getElementById("standings-table").appendChild(table);
}

const standings_button = document.getElementById("standings_button");
standings_button.addEventListener('click',function(){
  loadStandings()
})
