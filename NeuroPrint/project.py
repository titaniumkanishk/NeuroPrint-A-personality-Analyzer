import os
import re
import time
import textwrap
from datetime import datetime
from statistics import mean
from textblob import TextBlob


# My sources of info :
#https://en.wikipedia.org/wiki/Psycholinguistics
#- Speech and Language Processing       -by Jurafsky & Martin
#- Psychology of Language               -by David W. Carroll
#project by - kanishk
# ==========================================================
# BEHAVIORAL DICTIONARIES
# ==========================================================

STRESS_WORDS = {
    "stressed": 4,
    "tension": 3,
    "pressure": 3,
    "overwhelmed": 5,
    "panic": 5,
    "headache": 2,
    "frustrated": 4,
    "exhausted": 4,
    "mentally drained": 5,
    "can't handle": 5,
    "breakdown": 5,
    "worried": 4,
    "nervous": 4,
    "anxiety": 5,
    "mind is not working": 5,
    "emotionally tired": 5,
    "full pressure": 5,
    "overthinking too much": 5,
    "mind got blank": 5,
    "mood off": 3,
    "too hectic": 4,
    "feeling low": 4,
    "emotionally exhausted": 5,
    "not able to focus": 4,
}

CONFIDENCE_WORDS = {
    "definitely": 4,
    "surely": 3,
    "clearly": 3,
    "absolutely": 4,
    "i can handle it": 5,
    "i will manage": 5,
    "for sure": 4,
    "i am confident": 5,
    "certainly": 4,
    "i can solve this": 5,
    "strongly believe": 3,
    "no doubt": 4,
    "fully sure": 4,
    "i will do it": 4,
    "i am capable": 5,
    "fixed decision": 4,
    "confirmed": 3,
}

HEDGING_WORDS = {
    "maybe": 2,
    "perhaps": 2,
    "probably": 2,
    "i guess": 3,
    "kind of": 2,
    "not sure": 4,
    "depends": 2,
    "possibly": 2,
    "might": 2,
    "uncertain": 4,
    "difficult to say": 3,
    "somehow": 2,
    "let's see": 2,
    "hopefully": 2,
    "could be": 2,
}

NEGATIVE_WORDS = {
    "hurt": 3,
    "sad": 3,
    "angry": 4,
    "upset": 3,
    "disappointed": 3,
    "lonely": 4,
    "betrayed": 5,
    "ignored": 3,
    "hopeless": 5,
    "crying": 4,
    "depressed": 5,
    "broken": 4,
    "painful": 3,
    "regret": 3,
    "guilty": 2,
    "terrible": 3,
}

POSITIVE_WORDS = {
    "motivated": 3,
    "hopeful": 4,
    "calm": 5,
    "peaceful": 5,
    "focused": 4,
    "determined": 5,
    "growing": 3,
    "better now": 4,
    "disciplined": 4,
    "positive": 3,
    "stable": 5,
    "grateful": 3,
    "optimistic": 4,
    "trying again": 4,
    "balanced": 5,
    "mentally strong": 5,
    "patient": 3,
}

SOCIAL_WORDS = {
    "family": 3,
    "friends": 3,
    "support": 4,
    "trust": 4,
    "relationship": 4,
    "respect": 3,
    "together": 3,
    "community": 3,
    "parents": 3,
    "friendship": 4,
    "communication": 3,
    "helping": 4,
    "caring": 5,
    "understanding": 4,
    "teamwork": 4,
    "loyalty": 5,
}


# ==========================================================
# FULL ASSESSMENT QUESTIONS
# ==========================================================

FULL_QUESTIONS = [
    "Reflect on a major challenge you faced in recent years and explain how it affected you emotionally and mentally.",

    "Imagine a teammate repeatedly misses deadlines because of family problems. How would you handle the situation?",

    "You receive a message saying: 'I can't believe you did that.' What would be your first interpretation?",

    "You have eight coins and one is heavier. Using a balance scale only twice, how would you identify it?",

    "A self-driving car can save five people by sacrificing one person. What should it do and why?",

    "Your manager gives you urgent work before an important personal event. Explain how you would prioritize the situation.",

    "Describe an abandoned library with nature growing inside it. Explain the atmosphere and emotions you imagine there.",

    "A close friend accidentally reveals your private secret. How would you react emotionally and socially?",

    "Explain the concept of freedom to a child using simple examples.",

    "A business has good products but poor sales because of pricing problems. What would you recommend?",

    "Do you believe artificial intelligence will improve or reduce human creativity in future? Explain your reasoning.",

    "Describe one childhood memory that still feels emotionally important to you today.",
]


