FROM node:16-alpine

ENV LANG C.UTF-8
WORKDIR /wscrcpy

RUN apk update && \
    apk add --no-cache android-tools git build-base && \
    npm install -g node-gyp && \
    git clone https://github.com/NetrisTV/ws-scrcpy.git . && \
    npm install && \
    npm run dist && \
    apk del git build-base

EXPOSE 8000

CMD ["node", "dist/index.js"]
