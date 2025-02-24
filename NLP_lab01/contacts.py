import re

mails = [
    (re.compile(r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})'), '$1@$2.$3'),
]

socials = [
    (re.compile(r'facebook\.com/(([^/\'\"]+))/?[\"\']'),'facebook:$1'),
    (re.compile(r"twitter\.com\/(([^/\'\"]+))/?[\"\']"), 'twitter:$1'),
    (re.compile(r'instagram\.com/(([^/\'\"]+))/?'),'instagram:$1'),
    (re.compile(r"https?://(www\.)?linkedin\.com/company/([A-Za-z0-9-]+)"),"linkedin:$2",),
    (re.compile(r'youtube\.com/channel/(([^/\'\"]+))?[\"\']'), 'youtube:$1'), 
]

tels = [
    # Landline Numbers (No Alternatives)
    (
        re.compile(r"\(?0([2-4][1-9])\)?[\s.-]*(\d{2})[\s.-]*(\d{2})[\s.-]*(\d{2})"),
        "(0$1) $2 $3 $4"
    ),
    (
        re.compile(r"\+213[\s.-]*\(0\)[\s.-]*([2-4][1-9])[\s.-]*(\d{2})[\s.-]*(\d{2})[\s.-]*(\d{2})"),
        "(0$1) $2 $3 $4"
    ),
    (
        re.compile(r"\+213[\s.-]*([2-4][1-9])[\s.-]*(\d{2})[\s.-]*(\d{2})[\s.-]*(\d{2})"),
        "(0$1) $2 $3 $4"
    ),
    (
        re.compile(r"00213[\s.-]*([2-4][1-9])[\s.-]*(\d{2})[\s.-]*(\d{2})[\s.-]*(\d{2})"),
        "(0$1) $2 $3 $4"
    ),

    # Mobile Numbers (No Alternatives)
    (
        re.compile(r"\(?0([567]\d{2})\)?[\s.-]*(\d{2})[\s.-]*(\d{2})[\s.-]*(\d{2})"),
        "(0$1) $2 $3 $4"
    ),
    (
        re.compile(r"\+213[\s.-]*([567]\d{2})[\s.-]*(\d{2})[\s.-]*(\d{2})[\s.-]*(\d{2})"),
        "(0$1) $2 $3 $4"
    ),

    # Landline Numbers with One Alternative (e.g., "32/41" or "32 ou 41")
    (
        re.compile(r"\(?0([2-4][1-9])\)?[\s.-]*(\d{2})[\s.-]*(\d{2})[\s.-]*(\d{2})[\s.-]*(?:/|ou|a)[\s.-]*(\d{2})"),
        ["(0$1) $2 $3 $4", "(0$1) $2 $3 $5"]
    ),

    # Landline Numbers with Two Alternatives (e.g., "32 ou 41 ou 51")
    (
        re.compile(r"\(?0([2-4][1-9])\)?[\s.-]*(\d{2})[\s.-]*(\d{2})[\s.-]*(\d{2})[\s.-]*(?:/|ou|a)[\s.-]*(\d{2})[\s.-]*(?:/|ou|a)[\s.-]*(\d{2})"),
        ["(0$1) $2 $3 $4", "(0$1) $2 $3 $5", "(0$1) $2 $3 $6"]
    ),

    # Mobile Numbers with One Alternative
    (
        re.compile(r"\(?0([567]\d{2})\)?[\s.-]*(\d{2})[\s.-]*(\d{2})[\s.-]*(\d{2})[\s.-]*(?:/|ou|a)[\s.-]*(\d{2})"),
        ["(0$1) $2 $3 $4", "(0$1) $2 $3 $5"]
    ),

    # Mobile Numbers with Two Alternatives
    (
        re.compile(r"\(?0([567]\d{2})\)?[\s.-]*(\d{2})[\s.-]*(\d{2})[\s.-]*(\d{2})[\s.-]*(?:/|ou|a)[\s.-]*(\d{2})[\s.-]*(?:/|ou|a)[\s.-]*(\d{2})"),
        ["(0$1) $2 $3 $4", "(0$1) $2 $3 $5", "(0$1) $2 $3 $6"]
    ),
]
