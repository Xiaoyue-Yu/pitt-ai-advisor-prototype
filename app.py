import os
import streamlit as st
from openai import OpenAI


try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None


st.set_page_config(
    page_title="Pitt SCI AI Scholar-Advisor Prototype",
    page_icon="P",
    layout="wide",
)


PITT_BLUE = "#003594"
PITT_GOLD = "#FFB81C"

PITT_SCI_KNOWLEDGE = """
BSIS Pathways

Students must take 5 upper-level electives to satisfy the requirements of the IS major. Students can mix and match classes from a variety of areas to get a broad perspective of information science. For example, by taking INFSCI 1620: Advanced Security, INFSCI 1470: Immersive Media Technologies and INFSCI 1530: Data Mining, students can get an appreciation of using data for decision making, while accounting for security challenges and solutions with emerging technologies like VR/XR/AR and how humans use them.

It is also possible for students to pick focused Cybersecurity, UX, Information Systems, or Data-centric pathways.

Recommended Electives for Pathways

Cybersecurity Pathway:
- INFSCI 1620: Advanced Security
- INFSCI 1630: Communication Networks
- INFSCI 1670: Security Management and Computer Forensics

Students in this pathway also take two additional upper-level electives of their choosing.

UX Pathway:
- INFSCI 1420: User Centered Design
- INFSCI 1570: Network and Web Data Technologies
- INFSCI 1430: User Experience Engineering
- INFSCI 1450: Game Design
- INFSCI 1470: Immersive Media

Information Systems Pathway

Implementation of Information Systems:
- INFSCI 1570: Network and Web Data Technologies
- INFSCI 1630: Communication Networks
- INFSCI 1640: Wireless Networks
- INFSCI 1690: Cloud Computing
- INFSCI 1460: IT Project Management

Design of Information Systems:
- INFSCI 1460: IT Project Management
- INFSCI 1520: Information Visualization
- INFSCI 1430: User Experience Engineering
- INFSCI 1530: Data Mining
- INFSCI 1570: Network and Web Data Technologies

Data-Centric Pathway:
- INFSCI 1520: Information Visualization
- INFSCI 1530: Data Mining
- INFSCI 1540: Data Engineering
- INFSCI 1550: Spatial Information
- INFSCI 1560: Information Storage and Retrieval

Students can confer with their advisors and faculty mentors to select other classes for these pathways. For example, INFSCI 1440: Social Computing would also be a good choice for the data-centric pathway.
""".strip()


