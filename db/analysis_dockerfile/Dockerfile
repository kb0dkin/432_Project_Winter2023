# base image
FROM tensorflow/tensorflow:latest-gpu-jupyter

# update pip and install necessary reqs
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# set up to run Jupyter however desired
CMD ["jupyter","notebook","--port","9009","--no-browser"]
