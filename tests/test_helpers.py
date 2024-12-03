from app.utils.helpers import calculate_match_score, validate_regex

def test_validate_regex():
    assert validate_regex("simian adenovirus 27 (chimpanzee)") == "simian adenovirus 27 \\(chimpanzee\\)"
    assert validate_regex("hello world +[]()") == "hello world \\+\\[\\]\\(\\)"
    assert validate_regex("simian adenovirus 27 (chimpanzee)") != "simian adenovirus 27 (chimpanzee)"
    assert validate_regex("hello world +[]()") != "hello world +[]()"
    
def test_calculate_match_score():
    assert calculate_match_score("ABCDEFG", "ABCDEFG") == 3.00
    assert calculate_match_score("AAAA", "AABB") == 0.50 
    assert calculate_match_score("1234567", "ABCDEFG") == 0.00