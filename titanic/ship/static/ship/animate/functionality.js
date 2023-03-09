`use strict`;
var allActions = [];
var statesPerStep = [];
var timeSetList = []
var animateCounter = 0;
var totalStepCount;
var currentInterval;
var initialPage;

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

function str_pad_left(string, pad, length) {
  return (new Array(length + 1).join(pad) + string).slice(-length);
}

function getFixedTime(time) {
  const minutes = Math.floor(time / 60);
  const seconds = time - minutes * 60;

  return str_pad_left(minutes, '0', 2) + ':' + str_pad_left(seconds, '0', 2);
}

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

function checkContainerExist(element){
  return !element.classList.contains("extra-space") && !element.classList.contains("container-UNUSED") && !element.classList.contains("container-NAN");
}

function prepData(listOfSteps, timeSet) {
  totalStepCount = listOfSteps.length
  document.getElementById("total-step").textContent = totalStepCount;
  document.getElementById("estimated-time").textContent = getFixedTime(timeSet[0]);
  timeSetList = timeSet
  initialPage =  document.getElementById("transaction-wrapper").innerHTML;
  allActions = listOfSteps;
  
  let countUnloads = 1;
  let containerName = "", containerPos = [];

  for (let i = 0; i < allActions.length; i++) {   
    let isSkip = true; 
    let tempActionlist = allActions[i];
    let listLength = tempActionlist.length - 1;
    let isLoad = isLoadAction(tempActionlist[0]);

    if(isLoad) {
        containerName = tempActionlist[0];
        containerPos = tempActionlist[listLength];
        isSkip = false;
    } else {
      if (countUnloads % 2 === 1) {
        let itemPosition = tempActionlist[listLength];
        let row = itemPosition[0];
        let column = itemPosition[1];

        containerName = document.querySelector("[row='" + row + "'][column='" + column + "']").textContent.trim();
        containerPos = itemPosition;
        isSkip = false;
      }
      
      countUnloads += 1;
    }
  
      statesPerStep.push({isSkip: isSkip, containerName: containerName, containerPos: containerPos, step: i + 1, isLoad: isLoad});
  }

  initAnimate(0);
}

function isLoadAction(item){
  return typeof item === 'string' || item instanceof String;
}

function toggleAnimation(currentActionList, containerName, step){
  let currentAction = currentActionList[animateCounter];

  currentAction = isLoadAction(currentAction) ? [0, 0] : currentAction;

  let row = currentAction[0];
  let column = currentAction[1];
  let currentElement = document.querySelector("[row='" + row + "'][column='" + column + "']");

  clearActiveStep(step);
  currentElement.classList.toggle("active-step");

  animateCounter += 1;

  if (animateCounter >= currentActionList.length) {
    togglePause();
    currentElement.classList.add("final-loc");
    animateCounter = 0;
    setTimeout(togglePause, 2000);
  }
}

function initAnimate(step) {
  let currentActionList = allActions[step];
  let firstItem = currentActionList[0];
  let itemName = "";

  if (isLoadAction(firstItem)) {
    itemName = firstItem;
    currentActionList[0] = [0, 0];
  }
  
  animateCounter = 0;

  startClear(step);
  currentInterval = setInterval(toggleAnimation, 500, currentActionList, itemName, step);
}

function startClear(step){
  clearInterval(currentInterval);
  currentStep = parseInt(document.getElementById("current-step").textContent.trim());
  currentTime = document.getElementById("estimated-time").textContent.trim();
  document.getElementById("buffer-wrapper").remove();
  document.getElementById("unload-wrapper").remove();

  document.getElementById("transaction-wrapper").innerHTML = initialPage;
  document.getElementById("current-step").textContent = currentStep;
  document.getElementById("estimated-time").textContent = currentTime;

  if(step + 1 === totalStepCount){
    document.getElementById("proccess-complete-button").classList.remove("hidden");
  } else {
    document.getElementById("proccess-complete-button").classList.add("hidden");
  }

  for (let i = 0; i < step; i++) {
    let currentStep = statesPerStep[i];
    let isSkip = currentStep["isSkip"];

    if (!isSkip) {
      let isLoad = currentStep["isLoad"];
      let position = currentStep["containerPos"];
      let containerName = currentStep["containerName"];

      element = document.querySelector("[row='" + position[0] + "'][column='" + position[1] + "']");

      if(isLoad){
        element.innerText = containerName;
        element.classList.add("container-" + containerName);
        element.classList.remove("container-UNUSED")
        element.classList.add("recently-added");
      } else {
        element.getElementsByClassName("grid-content").textContent = "UNUSED";
        element.classList.remove("container-" + containerName)
        element.classList.add("container-UNUSED")
        element.classList.add("recently-removed");
      }
    }
  }
}

