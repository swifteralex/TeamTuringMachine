`use strict`;
itemCountForIds = 0;

function refreshTime() {
  const timeDisplay = document.getElementById("clock_time");
  const dateString = new Date()
  const hoursMin = dateString.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    });

  timeDisplay.textContent = hoursMin;
}

setInterval(refreshTime, 1000);

//Got help from: https://www.w3schools.com/howto/howto_js_filter_dropdown.asp
function openDropdown() {
  document.getElementById("dropdown-content").classList.toggle("show");
}

function filterFunction() {
  var input, filter, span;
  input = document.getElementById("container-input");
  filter = input.value.toUpperCase();
  div = document.getElementById("dropdown-content");
  span = div.getElementsByTagName("span");

  for (i = 0; i < span.length; i++) {
    txtValue = span[i].textContent || span[i].innerText;

    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      span[i].style.display = "";
    } else {
      span[i].style.display = "none";
    }
  }
}

function highlightElements(element){
  var elementName = element.textContent.trim()

  if (elementName.toLowerCase() !== "nan" && elementName.toLowerCase() !== "unused") {
    var className = "container-" + elementName
    var elementList = document.getElementsByClassName(className)

    for (let i = 0; i < elementList.length; i++) {
      elementList[i].classList.toggle("container-highlight");
    }
  }
}

function toggleClick(element) {
  var elementName = element.textContent.trim()

  if (elementName.toLowerCase() !== "nan" && elementName.toLowerCase() !== "unused") {
    var className = "container-" + elementName;
    var elementList = document.getElementsByClassName(className);

    if(elementList.length > 0 && !elementList[0].classList.contains("container-clicked")){
      updateCounts(true, 1);
    } else if (elementList.length > 0 && elementList[0].classList.contains("container-clicked")) {
      updateCounts(true, -1);
    }

    for (let i = 0; i < elementList.length; i++) {
      elementList[i].classList.toggle("container-clicked");
    }
  }
}

function updateCounts(isLoad, value) {
  if (isLoad) {
    var doc = document.getElementById("load-count-value")
    var current = parseInt(doc.textContent.trim());

    doc.textContent = current + value;
  } else {
    var current = parseInt(document.getElementById("unload-count-value").textContent.trim());
    
    document.getElementById("unload-count-value").textContent = current + value;
  }
}


function toggleType(type) {
  var isLoad = type == "load" ? true : false;
  var loadDoc = document.getElementById("load-wrapper");
  var unloadDoc = document.getElementById("unload-wrapper");
  var searchDoc = document.getElementById("search-box");

  if (isLoad) {
    loadDoc.classList.remove("hidden");
    searchDoc.classList.remove("hidden");
    unloadDoc.classList.add("hidden");    
  } else {
    loadDoc.classList.add("hidden");
    searchDoc.classList.add("hidden");
    unloadDoc.classList.remove("hidden");
  }
}

function triggerContainerAppend() {
  var nameDoc = document.getElementById("container-typed-name")
  var weightDoc = document.getElementById("container-typed-weight")
  var amountDoc = document.getElementById("container-typed-amount")
  var name = nameDoc.value.trim();
  var weight = weightDoc.value.trim();
  var amount = amountDoc.value.trim();
  
  if (name === "") {
    nameDoc.classList.add("error");
  }

  if (weight === "") {
    weightDoc.classList.add("error");
  }

  if (amount === "") {
    amountDoc.classList.add("error");
  }

  if (name !== "" && weight !== "" && amount !== "") {
    nameDoc.classList.remove("error");
    weightDoc.classList.remove("error");
    amountDoc.classList.remove("error");

    let buttonElement = document.createElement('button');
    let liElement = document.createElement('li');
    var ulList = document.getElementById("container-added-list");
    var listLength = document.querySelectorAll(".container-added-list li").length + 1

    liElement.textContent = amount + " " + name + " each weighing " + weight + "kg has been added to the load list";
    liElement.classList.add("added-container");
    liElement.classList.add("unload-item-id-" + itemCountForIds);
    buttonElement.classList.add("remove-button");
    buttonElement.textContent = "-"
    buttonElement.classList.add("unload-item-id-" + itemCountForIds);
    buttonElement.setAttribute("onclick","removeItem(this.classList, " + amount + ")");

    liElement.append(buttonElement);
    ulList.prepend(liElement);
    
    updateCounts(false, parseInt(amount));
    
    itemCountForIds += 1;
  }
}

function removeItem(clickedId, currentAmount) {
  let currentClass = clickedId[1].trim();

  document.getElementsByClassName(currentClass)[0].remove();

  updateCounts(false, -currentAmount);
}