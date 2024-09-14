import os
import re
import PyPDF2
from dotenv import load_dotenv
from openai import OpenAI

# openai api key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# read pdf
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# summarize earnings report using gpt-4o-mini
def summarize_earnings_report(text):
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system",
             "content": "You are a financial analyst. Summarize the key points of this earnings call transcript in two paragraphs."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

# summarize q&a sesh using gpt-4o-mini
def summarize_qa_session(text):
    qa_section = re.findall(r'Question-and-Answer Session.*', text, re.IGNORECASE | re.DOTALL)
    if qa_section:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system",
                 "content": "You are a financial analyst. Summarize the key points from this Q&A session of an earnings call in two paragraphs."},
                {"role": "user", "content": qa_section[0]}
            ]
        )
        return response.choices[0].message.content
    else:
        return "No Q&A session found in the transcript."


def get_financial_results(text):
    patterns = [
        r'Revenue.*?[\d.]+\s*(?:billion|million|B|M).*?(?<=\.)',
        r'Net income.*?[\d.]+\s*(?:billion|million|B|M).*?(?<=\.)',
        r'EPS.*?[\$]?[\d.]+.*?(?<=\.)',
        r'Operating income.*?[\d.]+\s*(?:billion|million|B|M).*?(?<=\.)',
        r'Gross margin.*?[\d.]+%.*?(?<=\.)'
    ]
    results = []
    positive_keywords = ['increase', 'growth', 'improvement', 'positive']
    negative_keywords = ['decrease', 'decline', 'drop', 'negative']
    positive_count = 0
    negative_count = 0

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            if any(word in match.lower() for word in positive_keywords):
                positive_count += 1
            elif any(word in match.lower() for word in negative_keywords):
                negative_count += 1
            results.append(match)

    if positive_count > negative_count:
        overall_sentiment = "Overall: Positive Analysis"
    elif negative_count > positive_count:
        overall_sentiment = "Overall: Negative Analysis"
    else:
        overall_sentiment = "Overall: Indifferent"

    results.append(overall_sentiment)
    return results

def get_strategic_initiatives(text):
    initiatives = re.findall(r'(?:strategic|initiative|plan).*?(?<=\.)', text, re.IGNORECASE | re.DOTALL)
    positive_keywords = ['success', 'growth', 'positive', 'improvement']
    negative_keywords = ['failure', 'decline', 'negative', 'problem']
    positive_count = 0
    negative_count = 0

    for item in initiatives:
        if any(word in item.lower() for word in positive_keywords):
            positive_count += 1
        elif any(word in item.lower() for word in negative_keywords):
            negative_count += 1

    if positive_count > negative_count:
        overall_sentiment = "Overall: Positive Analysis"
    elif negative_count > positive_count:
        overall_sentiment = "Overall: Negative Analysis"
    else:
        overall_sentiment = "Overall: Indifferent"

    initiatives.append(overall_sentiment)
    return initiatives

def get_performance_analysis(text):
    analysis = re.findall(r'(?:performance|growth|decline).*?(?<=\.)', text, re.IGNORECASE | re.DOTALL)
    positive_keywords = ['growth', 'increase', 'improvement', 'positive']
    negative_keywords = ['decline', 'decrease', 'drop', 'negative']
    positive_count = 0
    negative_count = 0

    for item in analysis:
        if any(word in item.lower() for word in positive_keywords):
            positive_count += 1
        elif any(word in item.lower() for word in negative_keywords):
            negative_count += 1

    if positive_count > negative_count:
        overall_sentiment = "Overall: Positive Analysis"
    elif negative_count > positive_count:
        overall_sentiment = "Overall: Negative Analysis"
    else:
        overall_sentiment = "Overall: Indifferent"

    analysis.append(overall_sentiment)
    return analysis

def get_operational_updates(text):
    updates = re.findall(r'(?:operational|operations|business).*?(?<=\.)', text, re.IGNORECASE | re.DOTALL)
    positive_keywords = ['growth', 'increase', 'improvement', 'positive']
    negative_keywords = ['decline', 'decrease', 'drop', 'negative']
    positive_count = 0
    negative_count = 0

    for item in updates:
        if any(word in item.lower() for word in positive_keywords):
            positive_count += 1
        elif any(word in item.lower() for word in negative_keywords):
            negative_count += 1

    if positive_count > negative_count:
        overall_sentiment = "Overall: Positive Analysis"
    elif negative_count > positive_count:
        overall_sentiment = "Overall: Negative Analysis"
    else:
        overall_sentiment = "Overall: Indifferent"

    updates.append(overall_sentiment)
    return updates

