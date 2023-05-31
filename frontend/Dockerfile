#FROM ubuntu:latest
#LABEL authors="ericryan"
#
#ENTRYPOINT ["top", "-b"]

# Use the official lightweight Node.js image
FROM node:16-alpine

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy the rest of the files
COPY . .

# Build the Vue.js app
RUN npm run build

# Expose port
EXPOSE 80
