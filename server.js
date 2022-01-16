import express from 'express';
import { resolve } from 'path';

const server = express();
const workDir = resolve() + '/docs';
const port = process.env.PORT ?? 8080;

server.use(express.static(workDir));
server.get('/', (_, res) => res.sendFile(`${workDir}/index.html`));
server.listen(port);

console.log(`http://localhost:${port}`);