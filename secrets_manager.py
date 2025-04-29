import keyring
import getpass
import argparse
import os
import platform
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get SERVICE_NAME from environment variables
SERVICE_NAME = os.getenv("SERVICE_NAME", "MyMCPServer")  # Default if not found

def get_secret(service_name, secret_key):
    """Retrieve a secret from system keyring."""
    try:
        secret = keyring.get_password(service_name, secret_key)
        if secret is None:
            raise KeyError(f"Secret '{secret_key}' not found in keyring for service '{service_name}'")
        return secret
    except Exception as e:
        print(f"Error accessing keyring: {e}")
        raise

def set_secret(service_name, secret_key, secret_value):
    """Store a secret in system keyring."""
    try:
        keyring.set_password(service_name, secret_key, secret_value)
        print(f"Secret '{secret_key}' stored successfully")
    except Exception as e:
        print(f"Error storing secret: {e}")
        raise

def setup_secrets():
    """Store initial secrets in keyring"""
    system = platform.system()
    print(f"Setting up secrets for {SERVICE_NAME} on {system}...")
    
    # Get secrets from user
    api_key = getpass.getpass("Enter API key: ")
    
    # Store in keyring
    keyring.set_password(SERVICE_NAME, "api_key", api_key)
    print(f"Secret stored successfully in {get_keyring_name()} for {SERVICE_NAME}")

def test_get_secret():
    """Test retrieving the stored secret"""
    try:
        system = platform.system()
        print(f"Retrieving secret for {SERVICE_NAME} from {get_keyring_name()}...")
        api_key = get_secret(SERVICE_NAME, "api_key")
        print(f"Retrieved API key: {api_key}")
    except Exception as e:
        print(f"Error retrieving secret: {e}")

def get_keyring_name():
    """Get the name of the current keyring backend"""
    system = platform.system()
    if system == "Darwin":
        return "macOS Keychain"
    elif system == "Windows":
        return "Windows Credential Locker"
    else:
        return keyring.get_keyring().__class__.__name__

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage secrets for Server")
    parser.add_argument("--store", action="store_true", help="Store secrets in keyring")
    parser.add_argument("--test", action="store_true", help="Test retrieving secrets")
    parser.add_argument("--info", action="store_true", help="Show keyring backend information")
    
    args = parser.parse_args()
    
    if args.info:
        print(f"Platform: {platform.system()}")
        print(f"Keyring backend: {get_keyring_name()}")
    elif args.store:
        setup_secrets()
    elif args.test:
        test_get_secret()
    else:
        print("Please specify an action: --store, --test, or --info")
        parser.print_help()
        
"""
security find-generic-password -l "MyMCPServer" -a "api_key" -g
"""