# ==========================================================
# RAPID ASSESSMENT QUESTIONS
# ==========================================================

RAPID_QUESTIONS = [
    {
        "question": "You are close to an important deadline when your main file gets corrupted. What is your immediate reaction?",
        "options": {
            "A": {
                "text": "I will calmly solve it step-by-step. Pressure is there but I can manage it.",
                "effects": {
                    "stress": 6,
                    "confidence": 12,
                    "stability": 10,
                    "decision": 8,
                },
            },
            "B": {
                "text": "Maybe we may need extra time depending on the situation.",
                "effects": {
                    "stress": 8,
                    "confidence": 2,
                    "flexibility": 6,
                },
            },
            "C": {
                "text": "This is too much pressure. I feel mentally drained already.",
                "effects": {
                    "stress": 18,
                    "stability": -10,
                    "confidence": -6,
                },
            },
            "D": {
                "text": "I will first check backup systems and recovery methods carefully.",
                "effects": {
                    "stress": 4,
                    "confidence": 10,
                    "decision": 10,
                    "flexibility": 5,
                },
            },
        },
    },

    {
        "question": "A teammate criticizes your work publicly during a meeting. How do you react?",
        "options": {
            "A": {
                "text": "I will strongly defend my work because I know my reasoning is correct.",
                "effects": {
                    "confidence": 14,
                    "social": -2,
                    "decision": 5,
                },
            },
            "B": {
                "text": "Maybe there is some misunderstanding. I would discuss it professionally later.",
                "effects": {
                    "social": 8,
                    "flexibility": 8,
                    "stability": 6,
                },
            },
            "C": {
                "text": "Honestly I would feel hurt and emotionally disturbed by the situation.",
                "effects": {
                    "stress": 12,
                    "stability": -8,
                    "social": 4,
                },
            },
            "D": {
                "text": "I will stay calm and focus only on solving the actual issue.",
                "effects": {
                    "stability": 12,
                    "decision": 8,
                    "confidence": 6,
                },
            },
        },
    },

    {
        "question": "You receive a message saying 'We need to talk.' What is your first thought?",
        "options": {
            "A": {
                "text": "Something has definitely gone wrong.",
                "effects": {
                    "stress": 10,
                    "stability": -4,
                },
            },
            "B": {
                "text": "Maybe it could mean many different things.",
                "effects": {
                    "flexibility": 10,
                    "confidence": -2,
                },
            },
            "C": {
                "text": "I probably made some mistake without realizing it.",
                "effects": {
                    "stress": 12,
                    "confidence": -6,
                },
            },
            "D": {
                "text": "I will wait calmly before making assumptions.",
                "effects": {
                    "stability": 12,
                    "decision": 6,
                },
            },
        },
    },
]
RAPID_QUESTIONS.extend([
    {
        "question": "How would you usually describe your communication style?",
        "options": {
            "A": {
                "text": "I usually explain things in a logical and structured way.",
                "effects": {
                    "confidence": 6,
                    "decision": 6,
                    "flexibility": 4,
                },
            },
            "B": {
                "text": "I explain things emotionally with personal examples.",
                "effects": {
                    "social": 8,
                    "stability": 2,
                },
            },
            "C": {
                "text": "I keep things short because overexplaining feels unnecessary.",
                "effects": {
                    "confidence": 3,
                    "social": -2,
                },
            },
            "D": {
                "text": "Depends on the situation and the people involved.",
                "effects": {
                    "flexibility": 10,
                    "social": 5,
                },
            },
        },
    },

    {
        "question": "You suddenly need to adapt to a completely new work system. What is your reaction?",
        "options": {
            "A": {
                "text": "I enjoy learning new systems and adapting quickly.",
                "effects": {
                    "flexibility": 12,
                    "confidence": 6,
                },
            },
            "B": {
                "text": "I will somehow manage but it may take time.",
                "effects": {
                    "stress": 5,
                    "flexibility": 5,
                },
            },
            "C": {
                "text": "Too much change at once becomes mentally exhausting.",
                "effects": {
                    "stress": 14,
                    "stability": -6,
                },
            },
            "D": {
                "text": "I prefer stable systems and organized routines.",
                "effects": {
                    "decision": 6,
                    "flexibility": -2,
                },
            },
        },
    },

    {
        "question": "Your friend forgets an important promise made to you. What affects you the most?",
        "options": {
            "A": {
                "text": "The emotional disappointment hurts more than the mistake itself.",
                "effects": {
                    "social": 8,
                    "stress": 6,
                },
            },
            "B": {
                "text": "I try to understand their situation before reacting.",
                "effects": {
                    "social": 12,
                    "stability": 6,
                },
            },
            "C": {
                "text": "I become frustrated if repeated behavior keeps happening.",
                "effects": {
                    "stress": 8,
                    "decision": 5,
                },
            },
            "D": {
                "text": "I prefer discussing problems directly and clearly.",
                "effects": {
                    "confidence": 8,
                    "decision": 6,
                },
            },
        },
    },

    {
        "question": "A group project is failing because nobody is coordinating properly. What would you do?",
        "options": {
            "A": {
                "text": "I will take responsibility and organize tasks clearly.",
                "effects": {
                    "confidence": 14,
                    "decision": 10,
                    "social": 5,
                },
            },
            "B": {
                "text": "Maybe the group needs better communication first.",
                "effects": {
                    "social": 10,
                    "flexibility": 6,
                },
            },
            "C": {
                "text": "Too much confusion in teams becomes mentally tiring.",
                "effects": {
                    "stress": 10,
                    "stability": -3,
                },
            },
            "D": {
                "text": "I will quietly finish my part properly.",
                "effects": {
                    "decision": 5,
                    "social": -2,
                },
            },
        },
    },

    {
        "question": "You accidentally send a personal message to the wrong person. What is your reaction?",
        "options": {
            "A": {
                "text": "I feel very embarrassed and emotionally disturbed.",
                "effects": {
                    "stress": 14,
                    "stability": -6,
                },
            },
            "B": {
                "text": "I will calmly apologize and handle the situation maturely.",
                "effects": {
                    "stability": 10,
                    "decision": 6,
                },
            },
            "C": {
                "text": "Maybe it is awkward but not a major issue.",
                "effects": {
                    "flexibility": 5,
                    "stress": 2,
                },
            },
            "D": {
                "text": "I will overthink the situation for a long time.",
                "effects": {
                    "stress": 16,
                    "stability": -8,
                },
            },
        },
    },

    {
        "question": "How do you usually make difficult decisions?",
        "options": {
            "A": {
                "text": "I analyze every possibility carefully before deciding.",
                "effects": {
                    "decision": 12,
                    "flexibility": 10,
                },
            },
            "B": {
                "text": "I mostly trust my instincts and emotions.",
                "effects": {
                    "social": 4,
                    "decision": -2,
                },
            },
            "C": {
                "text": "Too many choices make me mentally exhausted.",
                "effects": {
                    "stress": 14,
                    "confidence": -6,
                },
            },
            "D": {
                "text": "I ask trusted people for advice before deciding.",
                "effects": {
                    "social": 10,
                    "decision": 4,
                },
            },
        },
    },

    {
        "question": "What affects your mood the most during stressful periods?",
        "options": {
            "A": {
                "text": "Lack of clarity and uncertainty.",
                "effects": {
                    "stress": 12,
                    "flexibility": -3,
                },
            },
            "B": {
                "text": "Relationship conflicts and emotional tension.",
                "effects": {
                    "social": 8,
                    "stress": 10,
                },
            },
            "C": {
                "text": "Work pressure and mental overload.",
                "effects": {
                    "stress": 18,
                    "stability": -6,
                },
            },
            "D": {
                "text": "I usually stay balanced even during difficult phases.",
                "effects": {
                    "stability": 14,
                    "confidence": 5,
                },
            },
        },
    },

    {
        "question": "How do you usually react after making a mistake?",
        "options": {
            "A": {
                "text": "I feel guilty and keep replaying it mentally.",
                "effects": {
                    "stress": 14,
                    "stability": -8,
                },
            },
            "B": {
                "text": "I try to learn from it and improve next time.",
                "effects": {
                    "stability": 10,
                    "decision": 8,
                },
            },
            "C": {
                "text": "I become frustrated if the mistake was avoidable.",
                "effects": {
                    "stress": 8,
                    "confidence": 2,
                },
            },
            "D": {
                "text": "Mistakes happen. I move on quickly.",
                "effects": {
                    "stability": 8,
                    "flexibility": 6,
                },
            },
        },
    },

    {
        "question": "What matters most to you in teamwork?",
        "options": {
            "A": {
                "text": "Clear communication and responsibility.",
                "effects": {
                    "social": 8,
                    "decision": 6,
                },
            },
            "B": {
                "text": "Mutual trust and emotional support.",
                "effects": {
                    "social": 14,
                    "stability": 4,
                },
            },
            "C": {
                "text": "Efficiency and fast results.",
                "effects": {
                    "confidence": 6,
                    "decision": 8,
                },
            },
            "D": {
                "text": "Avoiding unnecessary stress and confusion.",
                "effects": {
                    "stress": 6,
                    "stability": 2,
                },
            },
        },
    },
])


