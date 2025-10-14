# Use official Node LTS
FROM node:20-alpine

WORKDIR /app

# Install deps first (allows better caching)
COPY package.json package-lock.json* .npmrc* ./
RUN npm ci || npm install

# Copy app files
COPY . .

# Expose port
ENV PORT=3000
EXPOSE 3000

# Start the server
CMD ["npm", "start"]
