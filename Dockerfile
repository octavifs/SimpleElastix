FROM python:3.6 AS simpleelastix_python

RUN pip install jupyter ipython numpy matplotlib scipy pandas scikit-learn
RUN apt update
RUN apt install -y cmake swig

COPY ./ /simpleelastix
WORKDIR /simpleelastix/build
RUN cmake ../SuperBuild
RUN make -j2
WORKDIR /simpleelastix/build/SimpleITK-build/Wrapping/Python/Packaging
RUN python setup.py install

RUN mkdir  ~/.jupyter
RUN printf "c.NotebookApp.ip = '0.0.0.0'\nc.NotebookApp.token = ''\n" > ~/.jupyter/jupyter_notebook_config.py

WORKDIR /notebooks
EXPOSE 8888
ENTRYPOINT ["jupyter", "notebook", "--no-browser", "--allow-root"]
