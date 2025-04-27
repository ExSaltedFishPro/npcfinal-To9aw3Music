FROM node:22

USER root
RUN apt update --allow-unauthenticated && \
    apt install -y --allow-unauthenticated nginx && \
    apt install -y --allow-unauthenticated python3 && \
    apt install -y --allow-unauthenticated python3-pip && \
    apt install -y --allow-unauthenticated npm && \
    apt clean
RUN apt-get install -y python3-flask
RUN apt-get install -y python3-jwt
RUN npm cache clean --force

WORKDIR /app
RUN npm install vite@6.2.4

RUN mkdir -p /app/templates
COPY ./templates/* /app/templates
RUN mkdir -p /app/vite
RUN mkdir -p /app/vite/public
COPY ./vite/public/* /app/vite/public
COPY ./vite/index.html /app/vite
RUN useradd -m app
RUN chown -R app:app /app
RUN chmod -R u+rwX /app

COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY run.sh .
RUN chmod +x run.sh
COPY app.py .
COPY rm_ds_store.py .
COPY copyflag.py .
COPY readFlag.c /readFlag.c
EXPOSE 80

USER app
RUN npm install vite@6.2.4
USER root
CMD ["/bin/bash", "run.sh"]