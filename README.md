# AI Wrapper Skeleton

A modular, Dockerized template repository for building custom AI API wrappers. Easily integrate and switch between providers like OpenAI (ChatGPT), Anthropic (Claude), and more. Configure with your API keys, define custom prompt logic, and deploy as a REST API for various use cases.

## Features

- 🔌 **Modular Provider System**: Switch between OpenAI, Anthropic, and more with a simple config change
- 🐳 **Docker Support**: Containerized setup for easy deployment and consistency
- 🔐 **Secure Configuration**: Support for environment variables and config files
- 🚀 **Dual Mode**: Run as a REST API or CLI script
- 🎯 **Customizable**: Easy-to-modify wrapper functions for your specific use case
- 📦 **Skeleton Template**: Clean starting point for your AI integration projects

## Quick Start

### Prerequisites

- Docker and Docker Compose (recommended), or
- Python 3.11+ with pip

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-wrapper-skeleton
   ```

2. **Configure your API keys**

   **Option A: Environment Variables (Recommended)**
   ```bash
   export OPENAI_API_KEY="your-key-here"
   # or
   export ANTHROPIC_API_KEY="your-key-here"
   ```

   **Option B: Config File**
   ```bash
   cp config.yaml.example config.yaml
   # Edit config.yaml and add your API keys
   ```

3. **Customize the wrapper** (optional)
   
   Edit `wrapper.py` to implement your custom logic:
   - `process_input()`: Transform your input data into a prompt
   - `process_output()`: Parse and format the AI response

4. **Run with Docker** (recommended)
   ```bash
   docker-compose up
   ```

   Or build and run manually:
   ```bash
   docker build -t ai-wrapper .
   docker run -p 8000:8000 -e OPENAI_API_KEY=your-key ai-wrapper
   ```

5. **Run without Docker**
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

## Usage

### API Mode (Default)

Start the API server:
```bash
python main.py --mode api
# or with Docker
docker-compose up
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

### CLI Mode

Run as a command-line script:
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
  input_file: inputs/prompt.json
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

```bash
# Test API mode
python main.py --mode api
# In another terminal
curl -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"prompt": "test"}'

# Test CLI mode
python main.py --mode cli --input inputs/example.json
```

## License

MIT License - see LICENSE file for details

## Contributing

This is a skeleton template. Fork it, customize it, and make it your own!
