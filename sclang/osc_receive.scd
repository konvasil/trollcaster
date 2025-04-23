(
SynthDef(\glitchTroll, {
    |out = 0, trigFreq = 8, feedback=0.3, noiseFreq = 1000, burstFreq = 200, amp = 0.5|

    var sig, trig, noise, burst, env, mod, pitchEnv, glitchEffect, feedbackSignal;

    // Trigger: Impulse generator with randomized frequency
    trig = Impulse.kr(trigFreq + Rand(0, 10));

    // Noise source with random frequency modulation
    noise = LFNoise1.ar(noiseFreq + Rand(0, 1000)) * Decay2.kr(trig, 0.01, 0.2);

    // Band-pass filter for the noise burst, with randomized frequency range
    burst = BPF.ar(noise, burstFreq + Rand(0, 5000), 0.3 + Rand(0, 0.5));

    // Envelope: Create a sharper attack-decay envelope for each glitch
    env = EnvGen.kr(Env.perc(0.001, 0.3), trig, doneAction: 2);

    // Pitch modulation: A sine wave for random pitch bending
    pitchEnv = LFNoise1.kr(1 + Rand(0, 0.5)) * 0.5;

    // Modulate the burst with some pitch shifting
    sig = burst * env * pitchEnv * amp;

	feedbackSignal = sig + (DelayC.ar(sig, 0.1, 0.1) * feedback);

    // Additional glitch effects: A high-frequency oscillator to add more chaos
    glitchEffect = SinOsc.ar(Rand(500, 2000), Rand(0, 1), 0.2) * EnvGen.kr(Env.perc(0.001, 0.3), trig);

    // Combine all elements together
    sig = sig + glitchEffect+ feedbackSignal;

    // Output the signal in stereo
    Out.ar(out, sig.dup);
}).add;
);

// Listen for incoming OSC messages from Flask
OSCdef(\triggerGlitch, { |msg|
    // Play the glitchTroll synth when a trigger message is received
    Synth(\glitchTroll, [
        \trigFreq, 8,               // Adjust the trigger frequency (default)
        \noiseFreq, 1000,           // Noise frequency (default)
        \burstFreq, 500,            // Burst frequency (default)
        \amp, 0.5,                   // Amplitude (default)
		\out, 0]);
	msg.postln
}, '/trigger');

OSCdef(\triggerGlitch).enable;


