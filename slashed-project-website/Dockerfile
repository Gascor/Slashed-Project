# Build stage with a specific version and less privileged base image
FROM node:20-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install -g npm@latest && \
    npm install -g @angular/cli && \
    npm install && \
    npm cache clean --force
COPY . .
ENV NODE_OPTIONS=--openssl-legacy-provider
RUN npm run build -- --configuration production

# Serve stage
FROM nginx:stable-alpine
COPY --from=build-stage /app/dist/slashed-project /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/nginx.conf
RUN chmod -R 755 /usr/share/nginx/html && \
    chown -R nginx:nginx /usr/share/nginx/html