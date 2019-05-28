FROM python:3.6

ADD ./requirements.txt /opt/solidity/requirements.txt

RUN pip install --no-cache-dir -r /opt/solidity/requirements.txt

RUN ln -s /root/.py-solc/solc-v0.4.25/bin/solc /usr/bin/solc

RUN python -m solc.install v0.4.25

WORKDIR /opt/election
