from flask import Flask, request, jsonify, render_template
import PyPDF2
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import re
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from dateutil import parser

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Global variable to track model readiness
model_ready = False

# QA list
qa_list = {
    "greetings": {
        "questions": ["hello", "hey", "hi", "greetings", "good morning", "good afternoon", "good evening"],
        "answer": "Hello! How can I assist you today?"
    },
    "president_of_kenya": {
        "questions": ["who is the president of kenya", "president of kenya", "kenya's president"],
        "answer": "William Ruto is the President of Kenya."
    },
    "finance_bill_taxes": {
        "questions": [
            "which taxes were introduced in the finance bill",
            "which tax measures did the bill propose",
            "which taxes did the bill introduce",
            "taxes introduced in the finance bill",
            "taxes in the finance bill",
            "what are the new taxes in the finance bill",
            "finance bill tax changes",
            "measures proposed in the Finance Bill to raise taxes",
            "tax increases in the finance bill"
        ],
        "answer": """The finance bill proposed several measures to raise taxes, which would increase the cost of living:
* Eco Levy: Introduced on imported environmentally harmful products like sanitary towels, diapers, motorcycles, tires, plastic packaging, and electronic equipment.
* 16% VAT: Applied to ordinary bread, sugarcane transportation, locally assembled mobile phones, electric bikes, solar and lithium-ion batteries, and electric buses, changing their tax status from exempt to standard.
* Excise Duty Calculation: Adjusted for alcoholic beverages, cigarettes, and tobacco products, potentially increasing taxes on these items by up to 40% or higher for stronger alcoholic drinks.
* 25% Excise Duty: Imposed on vegetable and seed oils; 5% duty or KES 27,000 per ton on coal, whichever is higher.
* Road Maintenance Levy: Increased from KES 18 to KES 25 per liter of fuel, raising fuel prices.
* 20% Excise Duty: Applied to financial services transactions, telephone and internet services, lottery, betting, gaming, and internet/social media advertisements.
* Motor Vehicle Tax: Introduced a 2.5% tax with a minimum of KES 5,000, later amended to remove the maximum limit of KES 100,000."""
    },
    "abducted_people": {
        "questions": [
            "names of people abducted by rogue police",
            "list of people abducted",
            "who were abducted by rogue police"
        ],
        "answer": """List of the People Abducted:
1. Billy Simani, also known by his Twitter name crazyNairobian.
2. Shad Khalif was abducted in South C outside a club.
3. Kevin Monari, known by his Twitter handle Osama Otero.
4. Macharia Gaith was allegedly abducted due to a mistaken identity.
5. Gabriel Oguda, a vocal social media and political activist.
6. Kasamuel McOure, a Kenyan activist.
7. Joshua Okayo, a KSL student.
8. Alfred Keter, former Nandi Hills Member of Parliament.
9. Leslie Muturi, son of Attorney General Justin Muturi.
10. Dr. Austin Omondi, also known as Ja Prado.
11. George Towett Diano, a human rights activist and farmer in Trans-Nzoia County.
Other people include John Frank Ngemi, Ray Mwangi, Nyerere Earnest, Kevin Munari, Harriet Nyongesa, Zadock Machaveli, Drey Mwangi, TemperCR7, Harriet, Shad, Franje, Worldsmith, and Hilla254."""
    },
    "Inspector general of police": {
        "questions": ["who is the Inspector of general of police", "Inspector general of police", "head of police", "who is the inspector-general of police"],
        "answer": "Douglas Kanja was appointed as the Inspector general of police after the resignation of Japheth Koome amid outcry by protestors and Kenyans over police brutality."
    },
    "finance_bill_protests_timeline": {
        "questions": [
            "timeline of events for the kenyan protests",
            "timeline of protests",
            "summary of events of the protests",
            "sequence of date protests",
            "how did the #RejectFinanceBill2024 protests unfold"
        ],
        "answer": """The #RejectFinanceBill2024 protests began in May 2024 and unfolded as follows:

May 2024
* 13 May to 18 June: The #RejectFinanceBill2024 movement starts on TikTok, spreading to X, Instagram, and WhatsApp. Activists share phone numbers of parliamentarians to pressure them to reject the bill. Calls for a demonstration on 18 June are widely circulated online.

June 2024
* 18 June: The first day of protests sees hundreds in Nairobi demonstrating peacefully against the bill. Police use tear gas; 210 people are arrested. Despite violence, no deaths are reported. Protesters publish personal information of police officers.
* 20 June: Protests continue in 19 counties as Parliament holds the second reading of the Finance Bill. Police use water cannons, tear gas, and allegedly live ammunition, resulting in over 200 injuries and two deaths. Protesters declare "7 days of rage" and call for a national strike on 25 June.
* 22 June: Protesters call for a nationwide strike. Music stops at midnight in bars and clubs, replaced by anti-bill chants.
* 23 June: President Ruto expresses willingness to engage in conversations with protesters. Catholic youths and bishops condemn the bill. Kenyan diaspora in Dallas protest.
* 24 June: Hundreds protest in Lamu County. Government allows planned protests for 25 June. Rights groups call for uninterrupted Internet.
* 25 June: Thousands break through police barricades and storm Parliament, resulting in 19 deaths and numerous injuries. Amnesty International reports police using live rounds. President Ruto denounces the protests, and the military is deployed.
* 26 June: President of the Kenya Medical Association reports 13 deaths. Deputy opposition leader Martha Karua and others condemn military deployment. Law Society of Kenya sues over military deployment. President Ruto announces he won't sign the Finance Bill and agrees with MPs to withdraw it.
* 27 June: Protests continue with demands for Ruto's resignation. Seven protesters are shot in Homa Bay.
* 28 June: The High Court prohibits police from using excessive force against protesters. President Ruto rejects the Finance Bill and signs the Appropriations Bill 2024 into law, cutting the budget by Sh346 billion.
* 29 June: Protesters carry the casket of Benson Kamau, killed during the storming of Parliament.

July 2024

* 1 July: Finance Minister emphasizes government's commitment to reduced spending. Protesters reject dialogue and announce fresh protests for 2 July.
* 2 July: Clashes in Nairobi and other cities as protesters demand Ruto's resignation. About 272 people are arrested.
* 5 July: President Ruto apologizes for police actions and announces austerity measures, including cuts to government spending and dissolution of state corporations.
* 7 July: A concert is held in Uhuru Park to commemorate those killed during the protests.
* 11 July: President Ruto dissolves his cabinet except for key positions.
* 12 July: Student protesters block a major highway over the discovery of a protester's remains. Inspector-General of Police Japheth Koome Nchebere resigns.
* 16 July: Protests in multiple cities lead to clashes with security forces. One person is killed, bringing the total number of deaths to at least 50.
* 17 July: Police impose an indefinite ban on protests in Nairobi's center.
* 18 July: The High Court lifts the ban on protests in Nairobi, citing the right to assembly."""
    },
}


