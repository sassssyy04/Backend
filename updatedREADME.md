# FastAPI Backend Architecture

This repository contains the backend implementation of a document query system using FastAPI. The backend serves as an API endpoint to upload documents, embed them using Qdrant, and query them based on user-provided questions using Together AI API with Llama Index integration.

## Architecture Overview

The backend architecture is designed to efficiently handle document uploads, embedding, and user queries. Here's a breakdown of the key components and workflow:


### Endpoint Routes

- **`GET /`**: This route serves as a health check for the server, indicating that the server is running.
- **`POST /predict`**: The primary endpoint for uploading documents and querying them based on user-provided questions. Upon receiving a request, the backend follows a multi-step process:

    1. **File Upload**: The uploaded document is saved to a specified directory on the server.
    2. **Document Embedding**: The uploaded document is embedded using Qdrant, a high-performance vector database, to convert the document into a numerical representation suitable for similarity comparison.
    3. **User Query Processing**: The user-provided question is processed using Together AI API, leveraging Llama Index integration. This likely involves passing the embedded document and the question to the API and receiving a relevant response.
    4. **Response**: The backend returns the predicted result/response to the user query.
    5. **Deletion of files**: Upon generating the response, we check if the file is different from existing one, if yes, it deletes the old db and directory and updates with this single file to improve accuracy and avoide hallucinating. 

### Qdrant Integration

Qdrant is utilized to embed the uploaded documents, allowing for efficient similarity comparison and retrieval based on user queries. The embedded documents are stored in the Qdrant database for future reference.

### Together AI API with Llama Index Integration

Together AI API, integrated with Llama Index, facilitates query processing and answer generation using llama-2 70b chat model. 

### Environment Configuration

Together AI API key.


# React Frontend for Document Query System

This repository contains the frontend implementation of a document query system using React. The frontend provides a user interface for uploading documents and asking questions related to them.

## Architecture Overview

The frontend architecture is built using React, a popular JavaScript library for building user interfaces. Here's a breakdown of the key components and workflow:

### Components

- **App Component**: The main component responsible for rendering the entire application UI.
- **DialogPopup Component**: A reusable component for displaying notification messages.

### State Management

The frontend utilizes React Hooks, such as `useState`, to manage component state efficiently. State variables are used to store the uploaded file, user-provided question, API response, and notification status.

### User Interaction

The user interacts with the frontend by:
- Entering a question in the input field.
- Uploading a document using the file input field.
- Clicking the submit button to send the question and uploaded document to the backend for processing.

### API Integration

Upon form submission, the frontend sends a POST request to the backend API endpoint (`/predict`) with the uploaded file and user-provided question. The API call is made using the `fetch` API provided by modern web browsers.

### Error Handling

The frontend includes basic error handling to check for required fields before submitting the form. Additionally, it catches and logs any errors that occur during API requests.


## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
