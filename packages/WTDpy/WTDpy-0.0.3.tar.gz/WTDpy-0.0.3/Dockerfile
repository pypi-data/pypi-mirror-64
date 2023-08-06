# Start with docker image from anaconda
FROM continuumio/miniconda3

# Set working directory
WORKDIR /wtdpy

COPY requirements.txt /wtdpy/requirements.txt
COPY test-requirements.txt /wtdpy/test-requirements.txt

# Then install rest via pip
RUN \
    pip install --upgrade pip \
    && pip install -r ./requirements.txt \
    && pip install -r ./test-requirements.txt

ADD . /wtdpy

# Install the application
RUN pip install -e .

# expose port 5000
EXPOSE 5000
# Serve on port 5000
CMD wtdpy serve --port 5000
