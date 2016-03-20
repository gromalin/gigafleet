FROM debian:jessie

# Update aptitude with new repo
RUN apt-get update

# Install software 
RUN apt-get install -y git python3 locales python3-pip
RUN pip3     install Flask

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


#RUN git clone https://github.com/gromalin/gigafleet/

# Dealing with the locales
RUN echo 'fr_FR.UTF-8 UTF-8' >> /etc/locale.gen
RUN locale-gen --purge --no-archive
ENV LANG fr_FR.UTF8

COPY src src



CMD /usr/bin/python3 src/giga_fleet.py
