# Load from tensorflow, gpu and jupyter supported
FROM tensorflow/tensorflow:latest-gpu-jupyter

# load in the requirements for pip
COPY requirements.txt requirements.txt
RUN ["pip","install","--upgrade","pip"]
RUN ["pip","install","-r","requirements.txt"]

# run jupyter notebook
CMD ["jupyter","notebook","--port","9009","--no-browser","--ip","0.0.0.0","--allow-root"]
