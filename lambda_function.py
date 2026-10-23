# -*- coding: utf-8 -*-
"""
StudyBuddy+ — Alexa Custom Skill (lambda_function.py)
Designed for Alexa-hosted Python skill on the Alexa Developer Console.

Features:
  - Voice quiz: 10 Class 10 CBSE Science MCQs, scored with explanations.
  - Topic revision: 4-5 sentence summaries for 5 Class 10 Science topics.
"""

import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

# ── Logger ────────────────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ── Quiz Data ─────────────────────────────────────────────────────────────────
# 10 Class 10 CBSE Science MCQs. Each entry: question, options (a-d), answer key, explanation.
QUIZ_QUESTIONS = [
    {
        "question": "What is the pH of a neutral solution?",
        "options": {"a": "0", "b": "7", "c": "14", "d": "1"},
        "answer": "b",
        "explanation": "A neutral solution has a pH of 7. Below 7 is acidic; above 7 is basic."
    },
    {
        "question": "Which mirror is used in vehicle rear-view mirrors?",
        "options": {"a": "Concave", "b": "Plane", "c": "Convex", "d": "Parabolic"},
        "answer": "c",
        "explanation": "Convex mirrors give a wider field of view, making them ideal for rear-view mirrors."
    },
    {
        "question": "The SI unit of electric resistance is?",
        "options": {"a": "Ampere", "b": "Volt", "c": "Watt", "d": "Ohm"},
        "answer": "d",
        "explanation": "Resistance is measured in Ohms, as defined by Ohm's Law: V equals I times R."
    },
    {
        "question": "Which gas is produced when dilute HCl reacts with zinc?",
        "options": {"a": "Oxygen", "b": "Chlorine", "c": "Hydrogen", "d": "Carbon dioxide"},
        "answer": "c",
        "explanation": "Zinc displaces hydrogen from HCl, releasing hydrogen gas and forming zinc chloride."
    },
    {
        "question": "The process of breaking down glucose to release energy is called?",
        "options": {"a": "Photosynthesis", "b": "Respiration", "c": "Digestion", "d": "Excretion"},
        "answer": "b",
        "explanation": "Respiration breaks glucose into carbon dioxide and water, releasing energy as ATP."
    },
    {
        "question": "Which lens is used to correct myopia (short-sightedness)?",
        "options": {"a": "Convex", "b": "Bifocal", "c": "Concave", "d": "Cylindrical"},
        "answer": "c",
        "explanation": "Concave lenses diverge light, correcting the over-convergence that causes myopia."
    },
    {
        "question": "What is the valency of carbon?",
        "options": {"a": "2", "b": "4", "c": "6", "d": "1"},
        "answer": "b",
        "explanation": "Carbon has 4 valence electrons, giving it a valency of 4 and enabling long chains."
    },
    {
        "question": "According to Ohm's Law, if voltage doubles and resistance stays the same, current?",
        "options": {"a": "Halves", "b": "Stays the same", "c": "Doubles", "d": "Quadruples"},
        "answer": "c",
        "explanation": "Ohm's Law: I equals V divided by R. Doubling V doubles I when R is constant."
    },
    {
        "question": "Which part of the plant conducts photosynthesis mainly?",
        "options": {"a": "Root", "b": "Stem", "c": "Leaf", "d": "Flower"},
        "answer": "c",
        "explanation": "Leaves contain chlorophyll and have the most surface area to absorb sunlight."
    },
    {
        "question": "Ethanol is an example of which class of carbon compounds?",
        "options": {"a": "Carboxylic acids", "b": "Aldehydes", "c": "Alcohols", "d": "Esters"},
        "answer": "c",
        "explanation": "Ethanol has an OH functional group, making it an alcohol (C2H5OH)."
    }
]

# ── Revision Data ─────────────────────────────────────────────────────────────
# 4-5 sentence spoken summaries for 5 Class 10 CBSE Science topics.
REVISION_SUMMARIES = {
    "acids and bases": (
        "Acids taste sour and turn blue litmus red, while bases taste bitter and turn red litmus blue. "
        "pH measures acidity: below 7 is acidic, 7 is neutral, and above 7 is basic. "
        "When acids and bases react, they neutralise each other to form salt and water. "
        "Common acids include hydrochloric acid and sulphuric acid. "
        "Indicators like phenolphthalein and methyl orange help identify acids and bases."
    ),
    "light": (
        "Light travels in straight lines and reflects off smooth surfaces following the law of reflection. "
        "Concave mirrors converge light and form real or virtual images depending on object distance. "
        "Convex mirrors always form virtual, erect, and diminished images. "
        "Refraction is the bending of light as it passes from one medium to another, explained by Snell's Law. "
        "The human eye uses a convex lens to focus images on the retina, and defects like myopia and hyperopia are corrected with lenses."
    ),
    "electricity": (
        "Electric current is the flow of charge, measured in Amperes. "
        "Ohm's Law states that voltage equals current multiplied by resistance. "
        "In a series circuit, the same current flows through all components; in a parallel circuit, voltage is the same across each branch. "
        "Electric power is calculated as P equals V times I, measured in Watts. "
        "Heating effect of current is used in devices like electric heaters and fuses."
    ),
    "life processes": (
        "Life processes are the essential functions that keep organisms alive: nutrition, respiration, transport, and excretion. "
        "In photosynthesis, plants use sunlight, water, and carbon dioxide to make glucose and release oxygen. "
        "Respiration releases energy from glucose; it can be aerobic (with oxygen) or anaerobic (without oxygen). "
        "The human heart pumps blood through a double circulatory system separating oxygenated and deoxygenated blood. "
        "Excretion removes waste products; in humans, the kidneys filter blood and produce urine."
    ),
    "carbon compounds": (
        "Carbon can form four covalent bonds, allowing it to create long chains, branches, and rings. "
        "Hydrocarbons contain only carbon and hydrogen; alkanes are saturated and alkenes are unsaturated. "
        "Functional groups like OH for alcohols and COOH for carboxylic acids give compounds their properties. "
        "Ethanol is a useful alcohol found in beverages and fuels, while ethanoic acid is the acid in vinegar. "
        "Addition and substitution reactions are the main reaction types for carbon compounds."
    )
}

