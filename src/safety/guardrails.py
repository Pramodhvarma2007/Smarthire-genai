import re

MAX_LEN = 1000

INJECTION_PATTERNS = [
    r"ignore (all |any )?(the )?(previous|above|prior) (instructions|rules|prompts?)",
    r"disregard (all |any )?(the )?(previous|above|prior)",
    r"forget (everything|all|your) (instructions|rules)",
    r"(reveal|show|print|tell me) (me )?(your |the )?(system )?(prompt|instructions)",
    r"you are now",
    r"pretend (to be|you are)",
    r"act as (an? )?(unrestricted|dan)",
    r"jailbreak",
    r"developer mode",
]
SELF_HARM_PATTERNS = [
    r"\bsuicide\b", r"kill myself", r"end my life", r"self[- ]harm",
]
UNSAFE_PATTERNS = [
    r"(make|build) (a )?(bomb|weapon|explosive)",
    r"\bhack (into|someone)",
    r"\bfake (resume|certificate|experience|degree|marksheet)",
    r"(kill|hurt|harm) (someone|people)",
]

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?\d{1,3}[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)")

MESSAGES = {
    "empty": "Please type a question.",
    "too_long": "That message is too long. Please keep it under 1000 characters.",
    "injection": "I can't follow instructions that try to change how I work. Please ask a career question.",
    "self_harm": ("I'm sorry you're feeling this way. I'm only a career helper, so I can't help "
                  "with this, but please talk to someone you trust or a local helpline."),
    "unsafe": "I can't help with that. I can help with careers, skills, resumes and jobs.",
}


def _matches(patterns, text):
    t = text.lower()
    return any(re.search(p, t) for p in patterns)


def find_email(text):
    m = EMAIL_RE.search(text)
    return m.group(0) if m else ""


def mask_pii(text):
    """Hide emails and phone numbers before text goes to the AI model."""
    text, n_email = EMAIL_RE.subn("[EMAIL]", text)
    text, n_phone = PHONE_RE.subn("[PHONE]", text)
    return text, n_email + n_phone


def has_injection(text):
    return _matches(INJECTION_PATTERNS, text)


def check_input(text):
    """Check a chat message. Returns ok, reason, message and a cleaned copy."""
    text = (text or "").strip()
    reason = None
    if not text:
        reason = "empty"
    elif len(text) > MAX_LEN:
        reason = "too_long"
    elif _matches(INJECTION_PATTERNS, text):
        reason = "injection"
    elif _matches(SELF_HARM_PATTERNS, text):
        reason = "self_harm"
    elif _matches(UNSAFE_PATTERNS, text):
        reason = "unsafe"
    if reason:
        return {"ok": False, "reason": reason, "message": MESSAGES[reason], "clean_text": ""}
    clean, _ = mask_pii(text)
    return {"ok": True, "reason": None, "message": "", "clean_text": clean}