def build_css() -> None:
    st.markdown(
        f"""
        <style>
            :root {{
                --pitt-blue: {PITT_BLUE};
                --pitt-gold: {PITT_GOLD};
                --soft-blue: #eaf1ff;
                --ink: #172033;
            }}

            .stApp {{
                background:
                    radial-gradient(circle at top right, rgba(255,184,28,0.18), transparent 28%),
                    linear-gradient(180deg, #f6f8fc 0%, #eef3fb 100%);
                color: var(--ink);
            }}

            .block-container {{
                padding-top: 2rem;
                padding-bottom: 2rem;
            }}

            h1, h2, h3 {{
                color: var(--pitt-blue);
            }}

            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, #082b71 0%, #003594 100%);
            }}

            [data-testid="stSidebar"] * {{
                color: white !important;
            }}

            .hero-card {{
                background: linear-gradient(135deg, rgba(0,53,148,0.96), rgba(0,53,148,0.82));
                border-left: 8px solid var(--pitt-gold);
                border-radius: 18px;
                padding: 1.35rem 1.5rem;
                box-shadow: 0 18px 40px rgba(0, 53, 148, 0.18);
                margin-bottom: 1rem;
            }}

            .hero-card h1 {{
                color: white;
                margin-bottom: 0.35rem;
                font-size: 2rem;
            }}

            .hero-card p {{
                color: rgba(255, 255, 255, 0.92);
                margin: 0;
                font-size: 1rem;
            }}

            .info-card {{
                background: white;
                border: 1px solid rgba(0,53,148,0.12);
                border-radius: 18px;
                padding: 1rem 1.1rem;
                box-shadow: 0 12px 32px rgba(23, 32, 51, 0.06);
                min-height: 170px;
            }}

            .option-card {{
                background: white;
                border: 2px solid rgba(0,53,148,0.1);
                border-radius: 20px;
                padding: 1.25rem;
                box-shadow: 0 14px 38px rgba(23, 32, 51, 0.08);
                height: 100%;
            }}

            .option-label {{
                display: inline-block;
                background: var(--pitt-gold);
                color: #1f2430;
                font-weight: 700;
                padding: 0.25rem 0.65rem;
                border-radius: 999px;
                margin-bottom: 0.6rem;
            }}

            .caption-note {{
                color: #53627c;
                font-size: 0.95rem;
                margin-bottom: 0.75rem;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_openai_client():
    if OpenAI is None:
        return None
    if not os.getenv("OPENAI_API_KEY"):
        return None
    return OpenAI()

def call_llm(system_prompt: str, user_prompt: str, fallback: str) -> str:
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
        if not api_key.startswith("sk-or-"):
            return fallback + "\n\n[Error: OPENROUTER_API_KEY in .streamlit/secrets.toml does not look like a valid OpenRouter API key]"
    except KeyError:
        return fallback + "\n\n[Error: Cannot find OPENROUTER_API_KEY in .streamlit/secrets.toml]"

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    try:
        response = client.chat.completions.create(
            model="openrouter/free", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7
        )
        
        # Safely extract the content to prevent NoneType errors
        content = response.choices[0].message.content
        
        if content is None:
            return f"{fallback}\n\n[System Note: The free OpenRouter model returned an empty response due to network latency or rate limits. Falling back to the default local response. Please try again.]"
            
        return content.strip()
        
    except Exception as exc:  # pragma: no cover
        return f"{fallback}\n\n[API Error]: {exc}"

def option_a_answer(question: str) -> str:
    system_prompt = (
        "You are a general academic advisor. Answer briefly and helpfully. "
        "You have no access to the student's personal academic history."
    )
    fallback = (
        "If you want an HCI-related internship next summer, consider taking one course in HCI or UX,"
        " one course that strengthens design or prototyping skills, and one course that helps you build"
        " a stronger project portfolio. It would also help to look for projects related to user research,"
        " interaction design, VR, or game design."
    )
    return call_llm(system_prompt, question, fallback)


def option_b_answer(question: str, allow_history: bool, allow_career: bool) -> str:
    if not allow_history and not allow_career:
        return (
            "Because you have not authorized access to your personal academic data, "
            "I can only provide general SCI course recommendations."
        )

    system_prompt = f"""
You are a customized Pitt SCI scholar-advisor assistant.
Use the student's background when giving course advice.

Student background:
- Name: Helen Yu
- Major: Information Science
- Interests: HCI, VR, Serious Games
- Completed core courses: INFSCI 0410, INFSCI 0510

Permission status:
- Access to course history (PeopleSoft): {"granted" if allow_history else "not granted"}
- Access to career intention (Handshake): {"granted" if allow_career else "not granted"}

Guidance rules:
- Recommend next-semester SCI coursework that supports an HCI-related internship next summer.
- Mention concrete INFSCI courses when relevant.
- Use the official pathway information below.
- Suggest contacting a research mentor such as Dr. Dmitriy Babichenko.
- If some permissions are missing, be transparent about those limits while still using the data that is available.

Official SCI knowledge:
{PITT_SCI_KNOWLEDGE}
""".strip()

    fallback = (
        "Based on your Information Science major and your interests in HCI, VR, and serious games,"
        " the strongest next-semester choices would likely come from the UX pathway. INFSCI 1420:"
        " User Centered Design and INFSCI 1430: User Experience Engineering would directly support"
        " HCI internship preparation, while INFSCI 1450: Game Design or INFSCI 1470: Immersive Media"
        " could help you connect that HCI interest to games and immersive experiences. If you also want"
        " to build a broader profile, INFSCI 1520: Information Visualization is a useful complement."
        " Beyond coursework, it would be smart to contact a faculty mentor such as Dr. Dmitriy Babichenko"
        " to ask about research, projects, or lab opportunities that can strengthen your resume before"
        " next summer's internship cycle."
    )
    return call_llm(system_prompt, question, fallback)


def sidebar() -> tuple[bool, bool]:
    st.sidebar.markdown("## Student Profile")
    st.sidebar.markdown("**Name:** Helen Yu")
    st.sidebar.markdown("**Major:** Information Science")
    st.sidebar.markdown("**Completed Core Courses:** INFSCI 0410, INFSCI 0510")
    st.sidebar.markdown("**Interests:** HCI, VR, Serious Games")
    st.sidebar.markdown("---")
    st.sidebar.markdown("## Permission Controls")
    allow_history = st.sidebar.checkbox(
        "Allow AI to access my course history (PeopleSoft)",
        value=True,
    )
    allow_career = st.sidebar.checkbox(
        "Allow AI to access my career interests (Handshake)",
        value=True,
    )
    return allow_history, allow_career


def main() -> None:
    build_css()
    allow_history, allow_career = sidebar()

    st.markdown(
        """
        <div class="hero-card">
            <h1>Pitt SCI AI Scholar-Advisor Prototype</h1>
            <p>Compare a general LLM answer with a personalized SCI advising experience.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.15, 0.85], gap="large")

    with col1:
        st.markdown("### Student Question")
        question = st.text_area(
            "Prompt",
            value="I want to get an HCI-related internship next summer. What courses should I take next semester?",
            height=110,
            label_visibility="collapsed",
        )
        run_compare = st.button("Run A/B Comparison", type="primary", use_container_width=True)

    with col2:
        st.markdown(
            """
            <div class="info-card">
                <h3 style="margin-top:0;">Prototype Logic</h3>
                <p style="margin-bottom:0.55rem;"><strong>Option A:</strong> General mode with no student background and no SCI website knowledge.</p>
                <p style="margin-bottom:0;"><strong>Option B:</strong> Customized mode that injects student context and <code>PITT_SCI_KNOWLEDGE</code> based on permission settings.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if run_compare:
        a_col, b_col = st.columns(2, gap="large")

        with a_col:
            st.markdown(
                """
                <div class="option-card">
                    <div class="option-label">Option A</div>
                    <h3>General Mode</h3>
                    <div class="caption-note">Call the LLM directly with no student-specific background.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.spinner("Generating Option A..."):
                st.write(option_a_answer(question))

        with b_col:
            st.markdown(
                """
                <div class="option-card">
                    <div class="option-label">Option B</div>
                    <h3>Customized Mode</h3>
                    <div class="caption-note">Use permission-aware personalization plus official SCI pathway knowledge.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.spinner("Generating Option B..."):
                st.write(option_b_answer(question, allow_history, allow_career))

        with st.expander("View injected PITT_SCI_KNOWLEDGE"):
            st.code(PITT_SCI_KNOWLEDGE, language="text")


if __name__ == "__main__":
    main()
