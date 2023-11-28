
//const medi = require(['@mediapipe/tasks-vision'])


//working vv
var c = document.getElementById("myCanvas");
var ctx = c.getContext("2d");

let video = document.querySelector("#videoElement");
var vidT = "false";

height = 0
frames = []
requests= 0 

video.addEventListener('play',  function () {
    
    
    //console.log(video.style.height)
    //console.log(h)
    var $this = this; //cache
    (function loop() {
        if (!$this.paused && !$this.ended) {
            //frames.push($this)
            /*if (frames.length === 40){
                predict(frames)
                frames=[]
            }*/

            //const dataURI = myCanvas.toDataURL();
            //img = dataURI;
            
            ctx.drawImage($this, 0, 0);
            const imageData = c.toDataURL('image/png');

            frames.push(imageData)
            if (frames.length === 40){
            if (requests < 5){
                predict(frames)
                
                requests+=1
                frames=[]
            }
            
        }
            setTimeout(loop, 1000 / 30); // drawing at 30fps
        }
    })();
}, 0);

function toggleCam(){

if (vidT == "false") {
    vidT = "true"; 
    navigator.mediaDevices.getUserMedia({ video: vidT}).then(function(stream) {
        video.srcObject = stream;
    })
    .catch( function (error){
        console.log("Something didn't go right")
    })
} else{
    console.log("getUserMedia isn't supported!")
    vidT = "false"; 

    navigator.mediaDevices.getUserMedia({ video: vidT}).then(function(stream) {
        video.srcObject = stream;
    })
    .catch( function (error){
        console.log("Something didn't go right")
    })
}
}

function predict(imgs){
    /*var videoElements = [
        'he;;o'
    ];
    var jsonData = JSON.stringify(videoElements);
    console.log(imgs)*/
    /*console.log(imgs)
    $.ajax({ type: "POST",   
         url: "/predict",   
         async: false,
         data: imgs, 
         success : function(text)
         {
             response = text;
         },
         error: function()
         {
            alert("error occured");  
         }
        });
    console.log(response)*/

    fetch('/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ images: imgs }),
      })
        .then(response => {
            if (response.ok) {
                return response.text(); // Extract the response as text
              } else {
                throw new Error('Something went wrong');
              }
        })
        .then(textData => {
            // Use the returned text data in your JavaScript code
            console.log('Text from server:', textData);
            // Further processing or displaying the text as needed
          })
          .catch(error => {
            console.error('Error:', error);
            // Handle errors here if needed
          });
}
//working^^








/*
async function setUp(){
    const vision = await FilesetResolver.forVisionTasks(
// path/to/wasm/root
"https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js"
);
const poseLandmarker = await poseLandmarker.createFromOptions(
vision,
{
  baseOptions: {
    modelAssetPath: "app/shared/models/pose_landmarker_heavy.task"
  },
  runningMode: VIDEO
});
}

async function LiveDetection(){
await poseLandmarker.setOptions({ runningMode: "VIDEO" });

let lastVideoTime = -1;
function renderLoop(){
const video = document.getElementById("videoElement");

if (video.currentTime !== lastVideoTime) {
const poseLandmarkerResult = poseLandmarker.detectForVideo(video);
processResults(detections);
console.log(processResults)
lastVideoTime = video.currentTime;
}

requestAnimationFrame(() => {
renderLoop();
});
}
}

setUp()
LiveDetection()*/