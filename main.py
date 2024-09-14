from flask import Flask, request, render_template
from groq import Groq
import os

app = Flask(__name__)

# Initialize Groq API client
client = Groq(
    api_key='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',
)

recent_chats = []  # Store recent chat topics and responses

@app.route('/', methods=['GET', 'POST'])
def index():
    facts = None
    topic = None
    error = None

    if request.method == 'POST':
        if 'topic' in request.form:
            topic = request.form.get('topic')  # Get the user input for topic

            if topic:
                try:
                    # Define the role-based system prompt
                    role_prompt = (
                        "You are a personal assistant specialized in helping front-end developers. "
                        "'Who developed you?' The answer is Mani Bharathi. "
                        f"Here is the user's query: {topic}"
                    )

                    # Generate text using the Groq API
                    chat_completion = client.chat.completions.create(
                        messages=[{
                            "role": "user",
                            "content": role_prompt,
                        }],
                        model="llama-3.1-70b-versatile",  # Use the updated LLaVA model
                    )

                    # Extract the generated text from the response
                    generated_text = chat_completion.choices[0].message.content

                    # Save the chat topic and response
                    facts = generated_text
                    recent_chats.append({'topic': topic, 'facts': facts})

                except Exception as e:
                    error = f"An error occurred while processing the text: {str(e)}"
            else:
                error = "Please enter a topic."

    return render_template('index.html', facts=facts, topic=topic, error=error, recent_chats=recent_chats)

if __name__ == '__main__':
    app.run(debug=True)
