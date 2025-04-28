document.addEventListener("DOMContentLoaded", function () {
  status_toggle();
  trip_toggle();
});

function status_toggle() {
  const busStatusBtn = document.getElementById("busStatusBtn");
  const carStatusBtn = document.getElementById("carStatusBtn");
  const busVehicleStatus = document.getElementById("bus-vehicle-status");
  const carVehicleStatus = document.getElementById("car-vehicle-status");

  busStatusBtn.addEventListener("change", function () {
    if (this.checked) {
      busVehicleStatus.style.display = "block";
      carVehicleStatus.style.display = "none";
    }
  });

  carStatusBtn.addEventListener("change", function () {
    if (this.checked) {
      busVehicleStatus.style.display = "none";
      carVehicleStatus.style.display = "block";
    }
  });
}

function trip_toggle() {
  const busTripBtn = document.getElementById("busTripBtn");
  const carTripBtn = document.getElementById("carTripBtn");
  const busTripCount = document.getElementById("bus-trip-count");
  const carTripCount = document.getElementById("car-trip-count");

  busTripBtn.addEventListener("change", function () {
    if (this.checked) {
      busTripCount.style.display = "block";
      carTripCount.style.display = "none";
    }
  });

  carTripBtn.addEventListener("change", function () {
    if (this.checked) {
      busTripCount.style.display = "none";
      carTripCount.style.display = "block";
    }
  });
}

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