# ==========================================================
# TERMINAL FUNCTIONS
# ==========================================================

def welcome_screen():
    print("=" * 60)
    print("                 NEUROPRINT SYSTEM")
    print("     Advanced Psycholinguistic Analyzer")
    print("=" * 60)

    print("Analyzing communication behavior through")
    print("linguistic and behavioral inference patterns.")

    input("\nPress ENTER to continue...")


def select_mode():
    print("\n" + "=" * 60)
    print("                SELECT TEST MODE")
    print("=" * 60)

    print("1. Full Behavioral Assessment")
    print("2. Rapid Behavioral Assessment")

    while True:
        choice = input("\nChoose mode (1/2): ").strip()

        if choice == "1":
            return "full"

        if choice == "2":
            return "rapid"

        print("Invalid choice. Please select 1 or 2.")


def conduct_full_assessment():
    responses = []

    print("\nStarting Full Behavioral Assessment...\n")

    for index, question in enumerate(FULL_QUESTIONS, start=1):
        print(f"\nQuestion {index}")
        print("-" * 60)

        print(textwrap.fill(question, width=70))

        answer = input("\nYour response:\n> ")

        responses.append({
            "text": answer,
            "effects": {}
        })

    return responses


def conduct_rapid_assessment():
    responses = []

    print("\nStarting Rapid Behavioral Assessment...\n")

    for index, item in enumerate(RAPID_QUESTIONS, start=1):
        print(f"\nQuestion {index}")
        print("-" * 60)

        print(textwrap.fill(item["question"], width=70))
        print()

        for option, value in item["options"].items():
            print(f"{option}. {value['text']}")

        while True:
            choice = input("\nChoose option (A/B/C/D): ").upper().strip()

            if choice in item["options"]:
                responses.append(item["options"][choice])
                break

            print("Invalid option.")

    return responses


