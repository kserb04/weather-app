FROM node:22.4-alpine
WORKDIR /home/app
COPY package.json .
COPY package-lock.json .
RUN npm install

COPY public public
COPY src src
