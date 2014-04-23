

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
 * Creates an array of values representing a musical tone of the given frequency
 *
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

/*
 * Creates an array of values representing silence
 *
 * duration: length in seconds
 * sampleRate: sampling rate in hz
 */
function silence(duration, sampleRate) {
  duration = sampleRate * duration;

  var curve = [];
  for (var i=0; i < duration; i++) {
    curve.push(0);
  }

  return curve;
}

/*
 * Merges 2 tones into 1
 *
 * Warning this does not ensure the values are normalized
 */
function tone_sum(tone1, tone2) {
  var sum = [];

  for (var i=0; i < tone1.length && i < tone2.length; i++) {
    sum.push(
      (i < tone1.length ? tone1[i] : 0) + (i < tone2.length ? tone2[i] : 0)
    );
  }

  return sum;
}

/*
 * Normalizes the tone to values between 1 and -1
 */
function normalize_tone(tone) {
  var max = tone.reduce(function(val1, val2) {return Math.max(val1, val2);});

  for (var i=0; i < tone.length; i++) {
    tone[i] = tone[i] / max;
  }

  return tone;
}

/*
 * Converts the tone into values between 0 to 255
 */
function convert255(tone) {
  var curve = [];
  for (var i=0; i < tone.length; i++) {
    curve[i]=128 + Math.round(127 * tone[i]);
  }
  return curve;
}


var sampleRate = 44100;
var ringback_tone = tone_sum(tone(440, 2, sampleRate), tone(480, 2, sampleRate));
var ringback_curve = normalize_tone(ringback_tone.concat(silence(4, sampleRate)));

var wave = new RIFFWAVE();
wave.header.sampleRate = sampleRate;
wave.header.numChannels = 1;
wave.Make(convert255(ringback_curve));

var ringback = new Audio();
ringback.src = wave.dataURI;
// loop doesn't seem to want to work
// so until then we have an event listener do the looping for us
// when the loop attribute is fixed, we can drop the listener
ringback.loop = true;
ringback.addEventListener('ended', function() {
  if (this.loop) {
    this.currentTime = 0;
    this.play();
  }
}, false);

setTimeout(function() { audio.play(); }, 10);