def generate_progress_bar(score):
    score = max(0, min(score, 100))

    filled = int(score / 5)
    empty = 20 - filled

    return f"[{'█' * filled}{'-' * empty}] {score}%"


def processing_animation():
    tasks = [
        "Analyzing emotional behavior",
        "Evaluating cognitive reasoning",
        "Generating communication profile",
        "Building NeuroPrint report",
    ]

    for task in tasks:
        print(f"\n{task}...")

        for number in range(0, 101, 20):
            print(generate_progress_bar(number), end="\r")
            time.sleep(0.2)

        print(generate_progress_bar(100))


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def main():
    welcome_screen()

    name = input("\nEnter your name: ").strip().title()

    mode = select_mode()

    if mode == "full":
        responses = conduct_full_assessment()
        assessment_name = "Full Behavioral Assessment"

    else:
        responses = conduct_rapid_assessment()
        assessment_name = "Rapid Behavioral Assessment"

    processing_animation()

    results = analyze_behavior(responses)

    report = generate_report(name, assessment_name, results)

    print(report)

    save_report(name, report)

# ==========================================================
# BEHAVIORAL ANALYSIS ENGINE
# ==========================================================

def analyze_behavior(responses):
    scores = {
        "stress": 0,
        "confidence": 50,
        "stability": 50,
        "social": 40,
        "flexibility": 45,
        "decision": 50,
    }

    full_text = []

    for response in responses:
        text = response["text"].lower()
        full_text.append(text)

        for category, value in response["effects"].items():
            scores[category] += value

        apply_dictionary_scoring(text, scores)

    combined_text = " ".join(full_text)

    scores["communication_style"] = detect_communication_style(combined_text)

    scores["fingerprint"] = generate_writing_fingerprint(combined_text)

    scores["contradictions"] = detect_contradictions(combined_text)

    scores["observations"] = generate_dynamic_observations(
        scores,
        combined_text
    )

    normalize_scores(scores)

    return scores


