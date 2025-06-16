# app.py
import os
import json
from dotenv import load_dotenv

# Optional: Simulate OpenAI response if openai not available
def mock_openai_response(prompt):
    return "[MOCK RESPONSE] This is a simulated response to: " + prompt[:60] + "..."

# Try importing openai, else fallback to mock
try:
    import openai
    openai_available = True
except ModuleNotFoundError:
    print("Warning: 'openai' module not installed. Using mock response.")
    openai_available = False

load_dotenv()
if openai_available:
    openai.api_key = os.getenv("OPENAI_API_KEY")

# Load career mapping data
def load_career_data():
    default_data = {
        "python": ["Data Scientist", "Backend Developer"],
        "design": ["UI/UX Designer", "Product Designer"],
        "marketing": ["Digital Marketer", "SEO Specialist"]
    }
    try:
        with open("career_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: 'career_data.json' not found. Using default data.")
        return default_data

career_data = load_career_data()

# Prompt templates
def generate_prompt(user_text):
    return f"""
You are an AI Career Coach. Based on the user's question below, give career advice, suggest learning paths, or recommend suitable roles.

User: {user_text}
"""

# Resume analyzer (simple)
def analyze_resume(resume_text):
    prompt = f"""Read this resume and give 3 improvement suggestions:

{resume_text}"""
    if openai_available:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    else:
        return mock_openai_response(prompt)

# Simulated main() interaction to avoid input() errors
def simulate_main():
    print("Welcome to AI Career Mentor (Simulated CLI Version)")
    test_modes = ["1", "2", "3"]

    for mode in test_modes:
        print(f"\n--- Running Mode {mode} ---")
        if mode == "1":
            user_input = "What are good career paths for someone learning Python and design?"
            prompt = generate_prompt(user_input)
            if openai_available:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                print("\nAdvice:\n", response.choices[0].message.content.strip())
            else:
                print("\nAdvice:\n", mock_openai_response(prompt))

        elif mode == "2":
            resume_text = "Experienced marketing professional skilled in SEO, content creation, and analytics."
            feedback = analyze_resume(resume_text)
            print("\nResume Feedback:\n", feedback)

        elif mode == "3":
            selected_skills = ["python", "design"]
            result = []
            for skill in selected_skills:
                result += career_data.get(skill, [])
            result = list(set(result))
            print("\nSuggested Careers:")
            for r in result:
                print("-", r)

if __name__ == "__main__":
    simulate_main()