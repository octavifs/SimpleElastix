FROM ubuntu:17.10

RUN apt update
RUN apt install -y build-essential cmake python3 python3-dev python3-pip monodevelop r-base r-base-dev ruby ruby-dev tcl tcl-dev tk tk-dev
RUN pip3 install jupyter ipython numpy matplotlib scipy pandas scikit-learn

COPY ./ /simpleelastix
WORKDIR /simpleelastix/build
RUN cmake -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python3 -DPYTHON_LIBRARY:FILEPATH=/usr/lib/x86_64-linux-gnu/libpython3.6.so -DPYTHON_INCLUDE_DIR:PATH=/usr/include/python3.6 -DBUILD_EXAMPLES=OFF -DBUILD_TESTING=OFF ../SuperBuild
RUN make -j8
WORKDIR /simpleelastix/build/SimpleITK-build/Wrapping/Python/Packaging
RUN python3 setup.py install

RUN mkdir  ~/.jupyter
RUN printf "c.NotebookApp.ip = '0.0.0.0'\nc.NotebookApp.token = ''\n" > ~/.jupyter/jupyter_notebook_config.py

WORKDIR /notebooks
EXPOSE 8888
ENTRYPOINT ["jupyter", "notebook", "--no-browser", "--allow-root"]
