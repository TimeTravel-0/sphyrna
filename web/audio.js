// global vars (ugly...)


var sound_buffer = Array();
var context;
var track;
var playback_position=0;
var playback_state=false;
var timer = setInterval(playbackTick,100);
var channel_states = [];

function GUIupdate(){
  TextTotalShow();
}


function ButtonTogglePlay(){
  togglePlay();
}

function ButtonTotalMinus(){
  totalSet(totalGet()-1);
  TextTotalShow();
}

function ButtonTotalPlus(){
  totalSet(totalGet()+1);
  TextTotalShow();
}

function TextTotalShow()
{
  document.getElementById("TextTotal").value=totalGet();
}

function totalGet(){
  return track[0][0];
}

function totalSet(value){
  track[0][0] = value;
}


function setSpeed(bpm){
  ticktime = 1000*60 / (bpm*4);
  clearInterval(timer)
  timer = setInterval(playbackTick,ticktime);
  track[0][1] = bpm;
}

function getSpeed(){
  return track[0][1];
}

function togglePlay(){
  playback_state = ! playback_state;
}

function run(){
  playback_state = true;
}


function stop(){
  playback_state = false;
}


function playbackTick(){
  if(playback_state==false){
    return;
  }
  //log("playbackTick")
  
  for(var c=0;c<6;c++){
    state = track[2][c][playback_position];
    soundn = track[1][c][1];
    //log("state="+state+" soundno="+soundn)
    stretchto = 0
    // speed adjustment for built-in sounds
    if(soundn>=24 && soundn<29){
        log(getSpeed()+" "+4*60/getSpeed())
//        stretchto = 1/60*(getSpeed()*4); //   ticktime = 1000*60 / (bpm*4);
stretchto=4*60/getSpeed();
    }
    // speed adjustments for .hub needs to be done (and included in the files - somehow...)
    
    
    playSound(soundn, state,1,stretchto);
  }
  
  
  playback_position+=1;    
  if(playback_position >= track[0][0]*16){
    playback_position-=track[0][0]*16;
  }
}




// from http://stackoverflow.com/questions/1766795/javascript-write-console-debug-output-to-browser
function log(msg){
  if (window.console && console.log) {
    console.log(msg); //for firebug
  }
  //document.write(msg); //write to screen
  //$("#logBox").append(msg); //log to container
}

// from http://www.html5rocks.com/en/tutorials/webaudio/intro/

window.addEventListener('load', init, false);
function init() {
  try {
    // Fix up for prefixing
    window.AudioContext = window.AudioContext||window.webkitAudioContext;
    context = new AudioContext();
  }
  catch(e) {
    alert('Web Audio API is not supported in this browser');
  }
  
  loadSounds();
}

function loadSounds() {
    sounds = Array("01_HardBD.wav","02_909BD.wav","03_SubBD.wav","04_JungleBD.wav","05_BlipBD.wav","06_Hardcore909BD1.wav","07_Hardcore909BD2.wav","08_606Snare.wav","09_JungleSnare.wav","10_HardSnare.wav","11_808Snare.wav","12_Ac.Snare1.wav","13_Ac.Snare2.wav","14_909Snare.wav","15_909Clap.wav","16_SnapClap.wav","17_Rimshot.wav","18_909OpenHH.wav","19_909ClosedHH.wav","20_909PedalHH.wav","21_Ac.OpenHH.wav","22_Ac.ClosedHH.wav","23_909Crash.wav","24_[HipHop].wav","25_[FunkyDrummer].wav","26_[Giz1].wav","27_[Giz2].wav","28_[Jungle1].wav","29_[Jungle2].wav","30_user_01.wav","31_user_02.wav","32_user_03.wav","33_user_04.wav","34_user_05.wav","35_user_06.wav")
    for(var k=0; k<sounds.length; k++) {
        loadSound("../wav/"+sounds[k],k+1);
    }
    
}



function onError() {}

function loadSound(url, slot) {
  log("loadSound("+url+","+slot+")");
  var request = new XMLHttpRequest();
  request.open('GET', url, true);
  request.responseType = 'arraybuffer';

  // Decode asynchronously
  request.onload = function() {
    context.decodeAudioData(request.response, function(buffer) {
      log("loadSound() callback for slot "+slot);
      sound_buffer[slot] = buffer
    }, onError);
  }
  request.send();
}

function playSounds(){
  for(var k=1;k<sound_buffer.length;k+=1){
      playSound(k);
  }
}

function playSound(slot, volume, speed, stretchto) {

  volume = typeof volume !== 'undefined' ? volume : 100; // http://stackoverflow.com/questions/894860/set-a-default-parameter-value-for-a-javascript-function#894877
  speed = typeof speed !== 'undefined' ? speed : 1.0; 
  stretchto = typeof stretchto !== 'undefined' ? stretchto : 0;


  if(volume == 0){
    return;
  }

  if(typeof channel_states[slot] !== 'undefined'){
    channel_states[slot].stop();
  }
  
  var source = context.createBufferSource(); // creates a sound source
  channel_states[slot] = source;
  source.buffer = (sound_buffer[slot]);                    // tell the source which sound to play
  
  
  if(stretchto>0){
    speed = 1/(stretchto / source.buffer.duration);
    log("stretch to "+stretchto + "  length "+source.buffer.duration+" factor "+speed)
  }
  
  source.playbackRate.value = speed
  var gainNode = context.createGain(); // Create a gain node.
  gainNode.gain.value = volume/100.0;
  source.connect(gainNode); // Connect the source to the gain node.
  gainNode.connect(context.destination);  // Connect the gain node to the destination.
  source.start(0);                           // play the source now
                                             // note: on older systems, may have to use deprecated noteOn(time);
}



function loadTrack(url){
  var xmlhttp = new XMLHttpRequest();
  log("loadTrack("+url+")");

  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        var myArr = JSON.parse(xmlhttp.responseText);
        loadTrackCallback(myArr);
    }
  }
  xmlhttp.open("GET", url, true);
  xmlhttp.send();
}

function loadTrackCallback(arr){
  log("loadTrack()");
  log(arr);
  track = arr;
  playback_position=0;
  setSpeed(track[0][1]);
}
