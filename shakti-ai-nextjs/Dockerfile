# Frontend Dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
# Copy only the intended manifest files (avoid package-new.json)
COPY package.json ./
COPY package-lock.json* ./
# Use npm install to avoid failing on out-of-sync lock files
RUN npm install

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN mkdir -p public
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
# Only copy the necessary artifacts
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./
COPY --from=builder /app/next.config.js ./
# Bring installed modules and prune dev dependencies for production runtime
COPY --from=builder /app/node_modules ./node_modules
RUN npm prune --omit=dev && npm cache clean --force
EXPOSE 3000
CMD ["npm", "start"]
