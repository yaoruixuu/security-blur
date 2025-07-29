from google import genai
from google.genai import types


def summarize(prompt, project_id):
    client = genai.Client(
    vertexai=True, project=project_id , location='global'
    )

    model = "gemini-2.5-flash"
    response = client.models.generate_content(
    model=model,
    contents=[
        f'''You are a skilled military analyst. Summarize the key points from the following military document text in a clear and concise paragraph.

        Document Text: {prompt}

        Provide a brief summary focusing on the main events, findings, and any important observations.
        '''
    ],
    )

    token_count = client.models.count_tokens(model = model, contents = response.text)

    original_length = len(prompt.prompt)

    dictionary = {"original length": original_length, "token count": token_count,  "summary": response.text}
    return dictionary

