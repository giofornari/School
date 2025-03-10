FROM node:18-alpine

# Create app directory
WORKDIR /usr/src/app

COPY src/package*.json ./

RUN npm install

COPY src/index.js .
COPY src/migrations/ ./migrations
COPY src/views/ ./views

EXPOSE 3000

RUN mkdir data && chown -R node:node data

# Switch to low privileged user
USER node

ENTRYPOINT [ "npm", "start" ]