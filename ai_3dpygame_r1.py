import streamlit as st
from openai import OpenAI
from agno.agent import Agent as AgnoAgent
from agno.run.agent import RunOutput
from agno.models.openai import OpenAIChat as AgnoOpenAIChat
from langchain_openai import ChatOpenAI 
import asyncio
from browser_use import Browser
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="PyGame Code Generator", layout="wide")

# Initialize session state
if "api_keys" not in st.session_state:
    st.session_state.api_keys = {
        "groq": "",
        "openai": ""
    }

# Streamlit sidebar for API keys
with st.sidebar:
    st.title("API Keys Configuration")
    st.session_state.api_keys["groq"] = st.text_input(
        "Groq API Key",
        type="password",
        value=st.session_state.api_keys["groq"]
    )
    st.session_state.api_keys["openai"] = st.text_input(
        "OpenAI API Key",
        type="password",
        value=st.session_state.api_keys["openai"]
    )
    
    st.markdown("---")
    st.info("""
    📝 How to use:
    1. Enter your API keys above
    2. Write your PyGame visualization query
    3. Click 'Generate Code' to get the code
    4. Click 'Generate Visualization' to:
       - Open Trinket.io PyGame editor
       - Copy and paste the generated code
       - Watch it run automatically
    """)

# Main UI
st.title("🎮 AI 3D Visualizer with Groq")
example_query = "Create a particle system simulation where 100 particles emit from the mouse position and respond to keyboard-controlled wind forces"
query = st.text_area(
    "Enter your PyGame query:",
    height=70,
    placeholder=f"e.g.: {example_query}"
)

# Split the buttons into columns
col1, col2 = st.columns(2)
generate_code_btn = col1.button("Generate Code")
generate_vis_btn = col2.button("Generate Visualization")

if generate_code_btn and query:
    if not st.session_state.api_keys["groq"] or not st.session_state.api_keys["openai"]:
        st.error("Please provide both API keys in the sidebar")
        st.stop()

    # Initialize Groq client
    from groq import Groq
    groq_client = Groq(
        api_key=st.session_state.api_keys["groq"]
    )

    system_prompt = """You are a Pygame and Python Expert that specializes in making games and visualisation through pygame and python programming. 
    During your reasoning and thinking, include clear, concise, and well-formatted Python code in your reasoning. 
    Always include explanations for the code you provide."""

    try:
        # Get reasoning from Groq
        with st.spinner("Generating solution..."):
            groq_response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                max_tokens=4000,
                temperature=0.1
            )

        reasoning_content = groq_response.choices[0].message.content
        print("\nGroq Reasoning:\n", reasoning_content)
        with st.expander("Groq's Reasoning"):      
            st.write(reasoning_content)

        # Initialize OpenAI agent
        openai_agent = AgnoAgent(
            model=AgnoOpenAIChat(
                id="gpt-4o",
                api_key=st.session_state.api_keys["openai"]
            ),
            debug_mode=True,
            markdown=True
        )

        # Extract code
        extraction_prompt = f"""Extract ONLY the Python code from the following content which is reasoning of a particular query to make a pygame script. 
        Return nothing but the raw code without any explanations, or markdown backticks:
        {reasoning_content}"""

        with st.spinner("Extracting code..."):
            code_response: RunOutput = openai_agent.run(extraction_prompt)
            extracted_code = code_response.content

        # Store the generated code in session state
        st.session_state.generated_code = extracted_code
        
        # Display the code
        with st.expander("Generated PyGame Code", expanded=True):      
            st.code(extracted_code, language="python")
            
        st.success("Code generated successfully! Click 'Generate Visualization' to run it.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

elif generate_vis_btn:
    if "generated_code" not in st.session_state:
        st.warning("Please generate code first before visualization")
    else:
        async def run_pygame_on_trinket(code: str) -> None:
            import webbrowser
            import urllib.parse
            import time
            
            try:
                # Create a simple HTML page with the code
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>PyGame Code - Ready to Paste</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 20px; }}
                        .code-block {{ background: #f4f4f4; padding: 15px; border-radius: 5px; white-space: pre-wrap; }}
                        .instructions {{ background: #e7f3ff; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                        button {{ background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }}
                    </style>
                </head>
                <body>
                    <h1>🎮 PyGame Code Generated!</h1>
                    <div class="instructions">
                        <h3>📋 Instructions:</h3>
                        <ol>
                            <li>Click the button below to open Trinket PyGame editor</li>
                            <li>Copy the code from the box below</li>
                            <li>Paste it into the Trinket editor</li>
                            <li>Click the Run button (▶) to execute</li>
                        </ol>
                        <button onclick="window.open('https://trinket.io/features/pygame', '_blank')">🚀 Open Trinket PyGame Editor</button>
                    </div>
                    <h3>🐍 Your PyGame Code:</h3>
                    <div class="code-block">{code}</div>
                </body>
                </html>
                """
                
                # Save HTML to temporary file
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                    f.write(html_content)
                    temp_file = f.name
                
                # Open the HTML file in browser
                webbrowser.open(f'file://{temp_file}')
                
                # Also open Trinket directly
                webbrowser.open('https://trinket.io/features/pygame')
                
                st.success("✅ Browser opened with your code!")
                st.info("📝 A new tab opened with your code and Trinket editor. Copy the code and paste it into Trinket to run.")
                
                # Also show the code in the app
                with st.expander("🐍 Generated PyGame Code", expanded=True):
                    st.code(code, language="python")
                    
            except Exception as e:
                st.error(f"Error opening browser: {str(e)}")
                st.info("You can manually go to https://trinket.io/features/pygame and paste the code below:")
                st.code(code, language="python")

        # Run the async function with the stored code
        asyncio.run(run_pygame_on_trinket(st.session_state.generated_code))

elif generate_code_btn and not query:
    st.warning("Please enter a query before generating code")