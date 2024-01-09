from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Replace with your OpenAI API key
openai.api_key = "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"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    system_msg = "Financial Advisor"
    category = request.form['category']
    user_message = request.form.get('message', '')
    # feedback = request.form['feedback']

    messages = [{"role": "system", "content": system_msg}]
    if category:
        messages.append({"role": "user", "content": category})
    if user_message:
        messages.append({"role": "user", "content": user_message})

    # if feedback:
    #     # Store feedback in a file, database, or any desired storage
    #     with open('feedback.txt', 'a') as feedback_file:
    #         feedback_file.write(f"User Feedback: {feedback}\n")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})

    return render_template('chat.html', messages=messages)

def get_initial_response(category):
    # Add logic here to determine the appropriate initial response
    if category == "RBI Policies":
        return "Welcome to RBI Policies! How can I assist you today?"
    elif category == "Indian Government Schemes/Policies":
        return "Exploring Government Schemes/Policies? Feel free to ask any questions."
    elif category == "Indian Government Sponsored Loans":
        return "Looking for information on Government Sponsored Loans? Ask away!"
    elif category == "Other Policies in India":
        return "Curious about Other Policies? Let me know what you're interested in."
    else:
        return "Welcome! How can I assist you today?"

@app.route('/dashboard')
def dashboard():
    # Retrieve feedback from the storage (e.g., a file)
    feedback = []
    with open('feedback.txt', 'r') as feedback_file:
        feedback = feedback_file.readlines()

    return render_template('dashboard.html', feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True)

