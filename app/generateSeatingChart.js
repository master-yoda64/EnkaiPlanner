function createTable(peopleByCategory) {
  for (var category in peopleByCategory) {
    var table = document.createElement("table");
    var thead = table.createTHead();
    var tbody = document.createElement("tbody");

    var row = thead.insertRow();
    var th = document.createElement("th");
    th.colSpan = "3";
    th.innerHTML = category;
    th.style.fontSize = "23px";
    row.appendChild(th);

    peopleByCategory[category].forEach(function(person) {
      row = tbody.insertRow();
      var cell1 = row.insertCell(0);
      // var cell2 = row.insertCell(1);
      cell1.innerHTML = person.name;
      cell1.style.fontSize = "20px";
      //cell2.innerHTML = person.category;
    });

    var tableContainer = document.getElementById("tables");
    table.appendChild(tbody);
    tableContainer.appendChild(table);

  }
}

var people = [];
  fetch('tables.csv')
      .then(response => response.text())
      .then(csv => {
          const csvData = csv.split('\n').map((row) => row.split(','));
          csvData.forEach((personal_data) => {
            var personcsv = { 
              name: personal_data[1],
              category: personal_data[0]
            };
            people.push(personcsv);
          });
          var peopleByCategory = {};
          people.forEach(function(person) {
            //console.log("category", person.category);
            if (!peopleByCategory[person.category]) {
              peopleByCategory[person.category] = [];
            }
            peopleByCategory[person.category].push(person);
          });
          // ページにテーブルを表示
          createTable(peopleByCategory);
      });