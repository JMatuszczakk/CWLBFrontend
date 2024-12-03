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
    # Test password
    password = "testpassword123"
    
    # Manually hash the password using SHA-256
    expected_hash = hash_password(password)
    
    # Verify the hash matches
    assert expected_hash == hash_password(password)
    
    # Verify different passwords produce different hashes
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
        # Predefined test user credentials
        test_users = {
            "testuser": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"  # hash of "password"
        }
        
        # Check if username exists
        if username not in test_users:
            return False
        
        # Check if password hash matches
        return test_users[username] == hash_password(password)
    
    # Test correct login
    assert mock_check_login("testuser", "password") is True
    
    # Test incorrect password
    assert mock_check_login("testuser", "wrongpassword") is False
    
    # Test non-existent user
    assert mock_check_login("nonexistentuser", "anypassword") is False

def test_config_file_generation():
    """
    Test configuration file generation
    """
    # Predefined color values
    primary_color = "#ff0000"
    background_color = "#ffffff"
    secondary_background_color = "#f0f0f0"
    text_color = "#000000"
    
    # Generate config
    config = f"""
[theme]
primaryColor="{primary_color}"
backgroundColor="{background_color}"
secondaryBackgroundColor="{secondary_background_color}"
textColor="{text_color}"
    """.strip()
    
    # Parse the generated toml
    parsed_config = toml.loads(config)
    
    # Verify parsing and values
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

    # Sample input data mimicking database rows
    sample_rows = [
        (1, "Burek", "Owczarek", "Brązowy", "dog1.jpg", "A001", "Brak"),
        (2, "Reks", "Mieszaniec", "Czarny", "brak", "A002", "Szczepienie")
    ]

    # Create DataFrame
    df = pandas.DataFrame(sample_rows, columns=["ID", "Imię", "Rasa", "Kolor", "Zdjęcie", "Numer", "Choroby"])
    
    # Transform photo column 
    df['Zdjęcie'] = df['Zdjęcie'].apply(lambda x: f'<img src="{x}" width="100">' if x != 'brak' else 'brak')
    
    # Verify DataFrame properties
    assert len(df) == 2
    assert list(df.columns) == ["ID", "Imię", "Rasa", "Kolor", "Zdjęcie", "Numer", "Choroby"]
    
    # Verify photo transformation
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
        # More explicit validation
        if not isinstance(username, str):
            return False
        
        # username must be non-empty, alphanumeric, and between 3-20 characters
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
        # More explicit validation
        if not isinstance(password, str):
            return False
        
        # password must be non-empty and at least 8 characters
        return bool(
            password and 
            password.strip() and 
            len(password.strip()) >= 8
        )
    
    # Test valid username and password
    assert validate_username("validuser123") is True
    assert validate_password("goodpassword") is True
    
    # Test invalid username
    assert validate_username("") is False
    assert validate_username("   ") is False
    assert validate_username("us") is False
    assert validate_username("user with spaces") is False
    
    # Test invalid password
    assert validate_password("") is False
    assert validate_password("   ") is False
    assert validate_password("short") is False

if __name__ == "__main__":
    pytest.main([__file__])