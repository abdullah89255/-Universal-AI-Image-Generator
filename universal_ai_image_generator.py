#!/usr/bin/env python3
"""
Example usage of Universal AI Image Generator
Shows various ways to use the generator programmatically
"""

from universal_ai_image_generator import UniversalImageGenerator
import time

# Example 1: Basic Usage with Single Provider
def example_basic():
    print("\n=== Example 1: Basic Usage ===\n")
    
    generator = UniversalImageGenerator("example_images")
    generator.add_provider('grok', 'your-grok-api-key-here')
    
    # Generate a single image
    filepath = generator.generate(
        provider='grok',
        prompt='a serene mountain landscape at sunset'
    )
    
    if filepath:
        print(f"✓ Image saved: {filepath}")


# Example 2: Multiple Providers
def example_multiple_providers():
    print("\n=== Example 2: Using Multiple Providers ===\n")
    
    generator = UniversalImageGenerator("multi_provider_images")
    
    # Add multiple providers
    generator.add_provider('openai', 'sk-your-openai-key')
    generator.add_provider('grok', 'xai-your-grok-key')
    generator.add_provider('stability', 'sk-your-stability-key')
    
    prompt = "a futuristic cityscape at night"
    
    # Generate same prompt with different providers
    print("Generating with OpenAI...")
    generator.generate('openai', prompt, model='dall-e-3')
    
    time.sleep(2)
    
    print("Generating with Grok...")
    generator.generate('grok', prompt)
    
    time.sleep(2)
    
    print("Generating with Stability AI...")
    generator.generate('stability', prompt, width=1024, height=1024)


# Example 3: Batch Generation
def example_batch_generation():
    print("\n=== Example 3: Batch Generation ===\n")
    
    generator = UniversalImageGenerator("batch_images")
    generator.add_provider('grok', 'your-grok-api-key-here')
    
    prompts = [
        "a peaceful zen garden",
        "abstract geometric patterns in blue and gold",
        "a cozy coffee shop interior",
        "northern lights over snowy mountains",
        "underwater coral reef scene"
    ]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\nGenerating image {i}/{len(prompts)}: {prompt}")
        filepath = generator.generate('grok', prompt)
        
        if filepath:
            print(f"✓ Saved: {filepath}")
        
        # Rate limiting
        if i < len(prompts):
            time.sleep(2)


# Example 4: Custom Settings for Each Provider
def example_custom_settings():
    print("\n=== Example 4: Provider-Specific Custom Settings ===\n")
    
    generator = UniversalImageGenerator("custom_settings_images")
    generator.add_provider('openai', 'sk-your-openai-key')
    generator.add_provider('grok', 'xai-your-grok-key')
    generator.add_provider('stability', 'sk-your-stability-key')
    
    # OpenAI with HD quality
    print("OpenAI DALL-E 3 - HD Quality:")
    generator.generate(
        provider='openai',
        prompt='a professional product photo of a watch',
        model='dall-e-3',
        size='1024x1024',
        quality='hd',
        style='natural'
    )
    
    time.sleep(2)
    
    # Grok with high quality
    print("\nGrok - High Quality:")
    generator.generate(
        provider='grok',
        prompt='an artistic portrait illustration',
        size='1024x1024',
        quality='high',
        style='vivid'
    )
    
    time.sleep(2)
    
    # Stability AI with custom parameters
    print("\nStability AI - Custom Parameters:")
    generator.generate(
        provider='stability',
        prompt='a dramatic landscape painting',
        width=1536,
        height=1024,
        steps=50,
        cfg_scale=10
    )


# Example 5: Error Handling
def example_error_handling():
    print("\n=== Example 5: Error Handling ===\n")
    
    generator = UniversalImageGenerator("error_handling_images")
    generator.add_provider('grok', 'your-grok-api-key-here')
    
    prompts = [
        "a beautiful landscape",
        "",  # Empty prompt - will fail
        "a city skyline",
    ]
    
    successful = 0
    failed = 0
    
    for prompt in prompts:
        if not prompt:
            print(f"⚠️  Skipping empty prompt")
            failed += 1
            continue
        
        print(f"\nGenerating: {prompt}")
        filepath = generator.generate('grok', prompt)
        
        if filepath:
            successful += 1
            print(f"✓ Success")
        else:
            failed += 1
            print(f"✗ Failed")
        
        time.sleep(1)
    
    print(f"\n📊 Results: {successful} successful, {failed} failed")


# Example 6: Different Image Sizes
def example_different_sizes():
    print("\n=== Example 6: Different Image Sizes ===\n")
    
    generator = UniversalImageGenerator("size_examples")
    generator.add_provider('grok', 'your-grok-api-key-here')
    
    prompt = "a minimalist logo design"
    
    sizes = ['512x512', '1024x1024', '1792x1024', '1024x1792']
    
    for size in sizes:
        print(f"\nGenerating {size} image...")
        generator.generate('grok', f"{prompt} - {size}", size=size)
        time.sleep(2)


# Example 7: Quality Comparison
def example_quality_comparison():
    print("\n=== Example 7: Quality Comparison ===\n")
    
    generator = UniversalImageGenerator("quality_comparison")
    generator.add_provider('grok', 'your-grok-api-key-here')
    
    prompt = "a detailed illustration of a dragon"
    qualities = ['low', 'medium', 'high']
    
    for quality in qualities:
        print(f"\nGenerating with {quality} quality...")
        generator.generate('grok', f"{prompt} - {quality}", quality=quality)
        time.sleep(2)


# Example 8: Creative Variations
def example_creative_variations():
    print("\n=== Example 8: Creative Variations ===\n")
    
    generator = UniversalImageGenerator("creative_variations")
    generator.add_provider('grok', 'your-grok-api-key-here')
    
    base_prompt = "a tree"
    
    variations = [
        "a tree in spring with cherry blossoms",
        "a tree in summer with lush green leaves",
        "a tree in autumn with golden foliage",
        "a tree in winter covered in snow"
    ]
    
    for variation in variations:
        print(f"\nGenerating: {variation}")
        generator.generate('grok', variation)
        time.sleep(2)


# Example 9: Using All Providers for Comparison
def example_provider_comparison():
    print("\n=== Example 9: Provider Comparison ===\n")
    
    generator = UniversalImageGenerator("provider_comparison")
    
    # Configure all providers
    generator.add_provider('openai', 'sk-your-openai-key')
    generator.add_provider('grok', 'xai-your-grok-key')
    generator.add_provider('stability', 'sk-your-stability-key')
    generator.add_provider('together', 'your-together-key')
    
    prompt = "a photorealistic portrait of a person"
    
    # Generate with each provider
    for provider in generator.providers.keys():
        print(f"\nGenerating with {provider}...")
        generator.generate(provider, prompt)
        time.sleep(3)


# Main function to run examples
def main():
    print("=" * 70)
    print("  UNIVERSAL AI IMAGE GENERATOR - EXAMPLES")
    print("=" * 70)
    print("\nThese examples show different ways to use the generator.")
    print("Make sure to replace API keys with your actual keys!\n")
    
    # Uncomment the examples you want to run:
    
    # example_basic()
    # example_multiple_providers()
    # example_batch_generation()
    # example_custom_settings()
    # example_error_handling()
    # example_different_sizes()
    # example_quality_comparison()
    # example_creative_variations()
    # example_provider_comparison()
    
    print("\n✓ Example script ready! Uncomment the examples you want to run.")


if __name__ == "__main__":
    main()
