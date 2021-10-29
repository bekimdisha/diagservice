FROM node:12-alpine

ARG APP_ENV=development
ENV NODE_ENV=${APP_ENV}

RUN apk upgrade && apk add git tar bash gawk
WORKDIR /usr/src/app
COPY . .
RUN npm install --unsafe-perm
COPY entrypoint_prod.sh /entrypoint_prod.sh
RUN chmod +x /entrypoint_prod.sh
EXPOSE 55555
ENTRYPOINT /entrypoint_prod.sh
