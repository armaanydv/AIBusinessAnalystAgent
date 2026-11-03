# ==============================================================================
# AIBA FRONTEND DOCKERFILE
# Multi-stage production container: Node.js Vite Build -> Nginx Static Server
# ==============================================================================

# Stage 1: Build React Application
FROM node:20-alpine AS build

WORKDIR /app

# Copy package manifests
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci || npm install

# Copy application source code
COPY . .

# Build production bundle
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Remove default nginx config and copy custom SPA config
RUN rm -rf /etc/nginx/conf.d/*
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy build artifacts from Stage 1
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