def apply_dictionary_scoring(text, scores):

    for word, value in STRESS_WORDS.items():
        if word in text:
            scores["stress"] += value
            scores["stability"] -= value // 2

    for word, value in CONFIDENCE_WORDS.items():
        if word in text:
            scores["confidence"] += value

    for word, value in HEDGING_WORDS.items():
        if word in text:
            scores["confidence"] -= value

            if value <= 2:
                scores["flexibility"] += 1

    for word, value in NEGATIVE_WORDS.items():
        if word in text:
            scores["stress"] += value
            scores["stability"] -= value

    for word, value in POSITIVE_WORDS.items():
        if word in text:
            scores["stability"] += value
            scores["stress"] -= 1

    for word, value in SOCIAL_WORDS.items():
        if word in text:
            scores["social"] += value


def normalize_scores(scores):

    dimensions = [
        "stress",
        "confidence",
        "stability",
        "social",
        "flexibility",
        "decision",
    ]

    for item in dimensions:
        scores[item] = max(0, min(scores[item], 100))


# ==========================================================
# COMMUNICATION ANALYSIS
# ==========================================================

def detect_communication_style(text):

    analytical_words = [
        "because",
        "therefore",
        "analyze",
        "process",
        "logic",
        "step",
        "reason",
        "carefully",
    ]

    emotional_words = [
        "feel",
        "hurt",
        "sad",
        "upset",
        "emotionally",
        "frustrated",
    ]

    professional_words = [
        "responsibility",
        "professional",
        "system",
        "strategy",
        "organized",
    ]

    analytical_score = sum(text.count(word) for word in analytical_words)

    emotional_score = sum(text.count(word) for word in emotional_words)

    professional_score = sum(text.count(word) for word in professional_words)

    if analytical_score > emotional_score and analytical_score > professional_score:
        return "Analytical and Structured"

    if emotional_score > analytical_score:
        return "Emotionally Reflective"

    return "Balanced and Professional"


# ==========================================================
# WRITING FINGERPRINT
# ==========================================================

def generate_writing_fingerprint(text):

    words = text.split()

    sentences = re.split(r"[.!?]", text)

    clean_sentences = [s for s in sentences if s.strip()]

    if not clean_sentences:
        average_length = 0
    else:
        average_length = round(len(words) / len(clean_sentences), 2)

    unique_words = len(set(words))

    lexical_density = round(
        (unique_words / max(len(words), 1)) * 100,
        2
    )

    punctuation_score = len(re.findall(r"[!?]", text))

    return {
        "average_sentence_length": average_length,
        "lexical_density": lexical_density,
        "punctuation_score": punctuation_score,
    }


# ==========================================================
# CONTRADICTION DETECTION
# ==========================================================

def detect_contradictions(text):

    contradictions = []

    if "calm" in text and "panic" in text:
        contradictions.append(
            "Some responses suggest emotional inconsistency during stressful situations."
        )

    if "confident" in text and "not sure" in text:
        contradictions.append(
            "Your responses show fluctuating confidence patterns in different situations."
        )

    if "trust" in text and "betrayed" in text:
        contradictions.append(
            "There are mixed emotional indicators regarding interpersonal trust."
        )

    return contradictions


# ==========================================================
# DYNAMIC OBSERVATIONS
# ==========================================================

