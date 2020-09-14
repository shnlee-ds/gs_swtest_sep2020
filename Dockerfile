FROM python:3.8-slim
WORKDIR /Sunghun
COPY model.py model.py
COPY controller.py controller.py
COPY view.py view.py
COPY sample.txt sample.txt
COPY requirements.txt requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 80 
CMD ["python3","view.py"]