// speech to text for compose

var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

// if (SpeechRecognition) {
//   console.log("your browser supports speech recognition")
var recognizing = false;
var text = "";
var stringValue;
var tostartspeech1;
var data;
var string;
var speechtext = "";
var writing_position;
var reading_position = 1;
var recognition = new SpeechRecognition();
recognition.continuous = true;
recognition.interimResults = false;

recognition.onstart = function () {
    console.log("sr started")
    recognizing = true;
};


recognition.onend = function () {
    console.log("sr deactivate")

    //   to start speech recognition automatically after the stop
    document.getElementById('button').click();
    console.log(" button is clicked inside end function")
    // recognizing = true;
};

recognition.onerror = function (event) {
    if (event.error == 'no-speech') {
        console.log("somethong is not right!")

    }
    if (event.error == 'audio-capture') {
        console.log("no microphone")

    }
};

recognition.onresult = function (event) {
    for (var i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
            textarea.value += event.results[i][0].transcript;
            speechtext += event.results[i][0].transcript;
        }
    }
    text = speechtext.trim()
    console.log(text)

    //     if(text.includes("open inbox") || text.includes("go to inbox"))
    // {
    //     location.replace("{% url 'EmailApp:EmailApp-inbox' %}");
    // }


    if (text.includes("receiver") && !text.includes("message") && !text.includes("subject")) {
        writing_position = "receiver"
        console.log(text)  // text=receiver example
        replaced = text.replace("receiver", "") + "@gmail.com"; //replace = example @gmail.com
        inputEmail.value = replaced.replace(/\s/g, ''); // example@gmail.com 

    }
    else if ((text.includes("subject") || writing_position == "subject") && !text.includes("message")) {
        writing_position = "subject"
        if (inputsubject.value == "") {
            console.log("1st time sunject")
            string = text.replace("subject ", "")
            inputsubject.value = string.charAt(0).toUpperCase() + string.slice(1);
        }
        else {
            inputsubject.value = inputsubject.value + " " + text.replace("subject ", "");
        }
    }
    else if (text.includes("message") || writing_position == "message") {
        writing_position = "message"
        if (message.value == "") {
            console.log("1st time message")
            string = text.replace("message ", "");
            message.value = string.charAt(0).toUpperCase() + string.slice(1);
        }
        else {
            message.value += " " + text.replace("message ", "");
        }

    }
    else if (text.slice(0, 3) == "yes" && message.value != "" && inputEmail.value != "" && inputsubject.value != "") {
        console.log("submitted");
        $.ajax(
            {
                url: "/ajax/submit/",
                data: {
                    receiver: inputEmail.value,
                    subject: inputsubject.value,
                    message: message.value
                },
                success: function (data) {
                    if (data.status == "success") {
                        location.replace("http://127.0.0.1:8000/");
                    }
                }
            })
    }
    else if (text.slice(0, 2) == "no" && message.value != "" && inputEmail.value != "" && inputsubject.value != "") {
        console.log("email not send");
        recognition.abort();
    }



    console.log("funtion run successfully")
    console.log(writing_position)


    speechtext = ""
}


function reset() {
    recognizing = false;
    button.innerHTML = "Click to Speak";

}

tostartspeech1 = function () {
    recognition.start();
    recognizing = true;
}

//   code  to play audio file of inbox introduction  
document.addEventListener("keydown", keyright, false);

function keyright(e) {
    e = e || window.event;
    if (e.keyCode == '39') {
        writing_position = ""
        // press right arrow key to text to speech
        if (reading_position == 1 && inputEmail.value != "") {
            speak = "receiver is" + inputEmail.value
            readOut(speak)
            reading_position = 2
        }
        else if (reading_position == 2 && inputsubject.value != "") {
            speak = "Subject is " + inputsubject.value
            readOut(speak)
            reading_position = 3
        }
        else if (reading_position == 3 && message.value != "") {
            speak = "And the message is" + message.value
            readOut(speak)
            reading_position = 4
        }
        else if (reading_position == 4 && message.value != "" && inputEmail.value != "" && inputsubject.value != "") {
            speak = "if you want to send this mail, say yes, else say no"
            readOut(speak)
        }

    }

}


