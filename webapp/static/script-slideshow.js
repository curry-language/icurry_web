var slideIndex = 0;
var slideAmount = 2;

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex + n);
}

// Show a specific slide. If more than one slide is shown at a time,
// n will be the first slide.
function showSlides(n) {
  const slides = document.getElementsByClassName("mySlides");

  const dots = document.getElementsByClassName("dot");
  if (n > slides.length-slideAmount) {
    slideIndex = slides.length-slideAmount;
  } else if (n < 0) {
    slideIndex = 0;
  } else {
    slideIndex = n;
  }
  //console.log("Now showing slide " + slideIndex);


  for (let i = 0; i < slides.length; i++) {
    if(i >= slideIndex && i < slideIndex + slideAmount){
      slides[i].style.display = "flex"; //use flex for centering
      dots[i].classList.add("active");
    } else {
      slides[i].style.display = "none";
      dots[i].classList.remove("active");
    }
  }
}

function plusSlideAmount(n) {
  setSlideAmount(slideAmount + n);
}

function setSlideAmount(n) {
  const slides = document.getElementsByClassName("mySlides");
  if(n <= 0) {
    slideAmount = 1;
  } else if (n >= slides.length){
    slideAmount = slides.length;
  } else {
    slideAmount = n;
  }

  for(let i = 0; i < slides.length; i++){
    slides[i].style.flex = (slideAmount * 100 / slides.length) + "%";
  }
  showSlides(slideIndex);
}

function nodeEntered(nid, gid) {
  //console.log("Node " + nid + " in graph " + gid + " entered");
  let nodes = document.getElementsByClassName("node" + nid + " graph" + gid);
  if(nodes.length > 1){
    for(let i = 0; i < nodes.length; i++){
      Array.from(nodes[i].children).forEach(item => item.setAttribute("stroke-width", "5"));
    }
  }
}

function nodeExited(nid, gid) {
  //console.log("Node " + nid + " in graph " + gid + " exited");
  let nodes = document.getElementsByClassName("node" + nid + " graph" + gid);
  let width = "3";
  if(nodes.length > 1){
    if(nodes[0].children[0].getAttribute("stroke") == "black"){
      width = "1";
    }
    for(let i = 0; i < nodes.length; i++){
      Array.from(nodes[i].children).forEach(item => item.setAttribute("stroke-width", width));
    }
  }
}

function popup(href, windowname) {
  if (!window.focus){
    return true;
  }
  window.open(href, windowname, 'width=400,height=600,scrollbars=yes');
  return false;
}
