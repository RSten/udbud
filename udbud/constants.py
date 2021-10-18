import re

CLEANTEACH_VOCAB = [
    "clean",
    "tech",
]

CLEANTECH_COMPANIES = [
    "danfoss",
    "grundfoss",
    "forsyning",
]

CLEANTECH_COMPANY_REGEX = re.compile(
    r"|".join(CLEANTECH_COMPANIES),
    flags=re.IGNORECASE
)

CLEANTECH_VOCAB_REGEX = re.compile(
    r"|".join(CLEANTEACH_VOCAB),
    flags=re.IGNORECASE
)