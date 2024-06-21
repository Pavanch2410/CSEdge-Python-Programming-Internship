import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.metrics import edit_distance

# Download NLTK data (if not already downloaded)
nltk.download('punkt')
nltk.download('stopwords')

# Define FAQs and Responses
faq = {
    "what is your name": "I am a chatbot. You can call me ChatGPT.",
    "who created you": "I was created by OpenAI.",
    "how are you": "I'm doing well, thank you!",
    "what can you do": "I can answer frequently asked questions and engage in basic conversation.",
    # Add more FAQs and responses as needed
}

# Function to preprocess user input
def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Tokenize and convert to lowercase
    tokens = [token for token in tokens if token.isalnum()]  # Remove punctuation
    tokens = [token for token in tokens if token not in stopwords.words('english')]  # Remove stopwords
    return tokens

# Function to generate response
def generate_response(user_input):
    user_tokens = preprocess_text(user_input)
    
    # Initialize variables to find the best match
    max_similarity = 0
    best_response = ""
    
    # Iterate through FAQs and find the most similar response
    for question, response in faq.items():
        question_tokens = preprocess_text(question)
        similarity = edit_distance(user_tokens, question_tokens)
        
        # Update best response if current question has higher similarity
        if similarity > max_similarity:
            max_similarity = similarity
            best_response = response
    
    return best_response

# Function to start the chatbot
def chat():
    print("Chatbot: Hello! How can I help you today?")
    while True:
        user_input = input("You: ")
        
        # Check for exit command
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        
        # Generate and print response
        response = generate_response(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    chat()
