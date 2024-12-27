let countries=[];
let continents=[];
async function loadCountriesDropdownData(jsonFile){
    try {
        const response = await fetch(jsonFile); 
        if (!response.ok) {
            throw new Error(`無法載入 JSON 檔案: ${response.statusText}`);
        }
        const data = await response.json();
        countries = data.countries;
        populateDropdown("country-1",countries);
        populateDropdown("country-2",countries);
        populateDropdown("country-3",countries);
        populateDropdown("country-4",countries);
        populateDropdown("country-5",countries);
    }
    catch (error){
        console.error("載入下拉選單資料時發生錯誤:", error); 
    }
}

async function loadContinentsDropdownData(jsonFile){
    try {
        const response = await fetch(jsonFile); 
        if (!response.ok) {
            throw new Error(`無法載入 JSON 檔案: ${response.statusText}`);
        }
        const data = await response.json();
        continents = data.continents;
        populateDropdown("continent-1",continents);
    }
    catch (error){
        console.error("載入下拉選單資料時發生錯誤:", error); 
    }
}

function populateDropdown(selectId, options){
    const selectElement = document.getElementById(selectId)
    if(!selectElement) return;
    selectElement.innerHTML = "";
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "-------";
    selectElement.appendChild(defaultOption);
    options.forEach(option => {
        const optionElement = document.createElement("option");
        optionElement.value = option;
        optionElement.textContent = option;
        selectElement.appendChild(optionElement);
    });
}

loadCountriesDropdownData("countries.json");
loadContinentsDropdownData("continents.json");