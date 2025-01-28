# Build stage
FROM node:16 as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install -g npm@latest # Ensuring npm is up to date
RUN npm install
COPY . .
RUN npm run build --configuration production

# Serve stage
FROM nginx:stable
COPY --from=build-stage /app/dist/slashed-project-website /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/nginx.conf
