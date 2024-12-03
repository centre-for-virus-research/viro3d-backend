from difflib import SequenceMatcher

def calculate_match_score(name: str, query: str) -> float:
        match = SequenceMatcher(None, name.lower(), query.lower())
        # Combine metrics: ratio score from SequenceMatcher, exact substring position, length closeness
        score = match.ratio()  # Base score by similarity ratio
        position = name.lower().find(query.lower())
        if position >= 0:
            score += 1 - (position / len(name))  # Boost if substring found early
            score += len(query) / len(name)  # Boost if query length is close to name length
        return score

#if a query contains square brackets, regular brackets or '+'s they need to be escaped with the validate_regex function as regex search in mongodb wont recoginse them otherwise
def validate_regex(str: str) -> str:
    new_str = str
    for c in ['+', '[', ']', '(', ')']:
        if c in str:
            new_str = new_str.replace(c, "\\" + c) 
    return new_str