def generate_dynamic_observations(scores, text):

    observations = []

    if scores["confidence"] >= 70:
        observations.append(
            "You tend to approach situations with noticeable confidence and direct decision-making."
        )

    if scores["stress"] >= 40:
        observations.append(
            "Your responses indicate that pressure and uncertainty can emotionally affect your thinking patterns."
        )

    if scores["stability"] >= 70:
        observations.append(
            "Even in emotionally difficult situations, your responses suggest good emotional recovery ability."
        )

    if scores["social"] >= 65:
        observations.append(
            "Your communication patterns suggest strong empathy and relationship awareness."
        )

    if scores["decision"] >= 70:
        observations.append(
            "You appear to prefer structured and practical decision-making over impulsive reactions."
        )

    if scores["flexibility"] >= 70:
        observations.append(
            "Your responses suggest cognitive flexibility and openness toward different perspectives."
        )

    if scores["communication_style"] == "Analytical and Structured":
        observations.append(
            "You generally communicate in a logical and organized way, especially during problem-solving situations."
        )

    if scores["communication_style"] == "Emotionally Reflective":
        observations.append(
            "Your communication style appears emotionally expressive and personally reflective."
        )

    if "overthinking" in text or "mentally drained" in text:
        observations.append(
            "There are indicators of overthinking tendencies during stressful or uncertain situations."
        )

    observations.extend(scores["contradictions"])

    if not observations:
        observations.append(
            "Your responses show a relatively balanced combination of emotional, logical, and social reasoning patterns."
        )

    return observations


# ==========================================================
# REPORT GENERATION
# ==========================================================

def generate_report(name, mode, scores):

    emotional_bar = generate_progress_bar(scores["stability"])

    stress_bar = generate_progress_bar(scores["stress"])

    confidence_bar = generate_progress_bar(scores["confidence"])

    social_bar = generate_progress_bar(scores["social"])

    flexibility_bar = generate_progress_bar(scores["flexibility"])

    decision_bar = generate_progress_bar(scores["decision"])

    report = f"""
============================================================
                    NEUROPRINT REPORT
============================================================

Behavioral Analysis Report For: {name}
Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M')}
Assessment Mode: {mode}

============================================================
                    BEHAVIOR SUMMARY
============================================================

{name} demonstrates a combination of emotional,
social, and cognitive patterns that reflect how
they process pressure, communication, uncertainty,
relationships, and decision-making situations.

============================================================
               PSYCHOLOGICAL INDICATORS
============================================================

Emotional Stability
{emotional_bar}

Stress Response
{stress_bar}

Confidence Style
{confidence_bar}

Social Orientation
{social_bar}

Cognitive Flexibility
{flexibility_bar}

Decision Behavior
{decision_bar}

============================================================
               COMMUNICATION STYLE
============================================================

Primary Communication Pattern:
→ {scores['communication_style']}

============================================================
                WRITING FINGERPRINT
============================================================

Average Sentence Length:
→ {scores['fingerprint']['average_sentence_length']} words

Lexical Density:
→ {scores['fingerprint']['lexical_density']}%

Punctuation Intensity:
→ {scores['fingerprint']['punctuation_score']}

============================================================
                BEHAVIORAL OBSERVATIONS
============================================================
"""

    for observation in scores["observations"]:
        report += f"\n• {observation}\n"

    report += f"""

============================================================
               HUMAN-FRIENDLY SUMMARY
============================================================

{name}, your responses suggest that you usually
try to balance emotions with practical thinking.

Your behavioral patterns indicate how you handle:
- pressure
- uncertainty
- communication
- social situations
- emotional reactions

You appear to reflect carefully before reacting,
and your responses show noticeable emotional
awareness and reasoning ability.

Your communication style suggests:
→ {scores['communication_style']}

============================================================
IMPORTANT NOTE
============================================================

NeuroPrint provides psycholinguistic behavioral
insights based on communication patterns.

This is NOT a medical or psychiatric diagnosis.

============================================================
"""

    return report


# ==========================================================
# SAVE REPORT
# ==========================================================

def save_report(name, report):

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"reports/{name.lower()}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"\nReport saved successfully: {filename}")


# ==========================================================
# PROGRAM EXECUTION
# ==========================================================

if __name__ == "__main__":
    main()
