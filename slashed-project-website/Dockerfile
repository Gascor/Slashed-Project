# Etape de build
FROM node:14 as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build --prod

# Etape de serve
FROM nginx:stable
COPY --from=build-stage /app/dist/slashed-project-website /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/nginx.conf