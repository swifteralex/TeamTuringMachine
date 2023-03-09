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


//Help from: https://docs.djangoproject.com/en/4.0/ref/csrf/#:%7E:text=Setting%20the%20token%20on%20the%20AJAX%20request¶
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

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
  var className = "container-" + elementName;
  var elementList = document.getElementsByClassName(className);
  

  if (element.classList.contains("container-list")) {
    for (let i = 0; i < elementList.length; i++) {
      elementList[i].classList.toggle("list-highlight");
    }
  } else if (elementName.toLowerCase() !== "nan" && elementName.toLowerCase() !== "unused") {
    if(elementList.length > 0 && !elementList[0].classList.contains("container-clicked")){
      updateCounts(true, 1);
    } else if (elementList.length > 0 && elementList[0].classList.contains("container-clicked")) {
      updateCounts(true, -1);
    }
  
    element.classList.toggle("container-clicked");
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
    searchDoc.classList.add("hidden");
    unloadDoc.classList.add("hidden");    
  } else {
    loadDoc.classList.add("hidden");
    searchDoc.classList.remove("hidden");
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

    liElement.textContent = amount + " " + name + " each weighing " + weight + "kg has been added to the load list";
    liElement.classList.add("added-container");
    liElement.classList.add("unload-item-id-" + itemCountForIds);
    liElement.setAttribute("name", name);
    liElement.setAttribute("amount",amount);
    liElement.setAttribute("weight", weight);

    buttonElement.classList.add("remove-button");
    buttonElement.textContent = "-"
    buttonElement.classList.add("unload-item-id-" + itemCountForIds);

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


function submitValues() {
  var unloadItems = document.getElementsByClassName("container-clicked");
  var loadItems = document.getElementsByClassName("added-container");
  var loadInput = document.getElementById("hidden-load-input");
  var unloadInput = document.getElementById("hidden-unload-input");
  var loadWeights = document.getElementById("hidden-load-weights");
  var loadItemList = [];
  var unloadItemList = [];
  var loadWeightsDict = {};

  for (let i = 0; i < unloadItems.length; i++) {
    let coordinate = [unloadItems[i].getAttribute("row"), unloadItems[i].getAttribute("column")];
    unloadItemList.push(coordinate);
  }

  for (let i = 0; i < loadItems.length; i++) {
    containerName = loadItems[i].getAttribute("name");
    loadWeightsDict[containerName] = parseInt(loadItems[i].getAttribute("weight"));

    for (let j = 0; j < loadItems[i].getAttribute("amount"); j++) {
      loadItemList.push(containerName);
    }
  }

  loadInput.setAttribute("value", loadItemList.join("./."));
  unloadInput.setAttribute("value", unloadItemList.join("./."));
  loadWeights.setAttribute("value", JSON.stringify(loadWeightsDict));
  document.getElementById("secret-submit-button").click();
}


function submitLogEntry(){
  logElement = document.getElementById("log-entry");
  logText = logElement.value;

  sendLog(logText);
}


function sendLog(logText){
    targetUrl =  document.getElementById("submit-log").getAttribute("target");

    //help by: https://stackoverflow.com/questions/62773503/how-to-save-a-javascript-variable-to-a-file-in-django-media-folder
    $.ajax({ 
      url: targetUrl,
      type: "POST",
      dataType: "json",
      data: {
          logEntry: logText,
          csrfmiddlewaretoken: getCookie('csrftoken')
          },
      success : function(json) {
        textHtml = document.createElement("div");
        textHtml.classList.add("pop-up");
        textHtml.textContent = "Log has been successfully updated!"
        document.body.prepend(textHtml);

        setTimeout(() => {document.getElementsByClassName("pop-up")[0].remove()}, 2500);
      },
      error : function(xhr, errmsg, err) {
        textHtml = document.createElement("div");
        textHtml.classList.add("pop-up");
        textHtml.classList.add("pop-up-error");
        textHtml.textContent = "ERROR: Log couldn't update!"
        document.body.prepend(textHtml);

        setTimeout(() => {document.getElementsByClassName("pop-up")[0].remove()}, 2500);
      }
    });
}

function toggleLog(element){
  if(element.id !== "log-entry-wrapper" || element.parentElement.id !== "log-entry-wrapper") {
    document.getElementById("log-box").classList.toggle("hidden");
  }
}

function toggleLogOutBox() {
  document.getElementById("log-out-box").classList.toggle("hidden") 
      
  logText = document.getElementById("operator-name-tag").textContent + " signs out"

  sendLog(logText)
}