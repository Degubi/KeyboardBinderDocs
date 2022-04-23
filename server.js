import express from 'express';
import { resolve } from 'path';

const server = express();
const workDir = resolve() + '/docs';

server.use(express.static(workDir));
server.get('/', (_, res) => res.sendFile(`${workDir}/index.html`));
server.listen(process.env.PORT ?? 8080);