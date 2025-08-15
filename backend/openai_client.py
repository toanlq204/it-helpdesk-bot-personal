import openai
from mock_data import faq_data, software_list


def call_openai_api(user_message, conversation_history):
    openai.api_key = "your-azure-openai-key"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=conversation_history +
        [{"role": "user", "content": user_message}],
        functions=[
            {"name": "get_faq_answer", "parameters": {"question": "string"}},
            {"name": "create_ticket", "parameters": {"issue": "string"}},
            {"name": "get_software_info", "parameters": {"name": "string"}}
        ]
    )
    return response.choices[0].message.content
