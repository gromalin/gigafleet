FROM debian:jessie

# Update aptitude with new repo
RUN apt-get update

# Install software 
RUN apt-get install -y git python3 locales

RUN git clone https://github.com/gromalin/gigafleet/

# Dealing with the locales
RUN echo 'fr_FR.UTF-8 UTF-8' >> /etc/locale.gen
RUN locale-gen --purge --no-archive
ENV LANG fr_FR.UTF8

CMD python3 gigafleet/src/giga_fleet.py
