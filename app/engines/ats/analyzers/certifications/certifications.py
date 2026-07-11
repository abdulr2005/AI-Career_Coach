import re


# ==================================================
# TOP CERTIFICATION PROVIDERS
# ==================================================

TOP_PROVIDERS = {

    "aws": 2,

    "microsoft": 2,

    "google": 2,

    "meta": 2,

    "ibm": 2,

    "oracle": 2,

    "cisco": 2,

    "azure": 2,

    "tensorflow": 2,

    "huawei": 2,

    "red hat": 2,

    "kaggle": 1,

    "hackerrank": 1,

    "coursera": 1,

    "udemy": 1,

    "edx": 1,

    "datacamp": 1,

    "deeplearning.ai": 2

}


# ==================================================
# PROFESSIONAL CERTIFICATIONS
# ==================================================

PROFESSIONAL_CERTS = [

    "aws certified",

    "azure",

    "az-900",

    "ai-900",

    "dp-100",

    "google professional",

    "ccna",

    "ccnp",

    "mcsa",

    "oracle",

    "security+",

    "network+",

    "pmp"

]


# ==================================================
# MAIN ANALYZER
# ==================================================

def analyze_certifications(certification_text):

    if isinstance(certification_text, list):

        certification_text = "\n".join(certification_text)

    lower = certification_text.lower()

    providers = []

    provider_score = 0

    for provider, score in TOP_PROVIDERS.items():

        if provider in lower:

            providers.append(provider)

            provider_score += score

    professional = []

    for cert in PROFESSIONAL_CERTS:

        if cert in lower:

            professional.append(cert)

    cert_lines = [

        line.strip()

        for line in certification_text.splitlines()

        if line.strip()

    ]

    total_certifications = len(cert_lines)

    score = 0

    score += min(total_certifications, 4)

    score += min(provider_score, 4)

    score += min(len(professional), 2)

    score = min(score, 10)

    return {

        "total_certifications": total_certifications,

        "providers": sorted(list(set(providers))),

        "professional_certifications": sorted(list(set(professional))),

        "score": score

    }