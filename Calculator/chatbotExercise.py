import gradio 
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def api_calling(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.2,
    )
    message = completions.choices[0].text
    return message
def message_and_history(input, history):
    
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = api_calling(inp)
    history.append((input, output))

    return history, history

context = [{'role':'system', 'content':"""
You are OrderBot, an automated service to collect orders for a pizza restaurant. 
You need to do the following first
1) You first greet the customer and tell them the menu
Then depending on their response you do one of the following:
a) collect the order making sure to ask for the size, toppings, and quantity of each item. Make sure to clarify all options, extras and sizes of pizza to uniquely identify that the item is on the menu
b) ask if it's a pickup or delivery. If it's a pickup, you ask for a name. If its pickup tell them our shop name and street address - make it up 
c) Once you have the entire order do the following: summarize the order for the customer and check for a final time if the customer wants to add anything else. 
d) Finally you tell the customer the total and if they agree you collect the payment. . 
You always respond in a short, clear and friendly style. \
The menu includes pepperoni pizza  12.95, 10.00, 7.00, cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75, fries 4.50, 3.50, greek salad 7.25 
Toppings: extra cheese 2.00, mushrooms 1.50 sausage 3.00, Canadian bacon 3.50, AI sauce 1.50, peppers 1.00 \
Drinks: coke 3.00, 2.00, 1.00, sprite 3.00, 2.00, 1.00, bottled water 5.00 
""" }] # accumulate messages




block = gradio.Blocks(theme=gradio.themes.Monochrome())
with block:
    gradio.Markdown("""<h1><center>ChatGPT 
    ChatBot with Gradio and OpenAI</center></h1>
    """)
    chatbot = gradio.Chatbot()
    # initialize textbox with 2 lines, label, and default text
    
    message = gradio.Textbox(lines=2, label="Enter your message here", value=context[0]["content"])
    state = gradio.State()
    submit = gradio.Button("SEND")
    submit.click(message_and_history, 
                 inputs=[message, state], 
                 outputs=[chatbot, state])
    #clear the message box on click
    message.clear_on_click = True
   
    
block.launch(debug = True, share = True)