def preprocess_question(question):
    stop_words = set(stopwords.words('english'))
    return [word.lower() for word in word_tokenize(question) if word.lower() not in stop_words]

def find_best_match(question, qa_list):
    best_match = None
    best_score = 0
    processed_question = preprocess_question(question)

    for key, qa in qa_list.items():
        for q in qa["questions"]:
            similarity = fuzz.ratio(question.lower(), q.lower())
            processed_q = preprocess_question(q)
            keyword_overlap = len(set(processed_question) & set(processed_q)) / len(set(processed_question) | set(processed_q))
            combined_score = 0.6 * similarity + 0.4 * keyword_overlap * 100

            if combined_score > best_score:
                best_score = combined_score
                best_match = key

    return best_match if best_score > 60 else None

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages])
    return text

def preprocess_text(text):
    text = text.replace('\n', ' ').replace('  ', ' ').strip()
    return text

# Load and preprocess the PDF
pdf_path = 'Gambi/delete.pdf'
text = extract_text_from_pdf(pdf_path)
text = preprocess_text(text)

# Load the model and tokenizer
model_name = "deepset/roberta-base-squad2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

def normalize_date(date_string):
    try:
        parsed_date = parser.parse(date_string)
        return parsed_date.strftime("%d %B")
    except ValueError:
        return date_string.lower()

def find_relevant_context(text, question):
    sentences = re.split('(?<=[.!?]) +', text)
    
    question_lower = question.lower()
    
    date_pattern = r'\b(\d{1,2})(?:st|nd|rd|th)?\s*(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b'
    date_match = re.search(date_pattern, question_lower)
    
    if date_match:
        normalized_question_date = normalize_date(date_match.group())
        
        relevant_sentences = []
        for sent in sentences:
            sent_date_match = re.search(date_pattern, sent.lower())
            if sent_date_match:
                normalized_sent_date = normalize_date(sent_date_match.group())
                if normalized_sent_date == normalized_question_date:
                    relevant_sentences.append(sent)
        
        if relevant_sentences:
            context = " ".join(relevant_sentences)
            return context
        else:
            return f"I don't have any information about events on {normalized_question_date}."
    
    keywords = [word for word in question_lower.split() if len(word) > 2]
    relevant_sentences = [
        sent for sent in sentences 
        if any(keyword in sent.lower() for keyword in keywords)
    ]
    
    if not relevant_sentences:
        return text
    
    context = " ".join(relevant_sentences)
    
    if len(context.split()) < 50:
        start_index = max(0, sentences.index(relevant_sentences[0]) - 2)
        end_index = min(len(sentences), sentences.index(relevant_sentences[-1]) + 3)
        context = " ".join(sentences[start_index:end_index])
    
    return context

def answer_question_with_model(question, context, tokenizer, model):
    inputs = tokenizer(question, context, return_tensors="pt", max_length=512, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    
    answer_start = outputs.start_logits.argmax()
    answer_end = outputs.end_logits.argmax()
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end+1]))
    
    if answer.strip() in ["", "<s>", "</s>"]:
        return None
    
    return answer

def find_keyword_answer(text, question):
    keywords = [word for word in question.lower().split() if len(word) > 2]
    sentences = re.split('(?<=[.!?]) +', text)
    
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in keywords):
            return sentence
    
    return "I'm sorry, I couldn't find a relevant answer to your question."

def answer_question(question):
    best_match = find_best_match(question, qa_list)
    if best_match:
        return qa_list[best_match]["answer"], "QA List"

    date_pattern = r'\b(\d{1,2})(?:st|nd|rd|th)?\s*(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b'
    if re.search(date_pattern, question.lower()):
        relevant_context = find_relevant_context(text, question)
        return relevant_context, "Date Context"

    relevant_context = find_relevant_context(text, question)
    model_answer = answer_question_with_model(question, relevant_context, tokenizer, model)
    if model_answer:
        return model_answer, "Model Answer"

    keyword_answer = find_keyword_answer(text, question)
    return keyword_answer, "Keyword Search"

@app.route('/')
def home():
    global model_ready
    model_ready = True
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data['question']
    
    answer, method = answer_question(question)
    
    return jsonify({
        'question': question,
        'answer': answer,
        'method': method
    })

@app.route('/model_status', methods=['GET'])
def check_model_status():
    question = "why did the people protest?"
    answer, _ = answer_question(question)
    if "tax increases" in answer.lower():
        return jsonify({'status': 'ready', 'answer': answer})
    else:
        return jsonify({'status': 'not_ready'})

if __name__ == '__main__':
    app.run(debug=True)