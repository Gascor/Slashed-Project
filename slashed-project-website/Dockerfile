# Build stage
FROM node:20
WORKDIR /app
COPY package*.json ./
RUN npm install -g npm@latest # Ensure npm is up to date
RUN npm install -g @angular/cli # Install Angular CLI globally
RUN npm install # Install project dependencies
COPY . .
ENV NODE_OPTIONS=--openssl-legacy-provider
RUN npm run build -- --configuration production
RUN ls -la /app/dist/slashed-project # List the contents of the build directory

# Serve stage
FROM nginx:stable
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf
RUN ls -la /usr/share/nginx/html # List the contents of the Nginx root directory