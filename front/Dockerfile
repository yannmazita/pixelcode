### First stage ###

FROM node:21-alpine as node-base

RUN adduser -h /home/appuser -D appuser

WORKDIR /application
RUN chown -R appuser:appuser /application


### Second stage ###

# Copy vite project files
FROM node-base as node-builder
COPY front/public /application/front/public
COPY front/src /application/front/src
COPY front/package.json front/postcss.config.js front/tailwind.config.js front/tsconfig.json \
    front/tsconfig.node.json front/vite.config.ts front/index.html \
    front/

################### This needs to be cleaned up
COPY .env.example /application/
################### This needs to be cleaned up

# Install dependencies, build application
WORKDIR /application/front
RUN mv ../.env.example ../.env && npm install && npm run build


### Final stage ###

FROM nginx:alpine as production-build
COPY front/nginx.conf /etc/nginx/nginx.conf
RUN rm -rf /usr/share/nginx/html/*
COPY --from=node-builder /application/front/dist /usr/share/nginx/html/front
EXPOSE 5173

CMD ["nginx", "-g", "daemon off;"]
