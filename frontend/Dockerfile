FROM node:18

WORKDIR /app

COPY package.json ./

RUN npm install

# Optionnel pour test
RUN npm install -g vite

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
