from google.cloud import dialogflow


def detect_intent(
    project_id: str,
    session_id: str,
    text: str,
    language_code: str = 'ru',
) -> tuple[str, bool]:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )
    query_result = response.query_result
    return response.query_result.fulfillment_text, query_result.intent.is_fallback