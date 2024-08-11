
var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

// if (SpeechRecognition) {
//   console.log("your browser supports speech recognition")
var recognizing = false;
var text = "";
var stringValue;
var tostartspeech;
var data;
var recognition = new SpeechRecognition();
recognition.continuous = true;
recognition.interimResults = false;

recognition.onstart = function () {
  console.log("sr started")
  recognizing = true;
};


recognition.onend = function () {
  console.log("sr deactivate")

  // console.log(stringValue);
  // var u = new SpeechSynthesisUtterance();
  if (stringValue) {
    //   if (stringValue.message != "error") {
    //     u.text = stringValue.message;
    //     u.lang = 'en-US';
    //     u.rate = 0.9;
    //     speechSynthesis.speak(u);
    //   }

    if (stringValue.message != "error") {
      readOut(stringValue.message)
    }
    if (stringValue.url) {
      window.location = stringValue.url

    }
    console.log("inside stringvalue ")


  }


  // to start speech recognition automatically after the stop
  document.getElementById('button').click();
  console.log(" button is clicked inside end function")
  // recognizing = true;
};

recognition.onerror = function (event) {
  if (event.error == 'no-speech') {
    console.log("NO audio!")

  }
  if (event.error == 'audio-capture') {
    console.log("no microphone")

  }
};

recognition.onresult = function (event) {
  for (var i = event.resultIndex; i < event.results.length; ++i) {
    if (event.results[i].isFinal) {

      text += event.results[i][0].transcript;
    }
  }
  console.log(text)

  $.ajax(
    {
      type: "GET",
      url: "/ajax/recognized/",
      data: {
        post_id: text,
        post_mess_id: messid,
        post_label: Label
      },
      success: function (data) {
        console.log(data);
        stringValue = data;
        recognition.stop();

      },
      error: function (error) {
        console.log(error)
        console.log('danger', 'ups..something went wrong')

      }
    })



  text = ""
}


function reset() {
  recognizing = false;
  button.innerHTML = "Click to Speak";

}

tostartspeech = function () {
  recognition.start();
  recognizing = true;
}

   // toggleStartStop = function() {
   //    if (recognizing) {
   //      recognition.stop();
   //      // recognizing = false;
   //      reset();
   //    } else {
   //      recognition.start();
   //      recognizing = true;
   //      button.innerHTML = "Click to Stop";
   //    }
   //  }











