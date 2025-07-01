import os
import json
import glob
from typing import Dict, Any

class PromptContributor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config.get('extracting', {})
        self.prompt_config = self.config.get('prompt', {})

    def _load_file_content(self, filepath: str) -> str:
        """Loads content from a given file path."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading file {filepath}: {e}")
            return ""

    def _construct_prompt(self, example_content: str, document_content: str, template_content: str) -> Dict[str, str]:
        """Constructs the prompt using the template, example, and document content, separating system and user parts."""
        # Split the template into system prompt and user content based on the 'Example:' delimiter
        system_prompt = template_content.replace('[Put Example here]', example_content)
        
        return {"system_prompt": system_prompt, "user_content": document_content}

    def run(self) -> Dict[str, str]:
        """Main method to run the prompt construction process and return prompts."""
        if not self.prompt_config.get('enable', False):
            print("Prompt construction is disabled in configuration.")
            return {}

        template_path = self.prompt_config.get('template_path')
        example_dir = self.prompt_config.get('example_dir')
        document_dir = self.prompt_config.get('document_dir')
        document_match_pattern = self.prompt_config.get('document_match_pattern', '')

        if not all([template_path, example_dir, document_dir]):
            print("Missing required paths for prompt construction.")
            return {}

        template_content = self._load_file_content(template_path)
        if not template_content:
            print(f"Failed to load template from {template_path}")
            return {}

        prompts = {}
        # Process documents
        document_files = glob.glob(os.path.join(document_dir, '*.md'))
        for doc_file in document_files:
            doc_basename = os.path.splitext(os.path.basename(doc_file))[0]
            
            # Apply fuzzy matching if pattern is provided
            if document_match_pattern and document_match_pattern not in doc_basename:
                continue

            document_content = self._load_file_content(doc_file)
            if not document_content:
                print(f"Skipping empty document: {doc_file}")
                continue

            # Find corresponding example file
            example_file_path = os.path.join(example_dir, f"{doc_basename.split('_')[0]}.txt") # Assuming example files are named like cloudflare.txt
            example_content = self._load_file_content(example_file_path)
            if not example_content:
                print(f"Warning: No example file found for {doc_basename} at {example_file_path}")
                example_content = ""

            prompt_parts = self._construct_prompt(example_content, document_content, template_content)
            prompts[doc_basename] = prompt_parts

        return prompts

if __name__ == '__main__':
    # Example usage (replace with actual config loading in main.py)
    sample_config = {
        "extracting": {
            "prompt": {
                "enable": True,
                "template_path": "prompt/template/extract.txt",
                "example_dir": "prompt/example",
                "document_dir": "docs/splitted_md",
                "document_match_pattern": "cloudflare"
            }
        }
    }
    contributor = PromptContributor(sample_config)
    generated_prompts = contributor.run()
    for doc_name, prompt_content in generated_prompts.items():
        print(f"\n--- Constructed Prompt for {doc_name} ---")
        print(prompt_content)