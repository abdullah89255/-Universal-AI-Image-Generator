#!/usr/bin/env python3
"""
Universal AI Image Generator - Standalone Version
Supports: OpenAI DALL-E, Grok, Stability AI, Replicate, Together AI
"""

import os
import requests
import json
from datetime import datetime
from pathlib import Path
import time
import base64
from typing import Optional, Dict, Any


class UniversalImageGenerator:
    def __init__(self, download_folder="ai_generated_images"):
        """Initialize the Universal Image Generator"""
        self.download_folder = download_folder
        self.providers = {}
        Path(self.download_folder).mkdir(parents=True, exist_ok=True)
        print(f"✓ Download folder: {self.download_folder}")
    
    def add_provider(self, provider_name: str, api_key: str):
        """Add an API provider"""
        self.providers[provider_name.lower()] = api_key
        print(f"✓ Added provider: {provider_name}")
    
    def generate_openai(self, prompt: str, model="dall-e-3", size="1024x1024", 
                       quality="standard", style="vivid") -> Optional[Dict]:
        """Generate image using OpenAI DALL-E"""
        if 'openai' not in self.providers:
            print("❌ OpenAI API key not configured")
            return None
        
        headers = {
            "Authorization": f"Bearer {self.providers['openai']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "prompt": prompt,
            "n": 1,
            "size": size
        }
        
        if model == "dall-e-3":
            payload["quality"] = quality
            payload["style"] = style
        
        try:
            print(f"🎨 Generating with OpenAI {model}...")
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return {
                'url': data['data'][0]['url'],
                'provider': 'openai',
                'model': model
            }
        except Exception as e:
            print(f"❌ OpenAI Error: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None
    
    def generate_grok(self, prompt: str, model="grok-2-vision-1212", size="1024x1024",
                     quality="medium", style="natural") -> Optional[Dict]:
        """Generate image using Grok (X.AI)"""
        if 'grok' not in self.providers:
            print("❌ Grok API key not configured")
            return None
        
        headers = {
            "Authorization": f"Bearer {self.providers['grok']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "prompt": prompt,
            "n": 1,
            "size": size,
            "quality": quality,
            "style": style
        }
        
        try:
            print(f"🎨 Generating with Grok...")
            response = requests.post(
                "https://api.x.ai/v1/images/generations",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return {
                'url': data['data'][0]['url'],
                'provider': 'grok',
                'model': model
            }
        except Exception as e:
            print(f"❌ Grok Error: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None
    
    def generate_stability(self, prompt: str, model="stable-diffusion-xl-1024-v1-0",
                          width=1024, height=1024, steps=30, cfg_scale=7) -> Optional[Dict]:
        """Generate image using Stability AI"""
        if 'stability' not in self.providers:
            print("❌ Stability AI API key not configured")
            return None
        
        headers = {
            "Authorization": f"Bearer {self.providers['stability']}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": cfg_scale,
            "height": height,
            "width": width,
            "steps": steps,
            "samples": 1
        }
        
        try:
            print(f"🎨 Generating with Stability AI...")
            response = requests.post(
                f"https://api.stability.ai/v1/generation/{model}/text-to-image",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            image_data = data['artifacts'][0]['base64']
            return {
                'base64': image_data,
                'provider': 'stability',
                'model': model
            }
        except Exception as e:
            print(f"❌ Stability AI Error: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None
    
    def generate_replicate(self, prompt: str, model="stability-ai/sdxl",
                          width=1024, height=1024, num_inference_steps=25) -> Optional[Dict]:
        """Generate image using Replicate"""
        if 'replicate' not in self.providers:
            print("❌ Replicate API key not configured")
            return None
        
        headers = {
            "Authorization": f"Token {self.providers['replicate']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "version": model,
            "input": {
                "prompt": prompt,
                "width": width,
                "height": height,
                "num_inference_steps": num_inference_steps
            }
        }
        
        try:
            print(f"🎨 Generating with Replicate...")
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            prediction_url = data['urls']['get']
            while True:
                time.sleep(2)
                status_response = requests.get(prediction_url, headers=headers)
                status_data = status_response.json()
                
                if status_data['status'] == 'succeeded':
                    return {
                        'url': status_data['output'][0] if isinstance(status_data['output'], list) else status_data['output'],
                        'provider': 'replicate',
                        'model': model
                    }
                elif status_data['status'] == 'failed':
                    print(f"❌ Generation failed: {status_data.get('error')}")
                    return None
                
                print("⏳ Waiting...")
        except Exception as e:
            print(f"❌ Replicate Error: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None
    
    def generate_together(self, prompt: str, model="black-forest-labs/FLUX.1-schnell",
                         width=1024, height=1024, steps=4) -> Optional[Dict]:
        """Generate image using Together AI"""
        if 'together' not in self.providers:
            print("❌ Together AI API key not configured")
            return None
        
        headers = {
            "Authorization": f"Bearer {self.providers['together']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "prompt": prompt,
            "width": width,
            "height": height,
            "steps": steps,
            "n": 1
        }
        
        try:
            print(f"🎨 Generating with Together AI...")
            response = requests.post(
                "https://api.together.xyz/v1/images/generations",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return {
                'url': data['data'][0]['url'],
                'provider': 'together',
                'model': model
            }
        except Exception as e:
            print(f"❌ Together AI Error: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None
    
    def download_image(self, result: Dict, prompt: str) -> Optional[str]:
        """Download image and save to folder"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt[:50] if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_prompt = safe_prompt.replace(' ', '_')
            provider = result.get('provider', 'unknown')
            filename = f"{timestamp}_{provider}_{safe_prompt}.png"
            filepath = os.path.join(self.download_folder, filename)
            
            if 'url' in result:
                print(f"⬇️  Downloading...")
                img_response = requests.get(result['url'])
                img_response.raise_for_status()
                image_data = img_response.content
            elif 'base64' in result:
                print(f"⬇️  Decoding...")
                image_data = base64.b64decode(result['base64'])
            else:
                print("❌ No image data")
                return None
            
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            print(f"✓ Saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Download error: {e}")
            return None
    
    def generate(self, provider: str, prompt: str, **kwargs) -> Optional[str]:
        """Generate and download image"""
        provider = provider.lower()
        
        if provider == 'openai':
            result = self.generate_openai(prompt, **kwargs)
        elif provider == 'grok':
            result = self.generate_grok(prompt, **kwargs)
        elif provider == 'stability':
            result = self.generate_stability(prompt, **kwargs)
        elif provider == 'replicate':
            result = self.generate_replicate(prompt, **kwargs)
        elif provider == 'together':
            result = self.generate_together(prompt, **kwargs)
        else:
            print(f"❌ Unknown provider: {provider}")
            return None
        
        if result:
            return self.download_image(result, prompt)
        return None


def main():
    """Main interactive function"""
    
    print("=" * 70)
    print("  UNIVERSAL AI IMAGE GENERATOR")
    print("  OpenAI | Grok | Stability | Replicate | Together")
    print("=" * 70)
    
    download_folder = input("\n📁 Download folder (default: 'ai_images'): ").strip()
    if not download_folder:
        download_folder = "ai_images"
    
    generator = UniversalImageGenerator(download_folder)
    
    print("\n" + "=" * 70)
    print("CONFIGURE PROVIDERS (press Enter to skip)")
    print("=" * 70)
    
    providers_config = {
        'openai': 'OpenAI DALL-E',
        'grok': 'Grok (X.AI)',
        'stability': 'Stability AI',
        'replicate': 'Replicate',
        'together': 'Together AI'
    }
    
    for key, name in providers_config.items():
        api_key = input(f"\n🔑 {name} API key: ").strip()
        if api_key:
            generator.add_provider(key, api_key)
    
    if not generator.providers:
        print("\n❌ No providers configured!")
        return
    
    print("\n" + "=" * 70)
    print(f"✓ Ready! Providers: {', '.join(generator.providers.keys())}")
    print("Type 'quit' to exit")
    print("=" * 70)
    
    image_count = 0
    
    while True:
        print("\n" + "-" * 70)
        
        if len(generator.providers) > 1:
            provider = input(f"\n🤖 Provider ({'/'.join(generator.providers.keys())}): ").strip().lower()
            if provider not in generator.providers:
                provider = list(generator.providers.keys())[0]
                print(f"Using: {provider}")
        else:
            provider = list(generator.providers.keys())[0]
            print(f"\n🤖 Provider: {provider}")
        
        prompt = input("💭 Prompt (or 'quit'): ").strip()
        
        if prompt.lower() in ['quit', 'exit', 'q']:
            print(f"\n✓ Generated {image_count} images. Goodbye!")
            break
        
        if not prompt:
            print("⚠️  Empty prompt!")
            continue
        
        kwargs = {}
        custom = input("Custom settings? (y/n): ").strip().lower()
        
        if custom == 'y':
            if provider == 'openai':
                model = input("  Model (dall-e-2/dall-e-3): ").strip()
                if model: kwargs['model'] = model
                size = input("  Size (1024x1024/1792x1024/1024x1792): ").strip()
                if size: kwargs['size'] = size
                
            elif provider == 'grok':
                size = input("  Size (1024x1024/1792x1024/etc): ").strip()
                if size: kwargs['size'] = size
                quality = input("  Quality (low/medium/high): ").strip()
                if quality: kwargs['quality'] = quality
                
            elif provider == 'stability':
                width = input("  Width (1024): ").strip()
                if width: kwargs['width'] = int(width)
                height = input("  Height (1024): ").strip()
                if height: kwargs['height'] = int(height)
        
        filepath = generator.generate(provider, prompt, **kwargs)
        
        if filepath:
            image_count += 1
            print(f"\n✅ Total: {image_count}")
        else:
            print("\n⚠️  Failed!")
        
        time.sleep(1)


if __name__ == "__main__":
    main()
