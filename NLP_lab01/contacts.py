import re
# # # TODO Define other Regex here

mails = [
    (re.compile(r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})'), '$1@$2.$3'),
]

socials = [
    (re.compile(r'https://([a-zA-Z]+)\.com/([a-zA-Z0-9_/-]{11,})'), '$1:$2')
]

tels = [
    (re.compile(r'\((\d{3})\) (\d{2}) (\d{2}) (\d{2})'), '($1) $2 $3 $4'),
    (re.compile(r'(\d{3}) (\d{2}) (\d{2}) (\d{2})'), '($1) $2 $3 $4'),
    (re.compile(r'(\d{2})-(\d{2})-(\d{2})-(\d{2})'), '(0$1) $2 $3 $4'),
    # (re.compile(r'\+(\d{1,3}) (\d{2}) (\d{2}) (\d{2}) (\d{2})'), '+$1 $2 $3 $4 $5'),
    (re.compile(r'\((\d{3})\)\s*(\d{2})\s*(\d{2})\s*(\d{2})'), '($1) $2 $3 $4')
]
