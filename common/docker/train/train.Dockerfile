FROM python:3.10

RUN apt-get update

RUN useradd --create-home --user-group --uid 1115 --shell /bin/bash stm32ai

USER 1115:1115

RUN mkdir -p /tmp/inputs /tmp/outputs \
    /tmp/datasets/train /tmp/datasets/valid /tmp/datasets/test

WORKDIR /stm32ai-modelzoo

COPY --chown=1115:1115 . .

ENTRYPOINT [ "/stm32ai-modelzoo/common/docker/train/train.entrypoint.sh" ]
