# VoiceCloner

## Overview
This project is to clone the voice with the selected text using TTS which is based on Pytorch framework.
It involves high-performance Deep Learning models for Text2Speech tasks, Text2Spec models (Tacotron, Tacotron2, 
Glow-TTS, SpeedySpeech), speaker encoder to compute speaker embeddings efficiently and 
vocoder models (MelGAN, Multiband-MelGAN, GAN-TTS, ParallelWaveGAN, WaveGrad, WaveRNN).
Using Flask server, user can upload the wav file and the prompt to download the cloned wav file.

## Structure
- src
    * The main engine of voice cloning
- static
    * style part
- templates
    * UI to upload file and prompt
- app.py
    * The Flask server
- requirements
    * all the dependencies of this project
- settings
    * Several settings of this project

## Installation
- Environment
    * Ubuntu 20.04+, Python3.9+, Nvidia Geforce GTX/RTX
- CUDA, CUDNN Installation
    * Please run the following command in ther terminal.
  ```
    sudo apt update && sudo apt upgrade
    ubuntu-drivers devices
    sudo apt install nvidia-driver-535 ("recommend version")
    sudo reboot
    nvidia-smi
    sudo apt update
    sudo apt install nvidia-cuda-toolkit
    wget https://developer.download.nvidia.com/compute/cudnn/9.2.0/local_installers/cudnn-local-repo-ubuntu2204-9.2.0_1.0-1_amd64.deb
    sudo dpkg -i cudnn-local-repo-ubuntu2204-9.2.0_1.0-1_amd64.deb
    sudo cp /var/cudnn-local-repo-ubuntu2204-9.2.0/cudnn-*-keyring.gpg /usr/share/keyrings/
    sudo apt-get update
    sudo apt-get -y install cudnn-cuda-11 ("according to cuda version") 
  ```
- Dependency Installation
    * Please run the following command in the terminal.
    ```
      pip install TTS
      pip install flask_cors
  ```
  
## Execution
- Please set the several constants in settings file and run the following command in the terminal.
  ```
    python3 app.py
  ```
- The server launches at 5000 port.