# ── Helper Functions ──────────────────────────────────────────────────────────

def get_current_question(session_attrs):
    """Return the current quiz question dict based on the session index."""
    idx = session_attrs.get("question_index", 0)
    return QUIZ_QUESTIONS[idx]


def build_question_speech(q_index):
    """Build the spoken text for a quiz question with its lettered options."""
    q = QUIZ_QUESTIONS[q_index]
    speech = (
        f"Question {q_index + 1}. {q['question']} "
        f"A: {q['options']['a']}. "
        f"B: {q['options']['b']}. "
        f"C: {q['options']['c']}. "
        f"D: {q['options']['d']}."
    )
    return speech


def build_final_score_speech(score):
    """Return an encouraging message with the final score."""
    total = len(QUIZ_QUESTIONS)
    pct = (score / total) * 100

    if pct == 100:
        encouragement = "Perfect score! You're a Science star!"
    elif pct >= 70:
        encouragement = "Great job! Keep practising and you'll ace it!"
    elif pct >= 40:
        encouragement = "Good effort! A little more revision will help!"
    else:
        encouragement = "Don't worry! Every attempt makes you smarter. Keep going!"

    return f"Quiz over! You scored {score} out of {total}. {encouragement}"


# ── Request Handlers ──────────────────────────────────────────────────────────

class LaunchRequestHandler(AbstractRequestHandler):
    """Handles skill launch — greets the user and offers quiz or revision."""

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech = (
            "Welcome to Study Buddy Plus! "
            "You can say quiz me to start a quiz, "
            "or revise a topic like acids and bases or electricity. "
            "What would you like to do?"
        )
        reprompt = "Say quiz me to start a quiz, or revise a topic."
        return (
            handler_input.response_builder
            .speak(speech)
            .ask(reprompt)
            .response
        )


class StartQuizIntentHandler(AbstractRequestHandler):
    """Starts the quiz by resetting session attributes and reading question 1."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("StartQuizIntent")(handler_input)

    def handle(self, handler_input):
        session_attrs = handler_input.attributes_manager.session_attributes
        # Reset quiz state
        session_attrs["in_quiz"] = True
        session_attrs["question_index"] = 0
        session_attrs["score"] = 0

        intro = "Let's start the quiz! "
        question_speech = build_question_speech(0)
        speech = intro + question_speech
        reprompt = "Say A, B, C, or D to answer."

        return (
            handler_input.response_builder
            .speak(speech)
            .ask(reprompt)
            .response
        )


class AnswerIntentHandler(AbstractRequestHandler):
    """Handles the user's answer during a quiz session."""

    def can_handle(self, handler_input):
        session_attrs = handler_input.attributes_manager.session_attributes
        # Only handle answers when a quiz is active
        return (
            ask_utils.is_intent_name("AnswerIntent")(handler_input)
            and session_attrs.get("in_quiz", False)
        )

    def handle(self, handler_input):
        session_attrs = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots

        # Get the user's choice slot value (resolved or raw)
        choice_slot = slots.get("choice")
        user_answer = None
        if choice_slot and choice_slot.value:
            user_answer = choice_slot.value.lower().strip()

        # Attempt to resolve synonym to canonical value (a/b/c/d)
        if choice_slot and choice_slot.resolutions:
            try:
                resolutions = choice_slot.resolutions.resolutions_per_authority
                if resolutions and resolutions[0].values:
                    user_answer = resolutions[0].values[0].value.name.lower().strip()
            except (AttributeError, IndexError):
                pass  # Fall back to raw slot value

        q_index = session_attrs.get("question_index", 0)
        score = session_attrs.get("score", 0)
        current_q = QUIZ_QUESTIONS[q_index]

        # Validate the answer
        if user_answer not in ("a", "b", "c", "d"):
            reprompt = "Please say A, B, C, or D."
            return (
                handler_input.response_builder
                .speak("I didn't catch that. " + reprompt)
                .ask(reprompt)
                .response
            )

        # Check correctness
        if user_answer == current_q["answer"]:
            result_speech = f"Correct! {current_q['explanation']}"
            score += 1
            session_attrs["score"] = score
        else:
            correct_letter = current_q["answer"].upper()
            correct_text = current_q["options"][current_q["answer"]]
            result_speech = (
                f"Not quite. The answer is {correct_letter}: {correct_text}. "
                f"{current_q['explanation']}"
            )

        # Move to next question or end quiz
        next_index = q_index + 1
        if next_index >= len(QUIZ_QUESTIONS):
            # Quiz complete
            session_attrs["in_quiz"] = False
            final_speech = build_final_score_speech(score)
            speech = result_speech + " " + final_speech
            return (
                handler_input.response_builder
                .speak(speech)
                .set_should_end_session(True)
                .response
            )
        else:
            session_attrs["question_index"] = next_index
            next_q_speech = build_question_speech(next_index)
            speech = result_speech + " " + next_q_speech
            reprompt = "Say A, B, C, or D to answer."
            return (
                handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .response
            )


