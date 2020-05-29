FROM nvcr.io/nvidia/tensorflow:19.05-py3 

RUN apt-get update
RUN apt-get install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg libav-tools python3-pyaudio wget git vim nano
# install c++ libs
RUN apt-get install -y cmake libboost-all-dev
# instalar dependencias ctc da Baidu
RUN apt-get install -y pkg-config libflac-dev libogg-dev libvorbis-dev libboost-dev swig python-dev python-pip

RUN python3 -m pip install -U pip

RUN git clone https://github.com/Edresson/OpenSeq2Seq

WORKDIR OpenSeq2Seq

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install  setuptools

# install OpenSeq2Seq Requeriments
RUN python3 -m pip install  numpy nltk==3.2.5 resampy pandas==0.23.0 six mpi4py joblib==0.13.2 librosa==0.6.3 python_speech_features matplotlib sentencepiece sacrebleu h5py tqdm future-fstrings 

# install CTC da Baidu a saida esperada final é "Finished processing dependencies for ctc-decoders==1.1"
RUN bash ./scripts/install_decoders.sh

# install kenlm 
RUN bash ./scripts/install_kenlm.sh

WORKDIR /mnt/