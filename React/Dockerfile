FROM node:latest


WORKDIR /app

COPY frontend/package*.json ./

RUN npm install

# Copiar el resto de los archivos del frontend
COPY frontend/ ./


RUN npm run build

CMD ["npm", "start"]
