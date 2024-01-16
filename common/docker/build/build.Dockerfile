FROM python:3.10-bullseye

RUN apt-get update

COPY ./st-stm32cubeide_1.14.0_19471_20231121_1200_amd64.deb_bundle.sh /run/cubeide.sh
RUN LICENSE_ALREADY_ACCEPTED=1 sh /run/cubeide.sh
