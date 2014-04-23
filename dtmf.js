

var context = new webkitAudioContext(),//webkit browsers only

low = context.createOscillator();
low.type = 0; // sine wave
low.frequency.value = 440;

high = context.createOscillator();
high.type = 0; // sine wave
high.frequency.value = 480;
low.connect(high);

high.connect(context.destination);

high.noteOn && high.noteOn(0);



/*
 * freq: frequency in hz
 * duration: length in seconds
 * sampleRate: sampling rate in hz
 */
function tone(freq, duration, sampleRate) {
  duration = sampleRate * duration;

  var curve = [];
  for (var i=0; i < duration; i++) {
    curve.push(Math.sin((2 * Math.PI) * freq * (i / sampleRate)));
  }

  return curve;
}

function silence(duration, sampleRate) {
  duration = sampleRate * duration;

  var curve = [];
  for (var i=0; i < duration; i++) {
    curve.push(0);
  }

  return curve;
}

function tone_sum(tone1, tone2) {
  var sum = [];

  for (var i=0; i < tone1.length && i < tone2.length; i++) {
    sum.push(
      (i < tone1.length ? tone1[i] : 0) + (i < tone2.length ? tone2[i] : 0)
    );
  }

  return sum;
}

function chop_tone(tone) {
  for (var i=0; i < tone.length; i++) {
    if (tone[i] > 1) {
      tone[i] = 1;
    } else if (tone[i] < -1) {
      tone[i] = -1;
    }
  }

  return tone;
}
function normalize_tone(tone) {
  var max = tone.reduce(function(val1, val2) {return Math.max(val1, val2);});

  for (var i=0; i < tone.length; i++) {
    tone[i] = tone[i] / max;
  }

  return tone;
}


var sampleRate = 44100;
var ringback_tone = tone_sum(tone(400, 0.4, sampleRate), tone(450, 0.4, sampleRate));
var ringback_curve = normalize_tone(ringback_tone.concat(silence(0.2, sampleRate)).concat(ringback_tone).concat(silence(2, sampleRate)));

var wave = new RIFFWAVE();
wave.header.sampleRate = sampleRate;
wave.header.numChannels = 1;
wave.Make(convert255(ringback_curve));

var audio = new Audio();
audio.src = wave.dataURI;

setTimeout(function() { audio.play(); }, 10);

