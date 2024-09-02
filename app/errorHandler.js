

/**
 * Handles HTTP errors based on the status code.
 * 
 * @param {number} status - The HTTP status code received from the API response.
 * @throws {Error} - Throws an error with a specific message based on the status code.
 */
export function handleHttpErrors(status) {
    // Switch-case to handle different HTTP status codes
    switch (status) {
        case 400:
            throw new Error('Bad Request: Please check the information you provided.');
        case 401:
            throw new Error('Unauthorized: Please log in and try again.');
        case 403:
            throw new Error('Forbidden: You do not have permission to access this resource.');
        case 404:
            throw new Error('Not Found: No matching results were found. Please try a different search.');
        case 429:
            throw new Error('Too Many Requests: Please wait a moment before trying again.');
        case 500:
            throw new Error('Internal Server Error: Something went wrong on our end. Please try again later.');
        case 502:
            throw new Error('Bad Gateway: The server received an invalid response. Please try again later.');
        case 503:
            throw new Error('Service Unavailable: The server is currently unavailable. Please try again later.');
        case 504:
            throw new Error('Gateway Timeout: The server took too long to respond. Please try again later.');
        default:
            throw new Error(`Unexpected error: ${status}`);
    }
}

/**
 * Logs an error to the console and optionally to a remote logging service.
 * 
 * @param {Error} error - The error object to log.
 */
export function logError(error) {
    console.log('Logging error to the server:', error);

    // Example: Sending the error details to a logging endpoint
    // fetch('/log-error', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ error: error.message, stack: error.stack })
    // });
}
