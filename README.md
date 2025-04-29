# Secrets Manager for MCP Server

## Overview

`secrets_manager.py` is a Python utility that enables MCP servers to securely store and retrieve sensitive information using the system's native keychain/credential manager instead of relying on `.env` files. This approach significantly improves security by leveraging the operating system's built-in secure storage mechanisms.

## Key Features

- **Cross-Platform Support**: Works on macOS (Keychain), Windows (Credential Locker), and other platforms (using appropriate keyring backends)
- **Secure Storage**: Stores sensitive data like API keys in the system's secure credential storage
- **Simple API**: Provides straightforward functions for storing and retrieving secrets
- **Command-Line Interface**: Includes a CLI for managing secrets directly

## Core Functionality

### Secret Storage

The script uses the `keyring` library to store secrets in the system's native credential manager:

- On macOS: Stores secrets in the macOS Keychain
- On Windows: Uses the Windows Credential Locker
- On other platforms: Uses the best available keyring backend

### Main Functions

1. **`get_secret(service_name, secret_key)`**: Retrieves a secret from the system keyring
2. **`set_secret(service_name, secret_key, secret_value)`**: Stores a secret in the system keyring
3. **`setup_secrets()`**: Interactive function to collect and store initial secrets
4. **`test_get_secret()`**: Tests the retrieval of stored secrets
5. **`get_keyring_name()`**: Returns the name of the current keyring backend based on the platform

### Command-Line Interface

The script can be run directly with the following options:

- `--store`: Initiates the interactive secret storage process
- `--test`: Tests retrieving stored secrets
- `--info`: Displays information about the current keyring backend

## Usage Example

Instead of storing API keys in `.env` files:

```python
# Old approach with .env files
API_KEY = os.getenv("API_KEY")  # Insecure, stored in plaintext

# New approach with secrets_manager
from secrets_manager import get_secret
API_KEY = get_secret("MyMCPServer", "api_key")  # Secure, stored in system keychain
```

## Benefits for MCP Servers

1. **Enhanced Security**: Secrets are stored in the operating system's secure storage rather than in plaintext files
2. **Simplified Management**: No need to manage `.env` files or worry about them being accidentally committed to version control
3. **User-Friendly**: Provides an interactive interface for setting up secrets
4. **Reliable Access**: Consistent API for accessing secrets across different platforms

## Implementation Note

The script includes a commented example of how to access the stored secret directly from the macOS terminal:

```bash
security find-generic-password -l "MyMCPServer" -a "api_key" -g
```
