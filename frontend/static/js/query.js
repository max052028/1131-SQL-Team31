let countries=[];
let continents=[];
let regions={};
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
        populateDropdown("continent-2",continents);
        populateDropdown("continent-3",continents);
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

document.getElementById('submit').addEventListener('click', (event) => {
    const selectedQuery = document.querySelector('input[name="query"]:checked');
    if (!selectedQuery) {
        event.preventDefault();
        alert('請選擇查詢模式！');
        return;
    }
    // 根據查詢模式進行其他驗證
});

loadCountriesDropdownData("/static/data/countries.json");
loadContinentsDropdownData("/static/data/continents.json");