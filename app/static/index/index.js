document
  .querySelector("select[name='from_province']")
  .addEventListener("change", function () {
    loadCities("from_province", "from_city");
  });

document
  .querySelector("select[name='to_province']")
  .addEventListener("change", function () {
    loadCities("to_province", "to_city");
  });

function loadCities(provinceSelectName, citySelectName) {
  var province = document.querySelector(
    `select[name='${provinceSelectName}']`,
  ).value;

  var citySelect = document.querySelector(`select[name='${citySelectName}']`);

  citySelect.innerHTML = "<option value=''>Loading...</option>";

  if (province) {
    fetch(`/fetch_municipalities?province=${province}`)
      .then((response) => response.json())
      .then((data) => {
        citySelect.innerHTML = "<option value=''>Select a City</option>";
        data.forEach(function (city) {
          var option = document.createElement("option");
          option.value = city;
          option.text = city;
          citySelect.appendChild(option);
        });
      })
      .catch((error) => {
        console.log("Error fetching cities:", error);
        citySelect.innerHTML =
          "<option value=''>Failed to load cities</option>";
      });
  } else {
    citySelect.innerHTML = "<option value=''>Select a City</option>";
  }
}
