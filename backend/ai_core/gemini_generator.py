from google import genai
from backend.config import GEMINI_API_KEY


class GeminiDocumentGenerator:

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

        self.models = [
            "gemini-3.8-flash",
            "gemini-3.7-flash",
            "gemini-3.6-flash",
        ]

    def generate_document(self, document_type, parties, terms, date):

        prompt = f"""
You are a professional legal document drafting assistant.

Generate a well-structured {document_type} based only on
the information provided by the user.

Details:
- Parties: {parties}
- Terms: {terms}
- Effective Date: {date}

Requirements:
- Use a clear title.
- Use proper headings.
- Maintain a formal legal tone.
- Clearly separate clauses.
- Use numbered clauses where appropriate.
- Use bullet points where useful.
- Include the effective date.
- Include a signature section at the end.
- Do not invent important facts that were not provided.
- Return only the drafted document.
"""

        last_error = None

        for model_name in self.models:
            try:
                print(f"Trying model: {model_name}")

                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                if response and response.text:
                    return response.text

            except Exception as error:
                print(f"{model_name} failed: {error}")
                last_error = error

        return f"Error generating document: {last_error}"