class AnswerOutsideQuizHandler(AbstractRequestHandler):
    """Handles AnswerIntent when no quiz is active — redirects the user."""

    def can_handle(self, handler_input):
        session_attrs = handler_input.attributes_manager.session_attributes
        return (
            ask_utils.is_intent_name("AnswerIntent")(handler_input)
            and not session_attrs.get("in_quiz", False)
        )

    def handle(self, handler_input):
        speech = "There's no quiz running. Say quiz me to start one, or revise a topic."
        return (
            handler_input.response_builder
            .speak(speech)
            .ask(speech)
            .response
        )


class RevisionIntentHandler(AbstractRequestHandler):
    """Returns a spoken revision summary for the requested topic."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("RevisionIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        topic_slot = slots.get("topic")
        topic = None

        # Try resolved canonical value first
        if topic_slot and topic_slot.resolutions:
            try:
                resolutions = topic_slot.resolutions.resolutions_per_authority
                if resolutions and resolutions[0].values:
                    topic = resolutions[0].values[0].value.name.lower().strip()
            except (AttributeError, IndexError):
                pass

        # Fall back to raw slot value
        if not topic and topic_slot and topic_slot.value:
            topic = topic_slot.value.lower().strip()

        if topic and topic in REVISION_SUMMARIES:
            summary = REVISION_SUMMARIES[topic]
            speech = f"Here's a quick revision on {topic}. {summary} What else would you like to do?"
            reprompt = "Say quiz me to take a quiz, or revise another topic."
        else:
            speech = (
                "Which topic would you like to revise? "
                "You can choose acids and bases, light, electricity, "
                "life processes, or carbon compounds."
            )
            reprompt = "Please say a topic name, like electricity or light."

        return (
            handler_input.response_builder
            .speak(speech)
            .ask(reprompt)
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handles AMAZON.HelpIntent with friendly guidance."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speech = (
            "I'm Study Buddy Plus, your Class 10 Science helper! "
            "Say quiz me to test yourself with 10 questions, "
            "or say revise followed by a topic like light or electricity "
            "to hear a quick summary. What would you like?"
        )
        return (
            handler_input.response_builder
            .speak(speech)
            .ask("Say quiz me or revise a topic.")
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Handles AMAZON.CancelIntent and AMAZON.StopIntent — says goodbye."""

    def can_handle(self, handler_input):
        return (
            ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input)
            or ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input)
        )

    def handle(self, handler_input):
        speech = "Goodbye! Keep studying and you'll do great!"
        return (
            handler_input.response_builder
            .speak(speech)
            .set_should_end_session(True)
            .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Handles AMAZON.FallbackIntent — guides the user back on track."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        speech = (
            "I'm not sure about that. "
            "Try saying quiz me to start a quiz, "
            "or revise a topic like carbon compounds."
        )
        return (
            handler_input.response_builder
            .speak(speech)
            .ask("Say quiz me or revise a topic.")
            .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handles SessionEndedRequest — cleans up gracefully."""

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # Nothing to do — Alexa has already ended the session
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Global exception handler — logs the error and speaks a friendly message."""

    def can_handle(self, handler_input, exception):
        return True  # Catch everything

    def handle(self, handler_input, exception):
        logger.error("Unhandled exception: %s", exception, exc_info=True)
        speech = (
            "Sorry, something went wrong on my end. "
            "Please try again or say quiz me to restart."
        )
        return (
            handler_input.response_builder
            .speak(speech)
            .ask("Say quiz me or revise a topic.")
            .response
        )


# ── Skill Builder ─────────────────────────────────────────────────────────────
sb = SkillBuilder()

# Register all handlers in order of specificity
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(StartQuizIntentHandler())
sb.add_request_handler(AnswerIntentHandler())          # Must come before AnswerOutsideQuizHandler
sb.add_request_handler(AnswerOutsideQuizHandler())
sb.add_request_handler(RevisionIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

# Lambda entry point
lambda_handler = sb.lambda_handler()
