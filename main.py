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
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are a financial analyst. Summarize the key points of this earnings call transcript."},
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
                 "content": "You are a financial analyst. Summarize the key points from this Q&A session of an earnings call."},
                {"role": "user", "content": qa_section[0]}
            ]
        )
        return response.choices[0].message.content
    else:
        return "No Q&A session found in the transcript."

# Self-analyzed functions
def get_financial_results(text):
    financial_results = re.findall(r'Revenue.*?[\d.]+\s*billion', text, re.IGNORECASE | re.DOTALL)
    financial_results += re.findall(r'Net income.*?[\d.]+\s*billion', text, re.IGNORECASE | re.DOTALL)
    financial_results += re.findall(r'EPS.*?[\d.]+', text, re.IGNORECASE)
    return financial_results

def get_strategic_initiatives(text):
    initiatives = re.findall(r'strategic.*?\.', text, re.IGNORECASE | re.DOTALL)
    return initiatives

def get_performance_analysis(text):
    analysis = re.findall(r'performance.*?\.', text, re.IGNORECASE | re.DOTALL)
    return analysis

def get_operational_updates(text):
    updates = re.findall(r'operational.*?\.', text, re.IGNORECASE | re.DOTALL)
    return updates

def get_capital_allocation(text):
    allocation = re.findall(r'capital.*?\.', text, re.IGNORECASE | re.DOTALL)
    allocation += re.findall(r'dividend.*?\.', text, re.IGNORECASE | re.DOTALL)
    return allocation

def get_risks_and_problems(text):
    risks = re.findall(r'risk.*?\.', text, re.IGNORECASE | re.DOTALL)
    risks += re.findall(r'challenge.*?\.', text, re.IGNORECASE | re.DOTALL)
    return risks

def get_sustainability(text):
    sustainability = re.findall(r'sustainability.*?\.', text, re.IGNORECASE | re.DOTALL)
    sustainability += re.findall(r'ESG.*?\.', text, re.IGNORECASE | re.DOTALL)
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