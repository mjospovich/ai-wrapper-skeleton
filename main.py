import os
import sys
import json
import yaml
import argparse
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from wrapper import process_input, process_output
from providers import OpenAIClient, AnthropicClient  # Import others as needed

# Load environment variables
load_dotenv()

# Load config
config_path = Path('config.yaml')
if not config_path.exists():
    print("Error: config.yaml not found. Please copy config.yaml.example to config.yaml and configure it.")
    sys.exit(1)

with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Get API keys from environment variables or config (env vars take precedence)
def get_api_key(provider: str) -> str:
    env_key_map = {
        'openai': 'OPENAI_API_KEY',
        'anthropic': 'ANTHROPIC_API_KEY',
        # Add more providers as needed
    }
    env_key = env_key_map.get(provider)
    if env_key and os.getenv(env_key):
        return os.getenv(env_key)
    return config['api_keys'].get(provider, '')

# Select provider based on config
provider_map = {
    'openai': OpenAIClient,
    'anthropic': AnthropicClient,
    # Add more providers as needed
}

provider_name = config['provider']
ClientClass = provider_map.get(provider_name)
if not ClientClass:
    raise ValueError(f"Invalid provider: {provider_name}. Available: {list(provider_map.keys())}")

api_key = get_api_key(provider_name)
if not api_key or api_key.startswith('YOUR_'):
    raise ValueError(f"API key for {provider_name} not set. Set {provider_name.upper()}_API_KEY env var or update config.yaml")

client = ClientClass(api_key, config['model'])

# FastAPI app
app = FastAPI(title="AI Wrapper API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "AI Wrapper API", "provider": provider_name, "model": config['model']}

@app.post("/generate")
async def generate(input_data: dict):
    try:
        prompt = process_input(input_data)
        raw_response = client.generate_response(prompt)
        output = process_output(raw_response)
        return output
    except ValueError as e:
        # Input validation errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Other errors (API failures, etc.)
        raise HTTPException(status_code=500, detail=str(e))

def run_cli(input_file: str = None):
    """Run as CLI script instead of API server"""
    if input_file:
        input_path = Path(input_file)
    else:
        input_path = Path(config['wrapper']['input_file'])
    
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    with open(input_path, 'r') as f:
        input_data = json.load(f)
    
    try:
        prompt = process_input(input_data)
        print(f"Prompt: {prompt}\n")
        raw_response = client.generate_response(prompt)
        print(f"Raw response: {raw_response}\n")
        output = process_output(raw_response)
        print(f"Processed output: {json.dumps(output, indent=2)}")
        
        # Save to outputs if configured
        outputs_dir = Path('outputs')
        outputs_dir.mkdir(exist_ok=True)
        output_file = outputs_dir / f"{input_path.stem}_output.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"\nOutput saved to: {output_file}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AI Wrapper - Custom AI API')
    parser.add_argument('--mode', choices=['api', 'cli'], default='api', help='Run mode: api (default) or cli')
    parser.add_argument('--input', type=str, help='Input file path (for CLI mode)')
    args = parser.parse_args()
    
    if args.mode == 'cli':
        run_cli(args.input)
    else:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=config['api']['port'])