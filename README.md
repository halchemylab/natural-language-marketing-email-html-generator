# Natural Language Marketing Email HTML Generator

This Streamlit application generates HTML and plain text marketing emails from a messy webinar brief.

## How to Use

1.  **Set up your environment:**
    *   Create a `.env` file in the root of the project and add your OpenAI API key:
        ```
        OPENAI_API_KEY="your-api-key"
        ```
    *   Install the required dependencies:
        ```
        pip install -r requirements.txt
        ```

2.  **Run the application:**
    ```
    streamlit run app.py
    ```

3.  **Generate emails:**
    *   Paste your webinar brief into the text area.
    *   Click the "Generate Emails" button.
    *   The application will generate an HTML and a plain text email based on your input.

## Features

*   **Extracts key information:** The application uses OpenAI's structured outputs to extract the title, subtitle, intro, overview, and speaker information from your webinar brief.
*   **Generates HTML and plain text emails:** It creates both an HTML and a plain text version of your marketing email.
*   **Persists ROI metrics:** The application tracks the number of runs, time saved, and money saved, and persists these metrics in a `run_log.csv` file.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
