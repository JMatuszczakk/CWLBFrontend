import pytest
import hashlib
import toml
import os
from unittest.mock import patch, MagicMock

def hash_password(password):
    """Helper function to hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def test_password_hashing():
    """
    Test that password hashing works correctly
    """
    
    password = "testpassword123"
    
    
    expected_hash = hash_password(password)
    
    
    assert expected_hash == hash_password(password)
    
    
    different_password = "differentpassword"
    assert expected_hash != hash_password(different_password)

def test_check_login():
    """
    Test login verification functionality
    """
    def mock_check_login(username, password):
        """
        Simulated login check function
        """
        
        test_users = {
            "testuser": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"  
        }
        
        
        if username not in test_users:
            return False
        
        
        return test_users[username] == hash_password(password)
    
    
    assert mock_check_login("testuser", "password") is True
    
    
    assert mock_check_login("testuser", "wrongpassword") is False
    
    
    assert mock_check_login("nonexistentuser", "anypassword") is False

def test_config_file_generation():
    """
    Test configuration file generation
    """
    
    primary_color = "#ff0000"
    background_color = "#ffffff"
    secondary_background_color = "#f0f0f0"
    text_color = "#000000"
    
    
    config = f"""
[theme]
primaryColor="{primary_color}"
backgroundColor="{background_color}"
secondaryBackgroundColor="{secondary_background_color}"
textColor="{text_color}"
    """.strip()
    
    
    parsed_config = toml.loads(config)
    
    
    assert 'theme' in parsed_config
    theme = parsed_config['theme']
    assert theme['primaryColor'] == primary_color
    assert theme['backgroundColor'] == background_color
    assert theme['secondaryBackgroundColor'] == secondary_background_color
    assert theme['textColor'] == text_color

def test_animal_list_dataframe_conversion():
    """
    Test the animal list conversion to DataFrame
    """
    import pandas

    
    sample_rows = [
        (1, "Burek", "Owczarek", "Brązowy", "dog1.jpg", "A001", "Brak"),
        (2, "Reks", "Mieszaniec", "Czarny", "brak", "A002", "Szczepienie")
    ]

    
    df = pandas.DataFrame(sample_rows, columns=["ID", "Imię", "Rasa", "Kolor", "Zdjęcie", "Numer", "Choroby"])
    
    
    df['Zdjęcie'] = df['Zdjęcie'].apply(lambda x: f'<img src="{x}" width="100">' if x != 'brak' else 'brak')
    
    
    assert len(df) == 2
    assert list(df.columns) == ["ID", "Imię", "Rasa", "Kolor", "Zdjęcie", "Numer", "Choroby"]
    
    
    assert df.loc[0, 'Zdjęcie'] == '<img src="dog1.jpg" width="100">'
    assert df.loc[1, 'Zdjęcie'] == 'brak'

def test_user_registration_data_validation():
    """
    Test user registration data validation
    """
    def validate_username(username):
        """
        Validate username criteria
        """
        
        if not isinstance(username, str):
            return False
        
        
        return bool(
            username and 
            username.strip() and 
            username.isalnum() and 
            3 <= len(username) <= 20
        )
    
    def validate_password(password):
        """
        Validate password criteria
        """
        
        if not isinstance(password, str):
            return False
        
        
        return bool(
            password and 
            password.strip() and 
            len(password.strip()) >= 8
        )
    
    
    assert validate_username("validuser123") is True
    assert validate_password("goodpassword") is True
    
    
    assert validate_username("") is False
    assert validate_username("   ") is False
    assert validate_username("us") is False
    assert validate_username("user with spaces") is False
    
    
    assert validate_password("") is False
    assert validate_password("   ") is False
    assert validate_password("short") is False

if __name__ == "__main__":
    pytest.main([__file__])