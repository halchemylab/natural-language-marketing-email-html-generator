import streamlit as st
import openai
import re
import json
import time
import base64
from typing import Dict, Any, List
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# --- MAIN APP ---

st.set_page_config(page_title="Webinar Email Generator", page_icon="📧", layout="wide")

# Initialize session state
if 'run_count' not in st.session_state:
    try:
        df = pd.read_csv("run_log.csv")
        if not df.empty:
            st.session_state.run_count = df["run_count"].iloc[0]
        else:
            st.session_state.run_count = 0
    except (FileNotFoundError, pd.errors.EmptyDataError):
        st.session_state.run_count = 0
    st.session_state.time_saved = st.session_state.run_count * 30
    st.session_state.money_saved = st.session_state.run_count * (30 / 60) * 40
    st.session_state.last_run_seconds = 0.0
    st.session_state.email1_html = ""
    st.session_state.email2_text = ""
    st.session_state.parsed_json = None
    st.session_state.api_key = os.getenv("OPENAI_API_KEY") or ""

# --- TEMPLATES & SCHEMA ---
def load_template(template_name: str) -> str:
    """Loads an HTML template from a file."""
    file_path = f"email_template_{template_name}.html"
    if template_name == "text":
        file_path = "email_template_text.txt"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Template file not found: {file_path}")
        return ""

EMAIL1_TEMPLATE = load_template("announcement")
EMAIL2_TEMPLATE = load_template("text")

# --- HTML RENDERING HELPERS ---

def to_br(text: str) -> str:
    """Converts newlines to <br> tags and escapes HTML."""
    if not text:
        return ""
    # Basic escape
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return text.replace('\n', '<br>\n')

def render_final_email(template_html: str, data: Dict[str, Any]) -> str:
    """
    Renders the final HTML by replacing placeholders in the rich template.
    """
    html = template_html
    overview = data.get('overview', {})

    # --- Replace simple text fields ---
    html = html.replace('{{intro}}', to_br(data.get('intro', '')))
    html = html.replace('{{title}}', to_br(data.get('title', '')))
    html = html.replace('{{subtitle}}', to_br(data.get('subtitle', '')))
    html = html.replace('{{place}}', overview.get('place', ''))
    html = html.replace('{{registration_deadline}}', overview.get('registration_deadline', ''))

    # --- Replace links ---
    if overview.get('link'):
        html = html.replace('{{link}}', overview['link'])

    # --- Replace date/time block ---
    datetime_parts = [
        f"&nbsp; &nbsp;日程： {overview.get('datetime_jp', '')}",
        f"&nbsp; &nbsp;時間：{overview.get('datetime_pt', '')}",
        overview.get('datetime_ct', ''),
        overview.get('datetime_et', '')
    ]
    datetime_str = '<br>\n'.join(filter(None, datetime_parts))
    html = html.replace('{{datetime}}', f'<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;">{datetime_str}</span></span>')

    # --- Replace speaker block ---
    speakers = data.get('speakers', [])
    if speakers:
        speaker_blocks = []
        for speaker in speakers:
            name = speaker.get('name', '')
            role = speaker.get('role', '')
            speaker_blocks.append(f"&nbsp; &nbsp;<strong>{to_br(name)}</strong><br>\n&nbsp; &nbsp;{to_br(role)}")
        speaker_html = '<br>\n<br>\n'.join(speaker_blocks)
        html = html.replace('{{speakers}}', f'<span style="font-size:14px;"><span style="font-family:Arial,Helvetica,sans-serif;">{speaker_html}</span></span>')

    # --- Replace notices block ---
    notices = overview.get('notices', [])
    if notices:
        notice_html = '\n'.join([f'<li><span style="font-family:Arial,Helvetica,sans-serif;"><span style="font-size:14px;">{to_br(item)}</span></span></li>' for item in notices])
        html = html.replace('{{notices}}', f'<ul>\n{notice_html}\n</ul>')
    
    return html

