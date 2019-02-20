{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "import wave\n",
    "import numpy as np"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [],
   "source": [
    "file = \"D:/MLDataset/SpeechAnalysis/Japanese/Yes_No/wavFiles/hai-hai.wav\"\n",
    "saveFileName = \"D:/MLDataset/SpeechAnalysis/Japanese/Yes_No/outputFiles/hai-hai-pitch1.wav\"\n",
    "wr = wave.open(file, 'r')\n",
    "#Set output file\n",
    "par = list(wr.getparams())\n",
    "par[3]= 0\n",
    "par = tuple(par)\n",
    "ww = wave.open(saveFileName, 'w')\n",
    "ww.setparams(par)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Process sound in fraction of seconds\n",
    "fr = 20 #Larger the number the less reverb \n",
    "#Read and process one frame at a time\n",
    "sz = wr.getframerate()//fr\n",
    "\n",
    "c = int(wr.getnframes()/sz)\n",
    "\n",
    "#Shift sound by 100 Hz\n",
    "shift = 100//fr\n",
    "for num in range(c):\n",
    "    #read in file and split left and right channel\n",
    "    da = np.frombuffer(wr.readframes(sz), dtype=np.int16)\n",
    "    left, right = da[0::2], da[1::2] #Get the left and right channel\n",
    "    \n",
    "    lf,rf = np.fft.rfft(left), np.fft.rfft(right)\n",
    "    #Roll array to increase pitch\n",
    "    lf, rf = np.roll(lf, shift), np.roll(rf, shift)\n",
    "    #Zero the higest frequencies as they roll over the lowerst ones\n",
    "    lf[0:shift], rf[0:shift] = 0, 0\n",
    "    \n",
    "    #inverse fourier transform to convert backtoamplitude\n",
    "    nl,nr = np.fft.irfft(lf), np.fft.irfft(rf)\n",
    "    #Combine two channels\n",
    "    ns = np.column_stack((nl, nr)).ravel().astype(np.int16)\n",
    "    \n",
    "    #Write the output data\n",
    "    ww.writeframes(ns.tostring())\n",
    "    \n",
    "wr.close()\n",
    "ww.close()\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.5.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
