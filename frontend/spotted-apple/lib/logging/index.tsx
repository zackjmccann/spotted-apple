import { pino } from 'pino';

// Pass the following to the logger or pipe
// the output to the CLI tool by including "| pino-pretty"
// in the run command
// {
//     transport: {
//         target: 'pino-pretty',
//     }
// }
const logger = pino()

if (process.env.NODE_ENV === 'development') {
    logger.level = 'trace'
}

export default logger;