def render_final_email_text(template_text: str, data: Dict[str, Any]) -> str:
    """
    Renders the final text email by replacing placeholders in the text template.
    """
    text = template_text
    overview = data.get('overview', {})

    # --- Replace simple text fields ---
    text = text.replace('{{intro}}', data.get('intro', ''))
    text = text.replace('{{title}}', data.get('title', ''))
    text = text.replace('{{subtitle}}', data.get('subtitle', ''))
    text = text.replace('{{place}}', overview.get('place', ''))
    text = text.replace('{{registration_deadline}}', overview.get('registration_deadline', ''))

    # --- Replace links ---
    if overview.get('link'):
        text = text.replace('{{link}}', overview['link'])

    # --- Replace date/time block ---
    datetime_parts = [
        f"日程： {overview.get('datetime_jp', '')}",
        f"時間：{overview.get('datetime_pt', '')}",
        overview.get('datetime_ct', ''),
        overview.get('datetime_et', '')
    ]
    datetime_str = '\n'.join(filter(None, datetime_parts))
    text = text.replace('{{datetime}}', datetime_str)
    text = text.replace('{{datetime_jp}}', overview.get('datetime_jp', ''))

    # --- Replace speaker block ---
    speakers = data.get('speakers', [])
    if speakers:
        speaker_blocks = []
        for speaker in speakers:
            name = speaker.get('name', '')
            role = speaker.get('role', '')
            speaker_blocks.append(f"{name}\n{role}")
        speaker_html = '\n\n'.join(speaker_blocks)
        text = text.replace('{{speakers}}', speaker_html)

    # --- Replace notices block ---
    notices = overview.get('notices', [])
    if notices:
        notice_html = '\n'.join([f'・{item}' for item in notices])
        text = text.replace('{{notices}}', notice_html)
    
    return text

def create_download_button(html_content: str, filename: str, label: str):
    """Generates a download button for the given HTML content."""
    b64 = base64.b64encode(html_content.encode()).decode()
    return st.download_button(
        label=label,
        data=html_content,
        file_name=filename,
        mime='text/html',
    )

# --- CORE FUNCTIONS ---

def cheap_prune(raw_text: str) -> str:
    """
    Normalizes and prunes the raw text to reduce token count while preserving key info.
    """
    # 1. Normalize whitespace and bullets
    text = re.sub(r'[\u200b\u200c\u200d\ufeff\xa0]', ' ', raw_text)
    text = re.sub(r'[・◦●■]', '•', text)
    text = re.sub(r'[\t ]+', ' ', text)
    lines = text.split('\n')

    # 2. Remove very short lines or lines with only whitespace, but keep lines with keywords
    keywords = [
        '開催', '日時', '日本時間', 'PT', 'CT', 'ET', 'タイトル', '対象',
        '注意事項', '紹介文', '概要', '登壇者', '経歴', 'Zoom', '締切',
        '申し込み', 'URL', 'メール', 'agenda', 'speaker', 'topic', 'date', 'time'
    ]
    keyword_regex = re.compile('|'.join(keywords), re.IGNORECASE)

    pruned_lines = [
        line.strip() for line in lines
        if keyword_regex.search(line) or len(line.strip()) > 10
    ]

    # Collapse multiple blank lines
    collapsed_text = re.sub(r'\n{3,}', '\n\n', "\n".join(pruned_lines))

    return collapsed_text

def extract_with_openai(cleaned_text: str, api_key: str, model: str, temperature: float) -> Dict[str, Any]:
    """
    Uses OpenAI's JSON mode to extract structured data from the pruned text.
    """
    client = openai.OpenAI(api_key=api_key)

    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "The main title of the webinar. Should be concise."},
            "subtitle": {"type": "string", "description": "The subtitle of the webinar. Often follows the main title."},
            "intro": {"type": "string", "description": "A 1-2 paragraph introduction to the webinar's topic and purpose."},
            "overview": {
                "type": "object",
                "properties": {
                    "datetime_jp": {"type": "string", "description": "Date and time in Japan Standard Time (e.g., '2024年10月28日(月) 10:00～11:00')."},
                    "datetime_pt": {"type": "string", "description": "Date and time in Pacific Time (e.g., '18:00-19:00 PT')."},
                    "datetime_ct": {"type": "string", "description": "Date and time in Central Time (e.g., '20:00-21:00 CT')."},
                    "datetime_et": {"type": "string", "description": "Date and time in Eastern Time (e.g., '21:00-22:00 ET')."},
                    "place": {"type": "string", "description": "The location or platform (e.g., 'Online Webinar (Zoom)')."},
                    "registration_deadline": {"type": "string", "description": "The deadline for registration (e.g., '米国時間11月17日（月）18:00 PST'). If not present, return an empty string."},
                    "link": {"type": "string", "description": "The URL for registration or more details. If not present, return an empty string."},
                    "notices": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "A list of important notices for attendees."
                    }
                },
                "required": ["datetime_jp", "place"]
            },
            "speakers": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "The speaker's full name and English name if available (e.g., '岸波 宏和氏 / Hirokazu Kishinami'). If not explicitly labeled, infer from the start of the biography."},
                        "role": {"type": "string", "description": "The speaker's title and affiliation."}
                    },
                    "required": ["name", "role"]
                }
            }
        },
        "required": ["title", "subtitle", "intro", "overview", "speakers"]
    }

    system_prompt = f"""
    You are a data extraction expert. Your task is to analyze the provided webinar brief and extract the key information in a structured JSON format.
    The output MUST conform to this JSON schema:
    {json.dumps(schema, indent=2)}

    - Extract all relevant fields. If a field is not present in the text, omit it from the JSON unless it is required.
    - For date and time, capture all timezones provided (PT, CT, ET, JST).
    - The 'intro' should be a clean, well-formatted paragraph.
    - 'notices' should be a list of individual points.
    - If a speaker's name is not explicitly labeled, infer it from the start of the biography.
    - If the registration deadline or link is not present, return an empty string for those fields.
    - Ensure the output is a single, valid JSON object.
    """

    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": cleaned_text}
        ]
    )

    try:
        parsed_json = json.loads(response.choices[0].message.content)
        return parsed_json
    except (json.JSONDecodeError, IndexError) as e:
        st.error(f"Error parsing JSON from OpenAI: {e}")
        st.text_area("Raw OpenAI Response:", response.choices[0].message.content)
        return {}
