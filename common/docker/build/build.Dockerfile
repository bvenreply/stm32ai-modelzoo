FROM python:3.10-bullseye as prepare

ARG cubeide_filename="en.st-stm32cubeide_1.14.0_19471_20231121_1200_amd64.deb_bundle.sh.zip"

RUN apt-get update

COPY ./common/docker/build/${cubeide_filename} /run/cubeide.zip
RUN cd /run && unzip cubeide.zip && LICENSE_ALREADY_ACCEPTED=1 sh /run/*cubeide*.sh
RUN rm /run/*cubeide*

FROM scratch as run

COPY --from=prepare / /

RUN useradd --create-home --user-group --uid 9001 --shell /bin/bash stm32ai
USER 9001:9001

RUN mkdir -p /tmp/inputs /tmp/outputs

WORKDIR /stm32ai-modelzoo
COPY --chown=9001:9001 ./requirements.txt .

RUN pip install --no-cache-dir --user --requirement ./requirements.txt colorama
COPY --chown=9001:9001 . .

ENV HOME=/home/stm32ai

ENTRYPOINT [ "/stm32ai-modelzoo/common/docker/build/build.entrypoint.py" ]
