# Python audio library

Functions written in python for audio processing using [sms-tools](https://github.com/MTG/sms-tools)
library (by MTG in UPF) and other python scientific computation and visualization
libraries like numpy, scipy and matplotlib.


## Instructions

Debian or Debian based systems (like Ubuntu) are recommended but it should work in other systems too if the correct libraries are present. Necesary python libraries: numpy , matplotlib, scipy, and cython.

For using sms-tools library you need to compile some C functions. For that you should go to the directory <code>lib/sms-tools/models/utilFunctions_C</code> and execution a python compilation script:
```
python compileModule.py build_ext --inplace
```


## Content

Available functions:
* *stft_onset*: Computes onset detection (beginning of a musical note) on a wav audio file using the short
  time fourier transform.
* *segment_stable_notes_monophonic*: Segments monophonic audio in different stable notes regions.
* *compute_inharmonicity_monophonic*: Computes the inharmonicity of a monophonic sound using the
  harmonic model.


