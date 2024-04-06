
# Resume Customizer

Resume Customizer is a Django-based application designed to help professionals tailor their resumes and cover letters for specific job applications. Utilizing the power of Google's Gemini API, it intelligently selects relevant skills, projects, and other professional details based on the job description (JD) and company name provided by the user. This tool aims to enhance job application efforts by generating highly customized resumes and cover letters that stand out.

## Features

- **Profile Creation**: Users can create profiles to input their comprehensive professional details, including Education, Work Experience, Technical Skills, Projects, Awards, and Certifications.
- **Customization Engine**: Enter the target company name and job description. Our tool uses Google's Gemini API to analyze and select the most relevant professional details for customization.
- **Resume and Cover Letter Generation**: With the click of a button, generate, customize, view, and download your tailored resume and cover letter.

## Built With

- **[Django](https://www.djangoproject.com/)** - The web framework used for backend development.
- **[Tailwind CSS](https://tailwindcss.com/)** - A utility-first CSS framework for styled components.
- **[Google's Gemini API](https://developers.google.com/)** - Leveraged for AI-driven content customization.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- pip
- Virtualenv (optional but recommended)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourgithubusername/resume-customizer.git
cd resume-customizer
```

2. **Setup a virtual environment (Optional)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Environment Variables**

Create a `.env` file in the project root directory and add your Google Gemini API key:

```plaintext
GEMINI_API_KEY=your_api_key_here
```

5. **Run the application**

```bash
python manage.py runserver
```

The application should now be running on [http://localhost:8000](http://localhost:8000).

## API Usage

The Resume Customizer provides an API endpoint to interact with Google's Gemini AI. You can use this endpoint to submit questions and receive responses as part of the resume customization process.

### Endpoint

`POST /chatgeminiapi/`

### Request Format

To ask a question, send a JSON POST request to the endpoint with the following format:

```json
{
  "question": "Your question here"
}
```

### Response Format

The API will return a JSON response with the answer. Here is the format of a successful response:

```json
{
  "answer": "Response from Gemini AI"
}
```

In case of an error, the API will return a JSON response with an error message, like so:

```json
{
  "error": "Description of the error"
}
```

### Example

Using a tool like Postman, you can send a POST request to `http://127.0.0.1:8000/chatgeminiapi/` with the question in the body. Set the `Content-Type` header to `application/json` and include your question in the body as shown in the request format.

### Security

Please ensure that your API key is kept confidential. Do not expose it in client-side code or public repositories.

## Usage

1. **Create Your Profile**: Navigate to the profile creation page and fill in your professional details.
2. **Customize Your Resume/Cover Letter**: Enter the company name and job description for which you are applying, and click "Generate" to customize your resume and cover letter accordingly.
3. **Download**: View the customized versions and download them directly from the site.

## Contributing

We welcome contributions! Please feel free to fork the repository and submit pull requests with any enhancements, bug fixes, or suggestions.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

## Acknowledgement

- Meri berojgari
- Moti❤️