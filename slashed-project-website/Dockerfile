# Build stage
FROM node:20 as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install -g npm@latest # Ensure npm is up to date
RUN npm install -g @angular/cli # Install Angular CLI globally
RUN npm install # Install project dependencies
COPY . .
RUN ls -la /app/slashed-project/slashed-project-website/src/environments
RUN npm run build -- --configuration production


# Serve stage
FROM nginx:stable
COPY --from=build-stage /app/dist/slashed-project /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/nginx.conf