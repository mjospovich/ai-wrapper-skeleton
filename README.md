# AI Wrapper Skeleton

A modular, Dockerized template repository for building custom AI API wrappers. Easily integrate and switch between providers like OpenAI (ChatGPT), Anthropic (Claude), and more. Configure with your API keys, define custom prompt logic, and deploy as a REST API for various use cases.

## Features

- 🔌 **Modular Provider System**: Switch between OpenAI, Anthropic, and more with a simple config change
- 🐳 **Docker Support**: Containerized setup for easy deployment and consistency
- 🔐 **Secure Configuration**: Support for environment variables and config files
- 🚀 **Dual Mode**: Run as a REST API or CLI script
- 🎯 **Customizable**: Easy-to-modify wrapper functions for your specific use case
- 📦 **Skeleton Template**: Clean starting point for your AI integration projects

## Quick Start (Docker Only)

### Prerequisites

- **Docker** and **Docker Compose** (that's all you need!)

### Setup in 3 Steps

1. **Clone and enter the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-wrapper-skeleton
   ```

2. **Create your config file**
   ```bash
   cp config.yaml.example config.yaml
   ```
   
   Then edit `config.yaml` and add your API key:
   ```yaml
   provider: openai
   api_keys:
     openai: your-actual-api-key-here
   model: gpt-4o-mini
   ```

3. **Start the API server**
   ```bash
   docker-compose up -d --build # or docker compose up -d --build 
   ```

That's it! The API will be running at `http://localhost:8000`

**Test it:**
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the capital of France?"}'
```

### Quick Customization

Once it's working, customize it for your use case:

1. **Edit `wrapper.py`** - This is the main file to customize:
   - `process_input()` - Transform your input data into an AI prompt
   - `process_output()` - Parse and format the AI response

2. **Restart Docker** - Changes to `wrapper.py` are automatically mounted:
   ```bash
   docker-compose restart
   ```

See the [Customization Example](#customization-example) section below for detailed examples.

### Alternative: Using Environment Variables

If you prefer environment variables for API keys (more secure), you still need to create `config.yaml` for provider/model settings, but you can skip adding the API key:

```bash
cp config.yaml.example config.yaml
# Edit config.yaml but leave api_keys as placeholders
# Then set environment variable:
export OPENAI_API_KEY="your-key-here"
docker-compose up
```

The environment variable will override the API key in the config file.

### Running Without Docker

If you have Python 3.11+ installed locally:
```bash
pip install -r requirements.txt
python main.py
```

## Usage

### API Mode (Default)

**With Docker:**
```bash
docker-compose up
```

**Without Docker:**
```bash
python main.py --mode api
```

The API will be available at `http://localhost:8000`

**Endpoints:**

- `GET /`: Health check and info
- `POST /generate`: Generate AI response

**Example API call:**
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the capital of France?"}'
```

**Response:**
```json
{
  "output": "The capital of France is Paris."
}
```

### CLI Mode

**With Docker:**
```bash
docker-compose run --rm ai-wrapper python main.py --mode cli --input inputs/example.json
```

**Without Docker:**
```bash
python main.py --mode cli --input inputs/example.json
```

Or use the default input file from config:
```bash
python main.py --mode cli
```

Outputs will be saved to the `outputs/` directory.

## Configuration

Edit `config.yaml` to customize:

```yaml
provider: openai  # Options: openai, anthropic
model: gpt-4o-mini  # Model name for the selected provider
api_keys:
  openai: YOUR_OPENAI_API_KEY
  anthropic: YOUR_ANTHROPIC_API_KEY
wrapper:
  input_file: inputs/example.json
  output_format: json
api:
  port: 8000
```

### Supported Providers

- **OpenAI**: Models like `gpt-4o-mini`, `gpt-4`, `gpt-3.5-turbo`
- **Anthropic**: Models like `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`

To add a new provider, create a new file in `providers/` following the `BaseAIClient` interface.

## Customization Example

Here's how to customize `wrapper.py` for a calorie estimation use case:

```python
def process_input(input_data: dict) -> str:
    food_items = ', '.join(input_data.get('food_items', []))
    prompt = f"Analyze these food items: {food_items}. Estimate total approximate calories for the day and return only the number (e.g., 1500)."
    return prompt

def process_output(raw_output: str) -> dict:
    try:
        calories = int(raw_output.strip())
        return {"total_calories": calories}
    except ValueError:
        return {"error": "Invalid output from AI"}
```

Then use it with:
```json
{
  "food_items": ["apple", "burger", "salad"]
}
```

## Project Structure

```
ai-wrapper-skeleton/
├── Dockerfile              # Docker container definition
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── config.yaml.example     # Example configuration (copy to config.yaml)
├── config.yaml            # Your configuration (gitignored)
├── main.py                # Entry point (API server or CLI)
├── wrapper.py             # Customizable wrapper logic
├── providers/             # AI provider implementations
│   ├── __init__.py
│   ├── base.py            # Base class interface
│   ├── openai.py          # OpenAI implementation
│   └── anthropic.py       # Anthropic implementation
├── inputs/                # Input files for CLI mode
│   └── example.json       # Example input
└── outputs/               # Output files (generated)
```

## Security Notes

- **Never commit `config.yaml`** with real API keys (it's gitignored)
- Prefer environment variables for API keys in production
- Use Docker secrets or environment variables in containerized deployments
- Review and customize `.gitignore` as needed

## Development

### Adding a New Provider

1. Create a new file in `providers/` (e.g., `providers/gemini.py`)
2. Implement the `BaseAIClient` interface:
   ```python
   from .base import BaseAIClient
   
   class GeminiClient(BaseAIClient):
       def __init__(self, api_key: str, model: str):
           # Initialize your client
           pass
       
       def generate_response(self, prompt: str) -> str:
           # Implement API call
           return response
   ```
3. Add it to `providers/__init__.py`
4. Add it to the `provider_map` in `main.py`
5. Update `config.yaml.example` with the new provider option

### Testing

**With Docker:**
```bash
# Start the API
docker-compose up -d

# Test the API
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, world!"}'

# Test CLI mode
docker-compose run --rm ai-wrapper python main.py --mode cli

# Stop the API
docker-compose down
```

**Without Docker:**
```bash
# Test API mode
python main.py --mode api
# In another terminal
curl -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"prompt": "Hello, world!"}'

# Test CLI mode
python main.py --mode cli --input inputs/example.json
```

## License

MIT License - see LICENSE file for details

## Contributing

This is a skeleton template. Fork it, customize it, and make it your own!
