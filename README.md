# voice-based-email-application📧🔊

## Overview

Welcome to the **voice-based-email-application** project! This system is designed to make email functionalities accessible to everyone, including visually impaired users. Our approach focuses on user-friendliness for all types of people, ensuring that everyone can easily access and manage their email through voice commands.

## Architecture Diagram

The system consists of the following major components:

- **User**: Initiates and interacts with the system using voice commands.
- **Web Server**: Connects the user with the email system, handles requests, processes data, and communicates with the Gmail database.
- **Text to Speech (TTS)**: Converts text into audio, providing audio feedback to users.
- **Predict Response**: Determines the appropriate response based on the user's input.
- **Intent Classification**: Classifies the user’s intent by analyzing their commands.
- **Speech to Text (STT)**: Converts spoken words into written text, also known as speech recognition.
- **Entity Recognition**: Identifies and categorizes key information within the text. This involves detecting named entities and categorizing them.
- **Gmail Database**: Stores user information, used for authentication and verification.

## Features

- **Voice-Activated Email**: Access and manage your email through voice commands.
- **Text to Speech**: Get audio output of email content and system responses.
- **Speech to Text**: Convert your spoken commands into written text for email actions.
- **Predictive Responses**: Receive relevant responses based on your commands.
- **Intent Classification**: Understand and classify the user’s intent for accurate action.
- **Entity Recognition**: Extract and categorize important information from the text.

## Getting Started

To get started with the Accessible Email Platform, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/PBL-Poject/voice-based-email-application
**Install Dependencies**:
cd accessible-email-platform
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

-pip install -r requirements.txt
-python manage.py runserver

**Architecture**
![architecture](https://github.com/user-attachments/assets/3f95f2f2-64c6-4f68-8052-422028733a66)

**Sequence Diagram**
![sequence](https://github.com/user-attachments/assets/20f6e030-34af-4269-a7ab-5ec342e13fbf)

**Some screenshots from Project**

![image1](https://github.com/user-attachments/assets/21e32d40-fad4-4cf4-8da6-aa5489c98142)

![images2](https://github.com/user-attachments/assets/9f8b7e4a-1f76-48e2-bfcb-1434fb999c02)

![images3](https://github.com/user-attachments/assets/9c6aec92-7cad-4128-b276-4c7b07f19a0c)

