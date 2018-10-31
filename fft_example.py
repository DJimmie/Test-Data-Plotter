import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy as np
from scipy import fftpack
from scipy.io import wavfile


def other_data():
    f = .25 # Frequency, in cycles per second, or Hertz
    f_s = 1 # Sampling rate, or number of measurements per second

    t = np.linspace(0, 100, 2 * f_s, endpoint=False)
    x = np.sin(f * 2 * np.pi * t)


    fig, ax = plt.subplots()
    ax.plot(t, x, color='blue')
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Signal amplitude')


def the_fft(x,f_s):
    X = fftpack.fft(x)
    freqs = fftpack.fftfreq(len(x)) * f_s

    fig, ax = plt.subplots()
    ax.plot(freqs, np.abs(X))
    ax.set_xlabel('Frequency in Hertz [Hz]')
    ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
    ax.set_xlim(-f_s / 2, f_s / 2)
    ax.set_ylim(-5, 110)
##    plt.show()



if __name__ == '__main__':
    
    rate, audio = wavfile.read('Graphical Programming.wav')
    audio=audio[0:100000]
    print(rate)
    print(audio)

    ##audio = np.mean(audio[0:1000], axis=1)
    
    N = audio.shape[0]
    print (N)
    L = N / rate

    print(f'Audio length: {L:.2f} seconds')

    f, ax = plt.subplots()
    ax.plot(np.arange(N) / rate, audio)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude [unknown]')

    the_fft(audio,rate)
    
    plt.show()

    

