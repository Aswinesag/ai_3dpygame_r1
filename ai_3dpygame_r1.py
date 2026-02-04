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
            import base64
            
            try:
                # Create a simple HTML page with the code
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>PyGame Code - Ready to Paste</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                        .code-block {{ background: #f4f4f4; padding: 15px; border-radius: 5px; white-space: pre-wrap; font-family: 'Courier New', monospace; font-size: 14px; max-height: 400px; overflow-y: auto; }}
                        .instructions {{ background: #e7f3ff; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #007cba; }}
                        .button {{ background: #007cba; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; margin: 10px 5px; text-decoration: none; display: inline-block; }}
                        .button:hover {{ background: #005a8b; }}
                        .header {{ text-align: center; color: #333; margin-bottom: 30px; }}
                        .copy-btn {{ background: #28a745; }}
                        .copy-btn:hover {{ background: #218838; }}
                        .success {{ background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; border: 1px solid #c3e6cb; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>🎮 PyGame Code Generated!</h1>
                            <p>Your AI-generated PyGame code is ready to run</p>
                        </div>
                        
                        <div class="success">
                            ✅ Code successfully generated by Groq + OpenAI
                        </div>
                        
                        <div class="instructions">
                            <h3>📋 Quick Instructions:</h3>
                            <ol>
                                <li><strong>Click the button below</strong> to open Trinket PyGame editor</li>
                                <li><strong>Copy the code</strong> from the green box below (click "Copy Code")</li>
                                <li><strong>Paste it</strong> into the Trinket editor</li>
                                <li><strong>Click Run</strong> (▶) to execute your PyGame!</li>
                            </ol>
                            
                            <div style="text-align: center; margin: 20px 0;">
                                <a href="https://trinket.io/features/pygame" target="_blank" class="button">🚀 Open Trinket PyGame Editor</a>
                                <button onclick="copyCode()" class="button copy-btn">📋 Copy Code</button>
                            </div>
                        </div>
                        
                        <h3>🐍 Your PyGame Code:</h3>
                        <div class="code-block" id="codeBlock">{code}</div>
                        
                        <div style="text-align: center; margin-top: 20px;">
                            <small>💡 Tip: Keep this page open while you work in Trinket for easy reference</small>
                        </div>
                    </div>
                    
                    <script>
                        function copyCode() {{
                            const codeBlock = document.getElementById('codeBlock');
                            const textArea = document.createElement('textarea');
                            textArea.value = codeBlock.textContent;
                            document.body.appendChild(textArea);
                            textArea.select();
                            document.execCommand('copy');
                            document.body.removeChild(textArea);
                            
                            // Show feedback
                            const btn = event.target;
                            const originalText = btn.textContent;
                            btn.textContent = '✅ Copied!';
                            btn.style.background = '#218838';
                            setTimeout(() => {{
                                btn.textContent = originalText;
                                btn.style.background = '#28a745';
                            }}, 2000);
                        }}
                        
                        // Auto-open Trinket after 2 seconds
                        setTimeout(() => {{
                            window.open('https://trinket.io/features/pygame', '_blank');
                        }}, 2000);
                    </script>
                </body>
                </html>
                """
                
                # Create a data URL for the HTML content
                html_bytes = html_content.encode('utf-8')
                html_base64 = base64.b64encode(html_bytes).decode('utf-8')
                data_url = f"data:text/html;base64,{html_base64}"
                
                # Show success message in Streamlit
                st.success("✅ Code visualization page created!")
                st.info("📝 A new page will open with your code and Trinket editor. If it doesn't open automatically, use the links below.")
                
                # Provide direct links in Streamlit
                st.markdown("### 🚀 Quick Links:")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🎮 Open Trinket PyGame Editor", key="trinket_btn"):
                        webbrowser.open('https://trinket.io/features/pygame')
                
                with col2:
                    if st.button("📄 Open Code Page", key="code_btn"):
                        webbrowser.open(data_url)
                
                # Show the code in the app as well
                with st.expander("🐍 Generated PyGame Code", expanded=True):
                    st.code(code, language="python")
                    
                # Additional instructions
                with st.expander("📖 Detailed Instructions", expanded=False):
                    st.markdown("""
                    ### Step-by-Step Guide:
                    
                    1. **Open Trinket Editor**: Click the button above or go to [trinket.io/features/pygame](https://trinket.io/features/pygame)
                    
                    2. **Copy Your Code**: 
                       - Click "Copy Code" button on the generated page
                       - Or manually copy from the code box below
                    
                    3. **Paste in Trinket**:
                       - Delete any existing code in the Trinket editor
                       - Paste your generated PyGame code
                    
                    4. **Run Your Game**:
                       - Click the Run button (▶) in Trinket
                       - Your PyGame visualization should start immediately
                    
                    ### Troubleshooting:
                    - If the browser doesn't open automatically, use the manual buttons above
                    - Make sure to copy the entire code block
                    - Check for any syntax errors in the Trinket editor
                    """)
                    
            except Exception as e:
                st.error(f"Error creating visualization: {str(e)}")
                st.info("You can manually go to https://trinket.io/features/pygame and paste the code below:")
                st.code(code, language="python")

        # Run the async function with the stored code
        asyncio.run(run_pygame_on_trinket(st.session_state.generated_code))

elif generate_code_btn and not query:
    st.warning("Please enter a query before generating code")