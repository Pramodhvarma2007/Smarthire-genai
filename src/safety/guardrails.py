import difflib
import re
import unicodedata

MAX_LEN = 1000

KEY_VERBS = ["ignore", "disregard", "forget", "override", "bypass"]
REAL_WORDS = {"forge", "forged", "forgo", "forgot", "forgone", "ignora"}   # not typos, so never repaired

INJECTION_PATTERNS = [
    # telling the mentor to drop its rules
    r"\b(ignore|disregard|forget|override|bypass|stop following|do not follow|don't follow)\b"
    r".{0,30}\b(your|previous|prior|above|earlier|all|any|these|those)\b"
    r".{0,30}\b(instructions?|rules?|guidelines?|restrictions?|settings?|prompts?|programming)\b",
    r"\bforget (what|everything|all)\b.{0,25}\b(told|said|given|taught)\b",
    r"\bfrom now on\b.{0,25}\byou (have|are|can|will|must|should|answer)\b",
    r"\byour (new|real|true) (instructions?|rules?|role|task)\b",
    r"\b(you|an ai|the ai|ai)\b.{0,25}\bno (restrictions|rules|limits|filters|guidelines)\b",
    r"\b(ignora|ignore|ignorar|ignorer|ignoriere)\b.{0,30}\b(instrucciones|anweisungen|instruktionen|consignes)\b",
    # asking for the hidden instructions
    r"\b(system|hidden|initial|original|secret)\s+(prompt|instructions?|message)\b",
    r"\b(reveal|show|print|repeat|display|give me|tell me)\b.{0,30}\b(your|the)\b.{0,15}"
    r"\b(prompt|instructions|rules|guidelines)\b",
    r"\brepeat (everything|all|the text|the words) (above|before)\b",
    r"\bwhat (were|are) (you|your)\b.{0,30}\b(told|given|instructions)\b",
    r"\bwords you were given\b",
    # role-play and jailbreak tricks
    r"\byou are now (an?|the|my)\b.{0,30}\b(ai|assistant|bot|unrestricted|hacker|dan|friend)\b",
    r"\bpretend (to be|you are|you're)\b.{0,30}\b(no rules|without|unrestricted|different|another)\b",
    r"\bact as\b.{0,12}\b(dan|an? unrestricted|jailbroken)\b",
    r"\bplay (a )?(game|role)\b.{0,30}\byou (are|can|will)\b",
    r"\bimagine you (are|were)\b.{0,40}\b(anything|no rules)\b",
    r"\byou are not (a|an|the)\b.{0,20}\bmentor\b",
    r"\bjailbreak\b",
    r"\bdeveloper mode\b",
]
SELF_HARM_PATTERNS = [
    r"\bsuicide\b", r"kill myself", r"end my life", r"self[- ]harm",
    r"\bend it all\b", r"don'?t want to (live|be alive)", r"\bwant to die\b", r"hurt myself",
]
UNSAFE_PATTERNS = [
    r"(make|build) (a )?(bomb|weapon|explosive)",
    r"\b(hack|crack|break) into\b", r"\bhack someone\b",
    r"\bfake (resume|certificate|experience|degree|marksheet)",
    r"\b(forge|fabricate|counterfeit)\b.{0,20}\b(certificate|degree|marksheet|experience|document|letter|resume)\b",
    r"\bsteal\b.{0,20}\b(password|data|account|identity)\b",
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


def normalize(text):
    """Lower case, remove hidden characters, join letters spread out like 'i g n o r e',
    and repair small typos in the key words."""
    t = unicodedata.normalize("NFKC", text or "")
    t = re.sub(r"[\u200b-\u200f\u2060\ufeff]", "", t).lower()
    t = re.sub(r"\b(?:\w\s){3,}\w\b", lambda m: m.group(0).replace(" ", ""), t)
    words = []
    for w in t.split():
        core = re.sub(r"[^a-z]", "", w)
        fix = difflib.get_close_matches(core, KEY_VERBS, n=1, cutoff=0.8) if len(core) >= 5 and core not in REAL_WORDS else []
        words.append(fix[0] if fix else w)
    return " ".join(words)


def _matches(patterns, text):
    t = normalize(text)
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