# --- SIDEBAR ---
with st.sidebar:
    st.header("📊 ROI Metrics")
    with st.container(border=True):
        st.metric("Count", f"{st.session_state.run_count} runs")
    with st.container(border=True):
        st.metric("Time Saved", f"{st.session_state.time_saved} min")
    with st.container(border=True):
        st.metric("Money Saved", f"${st.session_state.money_saved:,.2f}")

    if st.session_state.last_run_seconds > 0:
        st.info(f"Last run: {st.session_state.last_run_seconds:.2f}s")

    st.header("⚙️ Settings")
    
    st.session_state.api_key = st.text_input(
        "OpenAI API Key", 
        type="password", 
        value=st.session_state.api_key,
        help="Your API key is used only for this session and not stored."
    )
    if not st.session_state.api_key:
        st.warning("Please enter your OpenAI API Key to generate emails.")
    
    model = st.selectbox(
        "Model",
        ("gpt-4o-mini", "gpt-4o", "gpt-4-turbo"),
        index=0,
        help="Cheaper models like gpt-4o-mini are recommended."
    )
    
    temperature = st.slider(
        "Temperature", 0.0, 1.0, 0.2, 0.05,
        help="Lower values make the output more deterministic and focused."
    )

# --- MAIN UI ---
st.title("📧 Webinar → Two Emails")
st.caption("Paste a messy webinar brief from Word/Outlook to generate 1 HTML and 1 text email.")

raw_text_input = st.text_area(
    "Paste your webinar brief here (JP or EN)",
    height=300,
    placeholder="""
例：
【ウェビナータイトル】生成AI時代の新しい働き方
【紹介文】本ウェビナーでは、生成AIを活用して業務効率を...
【開催日時】2024年10月28日(月) 10:00～11:00 (日本時間)
【登壇者】山田 太郎 (株式会社サンプル 代表取締役)
...
"""
)

if st.button("Generate Emails", type="primary", disabled=not st.session_state.api_key):
    if not raw_text_input.strip():
        st.warning("Please paste some text into the brief area.")
    else:
        start_time = time.time()
        
        with st.spinner("Analyzing and generating emails..."):
            try:
                # 1. Prune text
                cleaned_text = cheap_prune(raw_text_input)
                prune_msg = f"Pruned {len(raw_text_input)}→{len(cleaned_text)} chars."
                
                # 2. Extract with OpenAI
                data = extract_with_openai(cleaned_text, st.session_state.api_key, model, temperature)
                st.session_state.parsed_json = data
                
                # 3. Render Emails
                email1_html = render_final_email(EMAIL1_TEMPLATE, data)
                st.session_state.email1_html = email1_html

                email2_text = render_final_email_text(EMAIL2_TEMPLATE, data)
                st.session_state.email2_text = email2_text

                # 5. Update metrics
                end_time = time.time()
                st.session_state.last_run_seconds = end_time - start_time
                st.session_state.run_count += 1
                st.session_state.time_saved += 30
                st.session_state.money_saved += (30 / 60) * 40 # Assume $40/hr
                
                df = pd.DataFrame({"run_count": [st.session_state.run_count]})
                df.to_csv("run_log.csv", index=False)

                st.success(f"✓ Success! Generated in {st.session_state.last_run_seconds:.2f}s. ({prune_msg})")

            except openai.APIError as e:
                st.error(f"An OpenAI API error occurred: {e.message}")
            except Exception as e:
                st.exception(e)

# Display generated content if available
if st.session_state.email1_html:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Email (HTML)")
        st.code(st.session_state.email1_html, language="html")
        create_download_button(st.session_state.email1_html, "email_announcement.html", "Download HTML")

    with col2:
        st.subheader("Email (Text)")
        st.code(st.session_state.email2_text, language="text")
        create_download_button(st.session_state.email2_text, "email_text.txt", "Download Text")

    if st.checkbox("Show parsed JSON data"):
        st.json(st.session_state.parsed_json)

st.markdown("---")
st.caption("Made with :brain:. Using the combined power of human and robot.")
