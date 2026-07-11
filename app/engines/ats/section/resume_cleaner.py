import re


# ==================================================
# HEADER PATTERNS
# ==================================================

HEADER_PATTERNS = [

    r"\+?\d[\d\s\-\(\)]{8,}",

    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

    r"linkedin",

    r"github",

    r"portfolio",

    r"http",

    r"https",

    r"www\."

]


# ==================================================
# REMOVE HEADER
# ==================================================

def remove_header(cv_text: str):

    lines = cv_text.splitlines()

    cleaned = []

    header_finished = False

    for line in lines:

        raw = line.strip()

        if not raw:
            continue

        if not header_finished:

            lower = raw.lower()

            if any(
                re.search(pattern, lower)
                for pattern in HEADER_PATTERNS
            ):
                continue

            if len(raw.split()) >= 4:

                header_finished = True

        cleaned.append(raw)

    return "\n".join(cleaned)


# ==================================================
# EXTRACT SUMMARY
# ==================================================

def extract_summary(cv_text: str):

    lines = cv_text.splitlines()

    summary = []

    remaining = []

    inside_summary = False

    for line in lines:

        raw = line.strip()

        if not raw:
            continue

        lower = raw.lower()

        if any(

            title in lower

            for title in [

                "summary",

                "professional summary",

                "profile",

                "about me",

                "career objective"

            ]

        ):

            inside_summary = True

            continue

        if inside_summary:

            if (

                raw.isupper()

                and len(raw.split()) <= 5

            ):

                inside_summary = False

                remaining.append(raw)

                continue

            summary.append(raw)

            continue

        remaining.append(raw)

    return (

        "\n".join(summary).strip(),

        "\n".join(remaining).strip()

    )


# ==================================================
# REMOVE EMPTY LINES
# ==================================================

def remove_extra_spaces(text):

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if line:

            lines.append(line)

    return "\n".join(lines)


# ==================================================
# MAIN CLEANER
# ==================================================

# ==================================================
# MAIN CLEANER
# ==================================================

def clean_resume(cv_text: str):

    text = remove_header(cv_text)

    summary, _ = extract_summary(text)

    text = remove_extra_spaces(text)

    return {

        "summary": summary,

        "clean_text": text

    }