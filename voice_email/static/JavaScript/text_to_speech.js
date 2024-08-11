// function for speaking any message
function readOut(msg) {
  // document.getElementById('speakbtn').click();
  // console.log("speakbtn is clicked")
  console.log("inside readout funtion");
  var speech = new SpeechSynthesisUtterance();
  speech.text = msg;
  speech.lang = 'en-US';
  speech.volume = 1;
  window.speechSynthesis.speak(speech);
  console.log("speaking out");
  return 0;
}







