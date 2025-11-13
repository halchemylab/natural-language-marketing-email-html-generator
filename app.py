import streamlit as st
import openai
import re
import json
import time
import base64
from typing import Dict, Any, List

# --- TEMPLATES & SCHEMA ---
# These templates can be edited to change branding, colors, and layout.
# Use standard HTML and inline CSS. Placeholders like {title} will be replaced.

EMAIL1_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; line-height: 1.6; color: #333; max-width: 600px; margin: 20px auto; padding: 0 15px; }
  h1, h2, h3 { color: #111; }
  h1 { font-size: 24px; }
  h2 { font-size: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-top: 30px; }
  .updated-notice { color: #aa2128; font-weight: bold; font-size: 14px; }
  .intro { white-space: pre-wrap; font-size: 16px; }
  .learnings-list { list-style-type: none; padding-left: 0; }
  .learnings-list li { margin-bottom: 15px; }
  .learnings-list strong { display: block; font-size: 16px; color: #000; }
  .speaker-block { margin-bottom: 20px; padding-left: 15px; border-left: 3px solid #eee; }
  .speaker-block .name { font-weight: bold; font-size: 16px; }
  .speaker-block .role { color: #555; font-size: 14px; }
  .speaker-block .career { white-space: pre-wrap; font-size: 14px; color: #666; margin-top: 5px; }
  .overview-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
  .overview-table th, .overview-table td { border: 1px solid #ddd; padding: 10px; text-align: left; vertical-align: top; }
  .overview-table th { background-color: #f9f9f9; width: 100px; }
  .cta-button { display: inline-block; background-color: #aa2128; color: #ffffff; padding: 12px 25px; text-align: center; text-decoration: none; font-weight: bold; border-radius: 5px; margin-top: 25px; }
</style>
</head>
<body>
  <h1>{title}</h1>
  {subtitle_html}
  {updated_html}
  
  <p class="intro">{intro}</p>

  {learnings_html}
  
  {speakers_html}

  <h2>開催概要</h2>
  {overview_html}
  
  {cta_button_html}
</body>
</html>
"""

EMAIL2_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>リマインダー: {title}</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; line-height: 1.6; color: #333; max-width: 600px; margin: 20px auto; padding: 0 15px; }
  h1 { font-size: 22px; color: #111; }
  .preface { color: #aa2128; font-weight: bold; border: 1px solid #aa2128; padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center; }
  .date-summary { font-weight: bold; font-size: 16px; margin-bottom: 10px; }
  .details { font-size: 14px; color: #555; }
  .intro-snippet { margin-top: 20px; font-size: 15px; }
  .cta-button { display: inline-block; background-color: #aa2128; color: #ffffff; padding: 12px 25px; text-align: center; text-decoration: none; font-weight: bold; border-radius: 5px; margin-top: 25px; }
</style>
</head>
<body>
  <div class="preface">開催が近づいてまいりました</div>
  
  <h1>{title}</h1>
  {subtitle_html}
  
  <p class="date-summary">{date_summary}</p>
  
  <div class="details">
    {place_html}
    {deadline_html}
  </div>
  
  <p class="intro-snippet">{intro_snippet}</p>
  
  {cta_button_html}
</body>
</html>
"""

JSON_SCHEMA = {
  "type": "object",
  "required": ["title", "intro", "overview"],
  "properties": {
    "title": { "type": "string", "description": "The main title of the webinar." },
    "subtitle": { "type": "string", "description": "The subtitle of the webinar, if any." },
    "updated": { "type": "string", "description": "An optional update notice, like 'Updated: June 5'." },
    "intro": { "type": "string", "description": "The main introductory text. Preserve line breaks." },
    "learnings": {
      "type": "array",
      "description": "Key takeaways or topics covered.",
      "items": { 
        "type": "object",
        "required": ["heading"],
        "properties": {
          "heading": { "type": "string", "description": "The heading of a learning point." },
          "desc": { "type": "string", "description": "A short description for the learning point." }
        }
      }
    },
    "speakers": {
      "type": "array",
      "description": "List of speakers.",
      "items": { 
        "type": "object",
        "required": ["name"],
        "properties": {
          "name": { "type": "string", "description": "Speaker's full name." },
          "role": { "type": "string", "description": "Speaker's title or role." },
          "career": { "type": "string", "description": "Speaker's biography or career summary. Preserve line breaks." }
        }
      }
    },
    "overview": {
      "type": "object",
      "description": "Structured details about the event.",
      "properties": {
        "datetime_jp": { "type": "string", "description": "Date and time in Japan Standard Time." },
        "datetime_pt": { "type": "string", "description": "Date and time in Pacific Time." },
        "datetime_ct": { "type": "string", "description": "Date and time in Central Time." },
        "datetime_et": { "type": "string", "description": "Date and time in Eastern Time." },
        "place": { "type": "string", "description": "Location of the event (e.g., 'Online', 'Zoom')." },
        "audience": { "type": "array", "items": { "type": "string" }, "description": "Target audience for the webinar." },
        "notices": { "type": "array", "items": { "type": "string" }, "description": "Important notices or disclaimers." },
        "registration_deadline": { "type": "string", "description": "Deadline for registration." },
        "link": { "type": "string", "description": "URL for registration or more details." }
      }
    }
  }
}

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
    
    # 2. Filter for lines containing likely event-related keywords
    keywords = [
        '開催', '日時', '日本時間', 'PT', 'CT', 'ET', 'タイトル', '対象', 
        '注意事項', '紹介文', '概要', '登壇者', '経歴', 'Zoom', '締切', 
        '申し込み', 'URL', 'メール', 'agenda', 'speaker', 'topic', 'date', 'time'
    ]
    keyword_regex = re.compile('|'.join(keywords), re.IGNORECASE)
    
    # Regex for simple date/time/url patterns
    pattern_regex = re.compile(
        r'(\d{1,4}[-/年]\d{1,2}[-/月]\d{1,2}日?)|'  # Date like 2023/10/26
        r'(\d{1,2}:\d{2})|'                        # Time like 10:00
        r'(https?://\S+)|'                       # URL
        r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})' # Email
    )

    pruned_lines = [
        line.strip() for line in lines 
        if keyword_regex.search(line) or pattern_regex.search(line) or len(line.strip()) < 10 # Keep very short lines (often headings)
    ]
    
    # Collapse multiple blank lines
    collapsed_text = re.sub(r'\n{3,}', '\n\n', "\n".join(pruned_lines))
    
    # 3. Fallback: If speaker info seems to be lost, use original text
    speaker_keywords_present = any(kw in raw_text for kw in ['登壇者', '経歴', 'speaker'])
    if speaker_keywords_present and not any(kw in collapsed_text for kw in ['登壇者', '経歴', 'speaker']):
        return raw_text # Fallback to original if pruning was too aggressive
        
    return collapsed_text

def extract_with_openai(cleaned_text: str, api_key: str, model: str, temperature: float) -> Dict[str, Any]:
    """
    Calls OpenAI API with structured output (JSON Schema) to extract webinar details.
    """
    client = openai.OpenAI(api_key=api_key)
    
    system_prompt = """
    You are a meticulous JP/EN webinar brief extractor. Your task is to analyze the provided text and extract information into a structured JSON format according to the given schema.
    - Return ONLY the JSON object that conforms to the schema. Do not add any introductory text, explanations, or markdown fences.
    - Preserve the original Japanese text wherever possible.
    - Normalize whitespace within fields.
    - For bulleted lists like 'learnings', split each bullet into a separate object in the array.
    - For 'speakers', create a separate object for each person.
    - If a field is not found in the text, return an empty string "" for string types or an empty array [] for array types. Do not invent data.
    """
    
    user_prompt = f"""
    Please extract the webinar details from the following text and provide the output strictly as a JSON object matching the required schema.

    --- START OF WEBINAR BRIEF ---
    {cleaned_text}
    --- END OF WEBINAR BRIEF ---
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "WebinarEmailSchema",
                "schema": JSON_SCHEMA,
                "strict": True
            }
        }
    )
    
    content = response.choices[0].message.content
    return json.loads(content)

# --- HTML RENDERING HELPERS ---

def to_br(text: str) -> str:
    """Converts newlines to <br> tags and escapes HTML."""
    if not text:
        return ""
    # Basic escape
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return text.replace('\n', '<br>\n')

def render_learnings_html(learnings: List[Dict[str, str]]) -> str:
    if not learnings:
        return ""
    items = []
    for item in learnings:
        heading = item.get('heading', '')
        desc = item.get('desc', '')
        item_html = f"<li><strong>{to_br(heading)}</strong>"
        if desc:
            item_html += f"<br>{to_br(desc)}"
        item_html += "</li>"
        items.append(item_html)
    return f'<h2>このウェビナーで学べること</h2>\n<ul class="learnings-list">\n{"".join(items)}\n</ul>'

def render_speakers_html(speakers: List[Dict[str, str]]) -> str:
    if not speakers:
        return ""
    blocks = []
    for speaker in speakers:
        name = speaker.get('name', 'N/A')
        role = speaker.get('role', '')
        career = speaker.get('career', '')
        block = '<div class="speaker-block">'
        block += f'<p class="name">{to_br(name)}</p>'
        if role:
            block += f'<p class="role">{to_br(role)}</p>'
        if career:
            block += f'<p class="career">{to_br(career)}</p>'
        block += '</div>'
        blocks.append(block)
    return f'<h2>登壇者紹介</h2>\n{"".join(blocks)}'

def render_overview_html(overview: Dict[str, Any]) -> str:
    if not overview:
        return ""
    
    rows = []
    
    # Combine date/time fields
    datetime_parts = [
        overview.get('datetime_jp'),
        overview.get('datetime_pt'),
        overview.get('datetime_ct'),
        overview.get('datetime_et')
    ]
    datetime_str = '<br>'.join(filter(None, datetime_parts))
    if datetime_str:
        rows.append(f'<tr><th>日時</th><td>{datetime_str}</td></tr>')

    if overview.get('place'):
        rows.append(f'<tr><th>場所</th><td>{to_br(overview["place"])}</td></tr>')
        
    if overview.get('audience'):
        audience_list = '<ul>' + ''.join(f'<li>{to_br(item)}</li>' for item in overview['audience']) + '</ul>'
        rows.append(f'<tr><th>対象</th><td>{audience_list}</td></tr>')

    if overview.get('notices'):
        notices_list = '<ul>' + ''.join(f'<li>{to_br(item)}</li>' for item in overview['notices']) + '</ul>'
        rows.append(f'<tr><th>注意事項</th><td>{notices_list}</td></tr>')

    if overview.get('registration_deadline'):
        rows.append(f'<tr><th>申込締切</th><td>{to_br(overview["registration_deadline"])}</td></tr>')

    if not rows:
        return ""
        
    return f'<table class="overview-table">\n{"".join(rows)}\n</table>'

def create_download_button(html_content: str, filename: str, label: str):
    """Generates a download button for the given HTML content."""
    b64 = base64.b64encode(html_content.encode()).decode()
    return st.download_button(
        label=label,
        data=html_content,
        file_name=filename,
        mime='text/html',
    )

# --- MAIN APP ---

st.set_page_config(page_title="Webinar Email Generator", page_icon="📧", layout="wide")

# Initialize session state
if 'run_count' not in st.session_state:
    st.session_state.run_count = 0
    st.session_state.time_saved = 0
    st.session_state.money_saved = 0.0
    st.session_state.last_run_seconds = 0.0
    st.session_state.email1_html = ""
    st.session_state.email2_html = ""
    st.session_state.parsed_json = None
    st.session_state.api_key = ""

# --- SIDEBAR ---
with st.sidebar:
    st.header("📊 Metrics")
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
st.title("📧 Webinar → Two Emails (LP-style)")
st.caption("Paste a messy webinar brief from Word/Outlook to generate two clean HTML emails.")

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

if st.button("Generate Emails", type="primary"):
    if not st.session_state.api_key:
        st.error("Please enter your OpenAI API Key in the sidebar.")
    elif not raw_text_input.strip():
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
                
                # 3. Render Email #1 (Announcement)
                overview = data.get('overview', {})
                email1_html = EMAIL1_TEMPLATE.format(
                    title=data.get('title', 'Webinar Announcement'),
                    subtitle_html=f"<h2>{to_br(data['subtitle'])}</h2>" if data.get('subtitle') else "",
                    updated_html=f"<p class='updated-notice'>{to_br(data['updated'])}</p>" if data.get('updated') else "",
                    intro=to_br(data.get('intro', '')),
                    learnings_html=render_learnings_html(data.get('learnings', [])),
                    speakers_html=render_speakers_html(data.get('speakers', [])),
                    overview_html=render_overview_html(overview),
                    cta_button_html=f'<a href="{overview["link"]}" class="cta-button">詳細・お申し込み</a>' if overview.get('link') else ""
                )
                st.session_state.email1_html = email1_html

                # 4. Render Email #2 (Reminder)
                date_summary_parts = [overview.get('datetime_jp')]
                other_times = ' / '.join(filter(None, [overview.get('datetime_pt'), overview.get('datetime_ct'), overview.get('datetime_et')]))
                if other_times:
                    date_summary_parts.append(f"({other_times})")
                
                intro_snippet = data.get('intro', '')
                if len(intro_snippet) > 280:
                    intro_snippet = intro_snippet[:280] + '...'

                email2_html = EMAIL2_TEMPLATE.format(
                    title=data.get('title', 'Webinar Reminder'),
                    subtitle_html=f"<h3>{to_br(data['subtitle'])}</h3>" if data.get('subtitle') else "",
                    date_summary=' '.join(filter(None, date_summary_parts)),
                    place_html=f"<p><strong>場所:</strong> {to_br(overview['place'])}</p>" if overview.get('place') else "",
                    deadline_html=f"<p><strong>申込締切:</strong> {to_br(overview['registration_deadline'])}</p>" if overview.get('registration_deadline') else "",
                    intro_snippet=to_br(intro_snippet),
                    cta_button_html=f'<a href="{overview["link"]}" class="cta-button">今すぐ申し込み</a>' if overview.get('link') else ""
                )
                st.session_state.email2_html = email2_html

                # 5. Update metrics
                end_time = time.time()
                st.session_state.last_run_seconds = end_time - start_time
                st.session_state.run_count += 1
                st.session_state.time_saved += 30
                st.session_state.money_saved += (30 / 60) * 40 # Assume $40/hr

                st.success(f"✓ Success! Generated in {st.session_state.last_run_seconds:.2f}s. ({prune_msg})")
                st.rerun()

            except openai.APIError as e:
                st.error(f"An OpenAI API error occurred: {e.message}")
            except Exception as e:
                st.exception(e)

# Display generated content if available
if st.session_state.email1_html:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Email #1 (Announcement)")
        st.code(st.session_state.email1_html, language="html")
        create_download_button(st.session_state.email1_html, "email_announcement.html", "Download HTML #1")

    with col2:
        st.subheader("Email #2 (Reminder)")
        st.code(st.session_state.email2_html, language="html")
        create_download_button(st.session_state.email2_html, "email_reminder.html", "Download HTML #2")

    if st.checkbox("Show parsed JSON data"):
        st.json(st.session_state.parsed_json)

st.markdown("---")
st.caption("Powered by Streamlit. Uses OpenAI Structured Outputs for schema-locked JSON.")
