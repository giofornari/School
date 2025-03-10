FROM node:18-alpine

# Create app directory
WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY index.js .

EXPOSE 3000

# Switch to low privileged user
USER node

CMD [ "node", "index.js" ]