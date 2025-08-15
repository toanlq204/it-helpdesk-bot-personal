from mock_data import faq_data, software_list, ticket_data


def get_faq_answer(question: str):
    for faq in faq_data:
        if question.lower() in faq["question"].lower():
            return faq["answer"]
    return "Sorry, I couldn't find an answer to your question."


def create_ticket(issue: str):
    ticket_id = len(ticket_data) + 1
    ticket_data.append({"id": ticket_id, "issue": issue})
    return f"Ticket #{ticket_id} created for issue: {issue}"


def get_software_info(name: str):
    for software in software_list:
        if name.lower() == software["name"].lower():
            return software
    return "Software not found."
