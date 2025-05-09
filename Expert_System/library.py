import gradio as gr
from nltk.chat.util import Chat, reflections

books = {
    'fiction': ["The Alchemist", "1984", "The Great Gatsby"],
    'non-fiction': ["Sapiens", "Atomic Habits", "Educated"],
    'academic': ["Engineering Mathematics", "Human Anatomy", "Principles of Management"]
}

patterns = [
    (r'hi|hello|hey', [
        'Hello! Welcome to BookWorld 📚. How can I assist you today?',
        'Hey there! Need help with books or orders?',
        'Hi! Looking for something to read?']),
    (r'how are you', [
        "I'm just a bot, but I'm here to help you find the perfect book!"]),
    (r'(.*)book(.*)', [
        'We have fiction, non-fiction, and academic books. What are you looking for?']),
    (r'(.*)fiction(.*)', [
        f"Our fiction section includes: {', '.join(books['fiction'])}. Would you like to buy one?"]),
    (r'(.*)non[- ]fiction(.*)', [
        f"Our non-fiction books include: {', '.join(books['non-fiction'])}. Would you like to buy one?"]),
    (r'(.*)academic(.*)', [
        f"Our academic books include: {', '.join(books['academic'])}. Interested in purchasing?"]),
    (r'(.*)price(.*)|(.*)cost(.*)', [
        'Most books range from ₹200 to ₹1500 depending on the category and author.']),
    (r'(.*)buy(.*)|(.*)order(.*)', [
        "Great! Let’s proceed with your order. Type 'start order' to begin."]),
    (r'(.*)help(.*)', [
        'I can assist you with book categories, prices, and placing orders.']),
    (r'(.*)contact(.*)', [
        'You can email us at support@bookworld.com or call 1800-BOOK-123.']),
    (r'(.*)bye|goodbye|exit', [
        'Thank you for visiting BookWorld! 📖 Goodbye!']),
    (r'(yes|yeah|yep)', [
        "Great! Let's proceed with your order. Type 'start order' to begin."]),
]

chatbot = Chat(patterns, reflections)
session = {"order_mode": False, "step": 0}

def step_0(message):
    if message not in books:
        return "Category not found 404"
    session["step"] = 1
    return f"You selected {message} category. We have {', '.join(books[message])} books for this category. Which one would you like to buy? You can also type 'nothing' if you would like to exit"

def step_1(message):
    if message == 'nothing':
        session["order_mode"] = False
        session["step"] = 0
        return "Thank you for chatting"
    session["step"] = 2
    return f"{message} added to cart. Cost is Rs.500. Should I confirm the order? (yes/no)"

def step_2(message):
    session["order_mode"] = False
    session["step"] = 0
    return "Order confirmed. Will reach soon." if message == 'yes' else "No worries! Come back later."

step_functions = {
    0: step_0,
    1: step_1,
    2: step_2
}

def respond(message, history):
    message = message.strip().lower()

    if session["order_mode"]:
        return step_functions[session["step"]](message)

    if "start order" in message or r"(.*)start(.*)":
        session["order_mode"] = True
        session["step"] = 0
        return "Ok let's start. Which category book (fiction/non-fiction/academic)?"
    
    reply = chatbot.respond(message)
    return reply if reply else "Sorry. I love you."

demo = gr.ChatInterface(
    fn=respond,
    title="📚 BookWorld Chatbot",
    description="Ask me about books, prices, or place an order!",
    theme="soft"
)

demo.launch()
