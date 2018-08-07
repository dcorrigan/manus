FROM python

RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install matplotlib
RUN pip install cython
RUN pip install scikit-image
RUN pip install imageio
RUN pip install pytest
RUN pip install pillow
RUN pip install scikit-learn
RUN pip install opencv-python
RUN pip install ipdb

COPY ./ /app

WORKDIR /app/

CMD while true; do sleep 1000; done
