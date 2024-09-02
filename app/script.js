import { handleHttpErrors, logError } from './errorHandler.js';
// Base URL for the PoetryDB API
const BASE_URL = 'https://poetrydb.org';

/**
 * Asynchronous function to fetch poetry data based on user input.
 * It retrieves author and title from input fields, validates them,
 * constructs the appropriate API URL, fetches the data, and displays
 * the results or any error messages.
 */
async function fetchPoetry() {
    // Retrieve user input values from the DOM
    const author = document.getElementById('authorInput').value.trim();
    const title = document.getElementById('titleInput').value.trim();
    const outputDiv = document.getElementById('output'); // Div to display fetched poetry data
    const errorDiv = document.getElementById('errorMessage'); // Div to display error messages

    // Clear previous results and errors
    outputDiv.textContent = '';
    errorDiv.textContent = '';

    // Validate input fields
    const validationError = validateInput(author, title);
    if (validationError) {
        showError(validationError); // Show error if validation fails
        return;
    }

    // Indicate to the user that data is being fetched
    outputDiv.textContent = 'Fetching poetry data...';

    // Construct the API URL based on user input
    const url = createPoetryUrl(author, title);

    try {
        // Make the API request
        const response = await fetch(url);
        
        // Handle any HTTP errors (e.g., 404, 500)
        if (!response.ok) {
            handleHttpErrors(response.status);
        }

        // Parse the JSON data from the response
        const data = await response.json();

        // When no poem is found, the server returns an object with status code
        // instead of array therefore we do a 
        //speical check and return meaningful User Friendly error message
        if (data.status === 404) {
            showError('No poems found. Try searching with different criteria.');
            return;
        }

        // Check if the data is an array (as expected)
        if (!Array.isArray(data)) {
            throw new Error('Unexpected response format. Please try again later.');
        }

        // Handle case where no poems are found
        if (data.length === 0) {
            showError('No poems found. Try searching with different criteria.');
        } else {
            // Log the fetched data to the console for debugging purposes
            console.log('Poetry data fetched:', data);

            // Display the fetched poetry data in the outputDiv
            //Making sure if if any element like "title" is not available, 
            //we show meaningful info
            outputDiv.innerHTML = data.map(poem => `
                <h3>${poem.title || 'Unknown Title'}</h3>
                <pre>${poem.lines ? poem.lines.join('\n') : 'No content available'}</pre>
                <p><strong>Author:</strong> ${poem.author || 'Unknown Author'}</p>
            `).join('');
        }
    } catch (error) {
        // Log and handle any errors that occur during the fetch process
        console.error('Error:', error);
        logError(error);

        // Display appropriate error messages based on the error type
        if (error.message === 'Failed to fetch') {
            showError('We’re having trouble connecting to the server. Please check your internet connection and try again.');
        } else if (error.message.includes('Unexpected error:')) {
            showError(`There was an issue with the server (${error.message}). Please try again later.`);
        } else if (error.message.includes('Unexpected response format')) {
            showError('We received an unexpected response from the server. Please try again later.');
        } else {
            showError('An unexpected error occurred. Please try again later.');
        }
    }
}
//event listerner to call the function when button is clicked using id from HTML index file
document.getElementById('searchButton').addEventListener('click', fetchPoetry);

/**
 * Validates the user input for author and title fields.
 * 
 * @param {string} author - The author's name input by the user.
 * @param {string} title - The poem's title input by the user.
 * @returns {string|null} - Returns a validation error message, or null if inputs are valid.
 */
function validateInput(author, title) {
    // Regular expression to match invalid characters in the author name (only letters and spaces allowed)
    const invalidAuthorPattern = /[^a-zA-Z\s]/;
    // Regular expression to match invalid characters in the title (letters, numbers, and spaces allowed)
    const invalidTitlePattern = /[^a-zA-Z0-9\s]/;

    // Ensure at least one of author or title is provided
    if (!author && !title) {
        return 'Please enter either an author name, title, or both.';
    }

    // Validate the author name against the invalid character pattern
    if (author && invalidAuthorPattern.test(author)) {
        return 'Please enter a valid author name with letters and spaces only.';
    }

    // Validate the title against the invalid character pattern
    if (title && invalidTitlePattern.test(title)) {
        return 'Please enter a valid title with letters, numbers, and spaces only.';
    }

    // If all validations pass, return null
    return null;
}

/**
 * Constructs the appropriate API URL based on the author and/or title provided by the user.
 * 
 * @param {string} author - The author's name input by the user.
 * @param {string} title - The poem's title input by the user.
 * @returns {string} - The constructed API URL.
 */
function createPoetryUrl(author, title) {
    // Construct the URL based on the presence of author and title
    if (author && title) {
        return `${BASE_URL}/author,title/${author};${title}`;
    } else if (author) {
        return `${BASE_URL}/author/${author}`;
    } else if (title) {
        return `${BASE_URL}/title/${title}`;
    }
}
/**
 * Displays an error message to the user.
 * 
 * @param {string} message - The error message to display.
 */
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
}
