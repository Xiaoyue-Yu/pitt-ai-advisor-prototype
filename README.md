# Pitt SCI AI Scholar-Advisor Prototype

A proof-of-concept AI assistant designed for the School of Computing and Information (SCI) to demonstrate personalized academic advising using LLMs.

## 🚀 Key Features
- **A/B Comparison**: Compare a "General Mode" response with a "Personalized Mode" that uses student-specific data.
- **Privacy-First**: Simulated permission toggles for PeopleSoft (course history) and Handshake (career goals) data.
- **Domain-Specific**: Injects official SCI Information Science pathway knowledge (UX, Cybersecurity, Data-centric).
- **Robustness**: Implements defensive error handling for API latency and empty responses.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **LLM Engine**: OpenRouter API (Free Models)
- **Language**: Python 3.x

## 📦 Quick Start

1. **Clone & Install**
   ```bash
   git clone https://github.com/Xiaoyue-Yu/pitt-ai-advisor-prototype.git
   pip install -r requirements.txt
   ```

2. **Setup Secrets**
   Create `.streamlit/secrets.toml`:
   ```toml
   OPENROUTER_API_KEY = "your_sk_or_key_here"
   ```

3. **Run**
   ```bash
   streamlit run app.py
   ```

## 🔒 Security
Sensitive credentials and caches are excluded from the repository via `.gitignore` to prevent credential leakage.

## 🎓 Disclaimer
This is a **prototype** for demonstration purposes only. Official academic advising should be sought through Pitt SCI advisors.

