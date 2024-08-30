FROM node:20
COPY ./ /kunstgraph/frontend
WORKDIR /kunstgraph/frontend
ENV API_BASE_URL="http://localhost:8000"
RUN npm install --save-exact
RUN npm run generate:client
RUN npm run build
CMD ["npm", "run", "start"]