function clearActiveStep() {
  activeSteps = document.getElementsByClassName("active-step");
  let finalLoc = document.getElementsByClassName("final-loc")[0]

  if (finalLoc != undefined) {
    finalLoc.classList.remove("final-loc");
  }

  for (let i = 0; i < activeSteps.length; i++) {
    activeSteps[i].classList.remove("active-step");
  }
};

function changeStep(isForward){
  let currentStepElement = document.getElementById("current-step");
  let currentStep = parseInt(currentStepElement.textContent.trim());
  let totalStepElement = document.getElementById("total-step");
  let totalStep = parseInt(totalStepElement.textContent.trim());

  if (!(currentStep === 1 && !isForward) && !(currentStep === totalStep && isForward)){
    clearInterval(currentInterval);
 
    const stepValue = isForward ? currentStep + 1 : currentStep - 1;

    currentStepElement.textContent = stepValue;
    document.getElementById("estimated-time").textContent = getFixedTime(timeSetList[stepValue - 1]);

    initAnimate(stepValue - 1);
  }
}

function togglePause() {
  let pauseButton = document.getElementById("pause-button");
  
  if (pauseButton.textContent.trim() === "Pause"){
    clearInterval(currentInterval);
    pauseButton.textContent = "Continue";
  } else {
    pauseButton.textContent = "Pause";
    initAnimate(parseInt(document.getElementById("current-step").textContent.trim()) - 1);
  }
}

function toggleLog(element){
  if(element.id !== "log-entry-wrapper" || element.parentElement.id !== "log-entry-wrapper") {
    document.getElementById("log-box").classList.toggle("hidden");
  }
}

function toggleProcess(shipid){
  document.getElementById("process-done-box").classList.remove("hidden");

  getFinalContent(shipid);
}

function getFinalContent(shipid){
  clearInterval(currentInterval);
  let finalContainerList = [];
  let containerWeightDict = JSON.parse((document.getElementById("hidden-load-weights") || {}).value || '{}');

  for (let i = 0; i < 8; i++) {
    for (let k = 0; k < 12; k++) {
      let row = i + 1;
      let column = k + 1;
      let container = document.querySelector("[row='" + row + "'][column='" + column + "']");
      let containerName = container.textContent.trim();
      let containerWeight = parseInt(container.getAttribute("weight")) || containerWeightDict[containerName] || 0;

      finalContainerList.push({'containerName': containerName, 'weight': containerWeight, "containerPos":[row, column]})
    }
  }

  $.ajax({ 
    url: "/ship/" + shipid + "/finalize/",
    type: "POST",
    dataType: "json",
    data: {
        finalList: JSON.stringify({"containers":finalContainerList}),
        csrfmiddlewaretoken: getCookie('csrftoken')
        },
    success : function(json) {
      console.log("Success!");
    },
    error : function(xhr, errmsg, err) {
        console.log(err);
    }
  });
}

function containerDone(){
  currentStep = parseInt(document.getElementById("current-step").textContent.trim());
  currentStep = statesPerStep[currentStep - 1]
  isLoad = currentStep['isLoad'];

  if((!isLoad && currentStep['isSkip']) || isLoad){
    logText = "\"" + currentStep['containerName'] + "\" is " + (isLoad ? "loaded." : "unloaded.");

    sendLog(logText);
  }

  changeStep(true);
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

function toggleLogOutBox() {
    document.getElementById("log-out-box").classList.toggle("hidden")

    logText = document.getElementById("operator-name-tag").textContent + " signs out"

    sendLog(logText)
}


function logOut(shipid){
  op_name = document.getElementById('op_first').value
  op_lastname = document.getElementById('op_last').value
  targetUrl =  '/ship/' + shipid + '/logoutAnimate/'


  //help by: https://stackoverflow.com/questions/62773503/how-to-save-a-javascript-variable-to-a-file-in-django-media-folder
  $.ajax({ 
    url: targetUrl,
    type: "POST",
    dataType: "json",
    data: {
        op_first: op_name,
        op_last: op_lastname,
        csrfmiddlewaretoken: getCookie('csrftoken')
        },
    success : function(json) {
      document.getElementById("logout-form").setAttribute("action", "/ship/" + json['op_id'] + "/" + shipid + "/animate/");
      document.getElementById("hidden-submit").click();
    },
    error : function(xhr, errmsg, err) {
      textHtml = document.createElement("div");
      textHtml.classList.add("pop-up");
      textHtml.classList.add("pop-up-error");
      textHtml.textContent = "ERROR: Couldn't Logout!"
      document.body.prepend(textHtml);

      setTimeout(() => {document.getElementsByClassName("pop-up")[0].remove()}, 2500);
    }
  });
}

function togglePorccessComplete() {
  
}