window.addEventListener( "load", function () {
  visTypeChange();

  function sendProgData(){
    const req = new XMLHttpRequest();
    const data = new FormData(icurryForm);

    req.addEventListener("load", function(event){
      document.getElementById("loadingArea").innerHTML="";
      switch (event.target.status) {
        case 200:
          window.location.href = "/slideshow?id=" + event.target.responseText;
          break;
        case 400:
          document.getElementById("msgArea").innerHTML=
            "Bad Request, there may have been an error in the supplied program: </br>\
            <pre>" + event.target.responseText; + "</pre>";
          break;
        case 508:
          document.getElementById("msgArea").innerHTML=
            "Evaluation of main expression took too long,\
            likely caused by an infinite loop";
          break;
      }
    });

    req.open("POST", "/slideshow");
    req.send(data);
    document.getElementById("loadingArea").innerHTML="computing graphs..."
  }

  function sendFileData(){
    const req = new XMLHttpRequest();
    const data = new FormData(fileForm);

    req.addEventListener("load", function(event){
      document.getElementById("loadingArea").innerHTML="";
      switch (event.target.status) {
        case 200:
          window.location.href = "/slideshow?id=" + event.target.responseText;
          break;
        case 400:
          document.getElementById("msgArea").innerHTML=
            "Bad Request: </br>\
            <pre>" + event.target.responseText; + "</pre>";
          break;
      }
    });

    req.open("PUT", "/slideshow");
    req.send(data);
  }

  const icurryForm = document.getElementById("icurryForm");

  icurryForm.addEventListener("submit", function(event){
    event.preventDefault();
    document.getElementById("msgArea").innerHTML="";

    if(checkMainFunc(document.getElementById("prog_field").value)) {
      sendProgData();
    } else {
      document.getElementById("msgArea").innerHTML="Program may not include a procedure called 'icurry_main'.";
    }
  });

  const fileForm = document.getElementById("fileForm");

  fileForm.addEventListener("submit", function(event){
    event.preventDefault();
    document.getElementById("msgArea").innerHTML="";
    sendFileData();
  });
});

/*
* Check wether a line in the given string doesn't
* declare an "icurry_main"-procedure.
*/
function checkMainFunc(str){
  lines = str.split('\n');
  for (let line in lines) {
    if (line.indexOf("icurry_main") == 0) {
      return false;
    }
  }
  return true;
}

function loadExample(){
  var example = document.getElementById("example_selector").value;
  if(example != "null"){
    const req = new XMLHttpRequest();

    req.open("POST", '/example');

    //Send the proper header information along with the request
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    //set prog_field and main_exp_field when example is received
    req.addEventListener("load", function() {
      document.getElementById("prog_field").value = req.responseText;
      document.getElementById("main_exp_field").value = "main";
    });
    req.send("example=" + example);
  }
}

function fileValidation(){
  const fileInput = document.getElementById("fileInput");
  let size = 0;
  for (let i = 0; i < fileInput.files.length; i++) {
    size += fileInput.files.item(i).size;
  }
  if(size >= Math.pow(2,20)){
    document.getElementById("msgArea").innerHTML="Files are too large.\
                                              Maximum allowed is 1 MB";
    fileInput.value = "";
  }
}

function clearForm(){
  document.getElementById("prog_field").value="";
  document.getElementById("main_exp_field").value="";
}

function visTypeChange(){
  on = document.getElementById("radio_tree").checked
  if(on){
    document.getElementById("paragraph_depth").style.display = "inline"
  } else {
    document.getElementById("paragraph_depth").style.display = "none"
  }
}
