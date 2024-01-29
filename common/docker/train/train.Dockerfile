FROM python:3.10

RUN apt-get update
RUN apt-get install --yes libgl1

RUN useradd --create-home --user-group --uid 9001 --shell /bin/bash stm32ai

USER 9001:9001

RUN mkdir -p /tmp/inputs /tmp/outputs \
    /tmp/datasets/train /tmp/datasets/valid /tmp/datasets/test

WORKDIR /stm32ai-modelzoo

COPY --chown=9001:9001 ./requirements.txt .
RUN pip install --user --requirement ./requirements.txt

COPY --chown=9001:9001 . .

ENV HOME=/home/stm32ai

ENTRYPOINT [ "/stm32ai-modelzoo/common/docker/train/train.entrypoint.py" ]
