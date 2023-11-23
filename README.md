# Music in Your Head  
*This project is a part of [Brain Code Camp 2023](https://course-braincodecamp.web.app/intro.html). For more info, please read [my article](https://medium.com/@paul.mongkud/music-in-your-head-my-first-step-towards-neuroscience-703ca32c28b8).*

## Datasets
1. **Joint EEG-fMRI** - A dataset recording joint EEG-fMRI during affective music listening. [Link to OpenNeuro](https://openneuro.org/datasets/ds002725/versions/1.0.0/)
2. **OpenMIIR** - Open Music Imagery Information Retrieval. [Link to GitHub](https://openmiir.github.io/)

## File Contents
### Joint EEG-fMRI Dataset
- EEG Preprocessing - [ONR_EEG_Preprocessing.ipynb](https://github.com/PPPaully/music-in-your-head/blob/main/ONR_EEG_Preprocessing.ipynb)
  - Using auto ICA labeling from the [mne-tools](https://github.com/mne-tools/mne-icalabel)
  - Can be executed with [script_preprocess.ipynb](https://github.com/PPPaully/music-in-your-head/blob/main/script_preprocess.ipynb)
  - Output results at `preprocessing/__.ipynb` and `preprocessing/data/___.fif`
- Music Preparation - [ONR_Music_Preprocessing.ipynb](https://github.com/PPPaully/music-in-your-head/blob/main/ONR_Music_Preprocessing.ipynb)
- Models - [ONR_Neural_Decoding_Model.ipynb](https://github.com/PPPaully/music-in-your-head/blob/main/ONR_Neural_Decoding_Model.ipynb)

### OpenMIIR Dataset
- Fix mne can't load data from old version - [OMIIR_Explore.ipynb](https://github.com/PPPaully/music-in-your-head/blob/main/OMIIR_Explore.ipynb)
  - Can import as function by `from read_ica import read_ica` - [read_ica.py](https://github.com/PPPaully/music-in-your-head/blob/main/read_ica.py)
- EEG & Music Preparation - [OMIIR_Preprocessing.ipynb](https://github.com/PPPaully/music-in-your-head/blob/main/OMIIR_Preprocessing.ipynb)
  - Using pre-computed ICA from the dataset
- Models - [OMIIR_Neural_Decoding_Model.ipynb](https://github.com/PPPaully/music-in-your-head/blob/main/OMIIR_Neural_Decoding_Model.ipynb)

### Experiments
Folder [/experiments](https://github.com/PPPaully/music-in-your-head/tree/main/experiments) contains results from training models with
1. Listening set (MLP + LSTM)
2. Imagination set (MLP)

**Note:** Some outputs was deprecated due to file size.  

## Citations
- Daly, Ian, et al. "[Electroencephalography reflects the activity of sub-cortical brain regions during approach-withdrawal behaviour while listening to music.](https://www.nature.com/articles/s41598-019-45105-2)" Scientific reports 9.1 (2019): 9415.
- Daly, Ian. "[Neural decoding of music from the EEG.](https://www.nature.com/articles/s41598-022-27361-x)" Scientific Reports 13.1 (2023): 624.
- Stober, Sebastian, et al. "[Towards Music Imagery Information Retrieval: Introducing the OpenMIIR Dataset of EEG Recordings from Music Perception and Imagination.](https://www.semanticscholar.org/paper/Towards-Music-Imagery-Information-Retrieval%3A-the-of-Stober-Sternin/cde4b1ec89f2c05a41f1143792a890a00e89541a)" ISMIR. 2015.