def get_capital_allocation(text):
    allocation = re.findall(r'(?:capital|dividend|buyback|investment).*?(?<=\.)', text, re.IGNORECASE | re.DOTALL)
    positive_keywords = ['increase', 'growth', 'positive', 'improvement']
    negative_keywords = ['decrease', 'decline', 'drop', 'negative']
    positive_count = 0
    negative_count = 0

    for item in allocation:
        if any(word in item.lower() for word in positive_keywords):
            positive_count += 1
        elif any(word in item.lower() for word in negative_keywords):
            negative_count += 1

    if positive_count > negative_count:
        overall_sentiment = "Overall: Positive Analysis"
    elif negative_count > positive_count:
        overall_sentiment = "Overall: Negative Analysis"
    else:
        overall_sentiment = "Overall: Indifferent"

    allocation.append(overall_sentiment)
    return allocation

def get_risks_and_problems(text):
    risks = re.findall(r'(?:risk|challenge|problem|issue).*?(?<=\.)', text, re.IGNORECASE | re.DOTALL)
    positive_keywords = ['mitigated', 'resolved', 'positive', 'improvement']
    negative_keywords = ['risk', 'challenge', 'problem', 'issue']
    positive_count = 0
    negative_count = 0

    for item in risks:
        if any(word in item.lower() for word in positive_keywords):
            positive_count += 1
        elif any(word in item.lower() for word in negative_keywords):
            negative_count += 1

    if positive_count > negative_count:
        overall_sentiment = "Overall: Positive Analysis"
    elif negative_count > positive_count:
        overall_sentiment = "Overall: Negative Analysis"
    else:
        overall_sentiment = "Overall: Indifferent"

    risks.append(overall_sentiment)
    return risks

def get_sustainability(text):
    sustainability = re.findall(r'(?:sustainability|ESG|environmental|social|governance).*?(?<=\.)', text, re.IGNORECASE | re.DOTALL)
    positive_keywords = ['improvement', 'positive', 'growth', 'increase']
    negative_keywords = ['decline', 'negative', 'problem', 'issue']
    positive_count = 0
    negative_count = 0

    for item in sustainability:
        if any(word in item.lower() for word in positive_keywords):
            positive_count += 1
        elif any(word in item.lower() for word in negative_keywords):
            negative_count += 1

    if positive_count > negative_count:
        overall_sentiment = "Overall: Positive Analysis"
    elif negative_count > positive_count:
        overall_sentiment = "Overall: Negative Analysis"
    else:
        overall_sentiment = "Overall: Indifferent"

    sustainability.append(overall_sentiment)
    return sustainability

def main():
    pdf_files = [f for f in os.listdir() if f.endswith('.pdf')]
    print("Available PDF files:")

    for i, file in enumerate(pdf_files):
        print(f"{i + 1}. {file}")

    choice = int(input("Enter the number of the PDF you want to analyze: ")) - 1
    pdf_path = pdf_files[choice]
    text = extract_text_from_pdf(pdf_path)

    while True:
        print("\nChoose an analysis option:")
        print("1. Summarize Earnings Report")
        print("2. Financial Results")
        print("3. Strategic Initiatives")
        print("4. Performance Analysis")
        print("5. Operational Updates")
        print("6. Capital Allocation and Dividends")
        print("7. Risks and Problems Faced")
        print("8. Sustainability Issues")
        print("9. Summarize Q&A Session")
        print("0. Quit")

        option = int(input("Enter your choice: "))

        if option == 0:
            break
        elif option == 1:
            print(summarize_earnings_report(text))
        elif option == 2:
            print("\n".join(get_financial_results(text)))
        elif option == 3:
            print("\n".join(get_strategic_initiatives(text)))
        elif option == 4:
            print("\n".join(get_performance_analysis(text)))
        elif option == 5:
            print("\n".join(get_operational_updates(text)))
        elif option == 6:
            print("\n".join(get_capital_allocation(text)))
        elif option == 7:
            print("\n".join(get_risks_and_problems(text)))
        elif option == 8:
            print("\n".join(get_sustainability(text)))
        elif option == 9:
            print(summarize_qa_session(text))
        else:
            print("Invalid option. Please try again!!")

if __name__ == "__main__":
    main()