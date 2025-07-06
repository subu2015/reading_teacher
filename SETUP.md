# Reading Teacher 2.0 Setup Guide

## Setting up OpenAI API Key

The application requires an OpenAI API key to generate stories and illustrations. Here's how to set it up:

### Option 1: Environment Variable (Recommended)

1. Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Set it as an environment variable:

```bash
export OPENAI_API_KEY="your-actual-api-key-here"
```

### Option 2: .env File (Development)

1. Create a `.env` file in the project directory:
```bash
echo 'OPENAI_API_KEY=your-actual-api-key-here' > .env
```

2. Replace `your-actual-api-key-here` with your actual OpenAI API key

### Option 3: Permanent Setup

Add to your shell profile for permanent setup:

```bash
echo 'export OPENAI_API_KEY="your-actual-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## Testing the Setup

Run the test script to verify your API key works:

```bash
python test_api.py
```

You should see: "✅ API Test successful: Hello, API is working!"

## Running the Application

Once the API key is set, run the application:

```bash
streamlit run main_app.py
```

## Troubleshooting

- If you get "OPENAI_API_KEY environment variable is not set", make sure you've set the API key
- If you get API errors, check that your API key is valid and has sufficient credits
- Make sure you're in the correct directory (`reading_teacher_2`) when running commands 