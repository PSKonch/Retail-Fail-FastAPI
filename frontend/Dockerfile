# Используем официальный Node.js образ для билда
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

RUN npm run build

# Минимальный runtime для Next.js
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV production

# Копируем только необходимые файлы из build-стадии
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Если используешь .env.production — скопируй его!
# COPY .env.production .env.production

EXPOSE 3000

CMD ["npm", "start"]