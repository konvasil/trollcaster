(
// Glitch SynthDef
SynthDef(\glitchTroll, {
    |out=0|
    var sig, trig, noise, burst, env;

    trig = Impulse.kr(8 + Rand(0, 10));
    noise = LFNoise2.ar(1000 + Rand(0, 1000)) * Decay2.kr(trig, 0.01, 0.2);
    burst = BPF.ar(noise, Rand(200, 8000), 0.2);

    env = EnvGen.kr(Env.perc(0.001, 0.3), doneAction: 2);
    sig = burst * env * 0.5;

    Out.ar(out, sig.dup);  // stereo
}).add;
)

Synth(\glitchTroll);

(
// OSCdef to receive the trigger
OSCdef(\triggerGlitch, {
    arg msg;
    "[SC] OSC Trigger received!".postln;
    Synth(\glitchTroll);
}, '/trigger');
)
