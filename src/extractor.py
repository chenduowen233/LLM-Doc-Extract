# import os
# import yaml
# import glob
# from openai import OpenAI
# from typing import Dict
# import json
# from .prompt_contributor import PromptContributor
# from .voter import Voter

# class DocumentExtractor:
#     def __init__(self, config: Dict[str, any]):
#         self.config = config.get('extracting', {})
#         self.llm_config = self.config.get('LLM', {})
#         self.vote_config = self.config.get('Vote', {})
#         self.prompt_contributor = PromptContributor(config) # Initialize the prompt contributor
#         self.voter = Voter(self.vote_config) # Initialize the Voter

#         self.llm_clients = self._initialize_llm_clients()

#     def _initialize_llm_clients(self) -> Dict[str, OpenAI]:
#         """Initializes LLM clients based on configured models and providers."""
#         clients = {}
#         provider_config_path = self.llm_config.get('provider_config_path')
#         model_names = self.llm_config.get('model_name', [])

#         if not provider_config_path:
#             print("Warning: LLM provider_config_path is not specified in config.")
#             return clients

#         for model_name in model_names:
#             model_provider_mapping = self.llm_config.get('model_provider_mapping', {})
#             provider_name = model_provider_mapping.get(model_name)
#             if not provider_name:
#                 print(f"Warning: No provider mapping found for model: {model_name}. Skipping.")
#                 continue

#             provider_file = os.path.join(provider_config_path, f'{provider_name}.yaml')
            
#             if not os.path.exists(provider_file):
#                 print(f"Warning: Provider config file not found for {provider_name} at {provider_file}")
#                 continue

#             try:
#                 with open(provider_file, 'r', encoding='utf-8') as f:
#                     provider_config = yaml.safe_load(f)

#                 api_key = provider_config.get('api_key')
#                 base_url = provider_config.get('api_base')

#                 if not api_key or not base_url:
#                     print(f"Warning: API key or base URL not found in {provider_file}")
#                     continue
                
#                 # Initialize client based on provider
#                 clients[model_name] = OpenAI(api_key=api_key, base_url=base_url)
#                 print(f"Initialized client for {model_name} with base URL: {base_url}")
#                 # Add more client initializations for other providers

#             except Exception as e:
#                 print(f"Error loading or initializing client for {model_name} from {provider_file}: {e}")
#         return clients

#     def _get_model_temperature(self, model_name: str) -> float:
#         """Retrieves the temperature setting for a given model from its provider config."""
#         provider_config_path = self.llm_config.get('provider_config_path')
#         model_provider_mapping = self.llm_config.get('model_provider_mapping', {})
#         provider_name = model_provider_mapping.get(model_name)

#         if not provider_name:
#             print(f"Warning: No provider mapping found for model: {model_name}. Using default temperature (0.7).")
#             return 0.7

#         provider_file = os.path.join(provider_config_path, f'{provider_name}.yaml')
#         if not os.path.exists(provider_file):
#             print(f"Warning: Provider config file not found for {provider_name} at {provider_file}. Using default temperature (0.7).")
#             return 0.7

#         try:
#             with open(provider_file, 'r', encoding='utf-8') as f:
#                 provider_config = yaml.safe_load(f)
#             return provider_config.get('models', {}).get(model_name, {}).get('params', {}).get('temperature', 0.7)
#         except Exception as e:
#             print(f"Error loading temperature for {model_name} from {provider_file}: {e}. Using default temperature (0.7).")
#             return 0.7

#     def _send_to_llm(self, system_prompt: str, user_content: str, model: str, temperature: float = 0.7) -> str:
#         """Sends the prompt to the LLM and returns the response."""
#         client = self.llm_clients.get(model)
#         if not client:
#             print(f"Error: LLM client not initialized for model: {model}")
#             return ""

#         messages = [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_content}
#         ]

#         try:
#             chat_completion = client.chat.completions.create(
#                 model=model,
#                 messages=messages,
#                 response_format={"type": "json_object"},
#                 temperature=temperature,
#             )
#             return chat_completion.choices[0].message.content
#         except Exception as e:
#             print(f"Error sending prompt to LLM ({model}): {e}")
#             return ""

#     def run(self):
#         """Main method to run the document extraction process."""
#         if not self.config.get('prompt', {}).get('enable', False):
#             print("Document extraction is disabled in configuration.")
#             return

#         # Get all constructed prompts from the prompt contributor
#         prompts = self.prompt_contributor.run()

#         if not prompts:
#             print("No prompts generated by the prompt contributor. Exiting extraction.")
#             return

#         for doc_basename, prompt_parts in prompts.items():
#             system_prompt = prompt_parts.get('system_prompt', '')
#             user_content = prompt_parts.get('user_content', '')

#             if not self.vote_config.get('enable', False):
#                 default_model = self.llm_config.get('default_model')
#                 if not default_model:
#                     print("Default model not specified in config when vote is disabled. Skipping.")
#                     continue
#                 if default_model not in self.llm_clients:
#                     print(f"Error: Default model '{default_model}' client not initialized. Skipping.")
#                     continue
                
#                 # Get temperature from provider config
#                 temperature = self._get_model_temperature(default_model)

#                 print(f"\n--- Extracting with {default_model} for {doc_basename} ---")
#                 response = self._send_to_llm(system_prompt, user_content, default_model, temperature)
#                 print(f"Response from {default_model}:\n{response}")
#             else:
#                 # Voting logic
#                 model_names = self.llm_config.get('model_name', [])
#                 if not model_names:
#                     print("No models specified in config for voting. Skipping.")
#                     continue

#                 responses = {}
#                 for model in model_names:
#                      if model not in self.llm_clients:
#                          print(f"Error: Model '{model}' client not initialized. Skipping.")
#                          continue
                     
#                      # Get temperature from provider config
#                      temperature = self._get_model_temperature(model)

#                      print(f"\n--- Sending prompt to {model} for {doc_basename} ---")
#                      response = self._send_to_llm(system_prompt, user_content, model, temperature)
#                      responses[model] = response
#                      print(f"Response from {model}:\n{response}")
                
#                 # Here you would implement your voting mechanism
#                 # For now, let's just print all responses
#                 print(f"\n--- All responses for {doc_basename} (voting enabled) ---")
#                 final_response = self.voter.vote(responses)
#                 # Assuming final_response is now a dictionary, convert to string for printing if needed
#                 print(f"\n--- Final Voted Response for {doc_basename} ---\n{json.dumps(final_response, indent=2)}\n---")

# if __name__ == '__main__':
#     # Example usage (replace with actual config loading in main.py)
#     sample_config = {
#         "extracting": {
#             "prompt": {
#                 "enable": True,
#                 "template_path": "prompt/template/extract.txt",
#                 "example_dir": "prompt/example",
#                 "document_dir": "docs/splitted_md",
#                 "document_match_pattern": "cloudflare"
#             },
#             "LLM": {
#                 "model_name": ["gpt-3.5-turbo"],
#                 "default_model": "gpt-3.5-turbo",
#                 "provider_config_path": "providers"
#             },
#             "Vote": {
#                 "enable": False
#             }
#         }
#     }
#     extractor = DocumentExtractor(sample_config)
#     extractor.run()

import os  # 已导入
import yaml
import glob
from openai import OpenAI
from typing import Dict
import json
from .prompt_contributor import PromptContributor
from .voter import Voter

class DocumentExtractor:
    def __init__(self, config: Dict[str, any]):
        self.config = config.get('extracting', {})
        self.llm_config = self.config.get('LLM', {})
        self.vote_config = self.config.get('Vote', {})
        self.output_paths = self.config.get('output_paths', {})
        self.prompt_contributor = PromptContributor(config)
        self.voter = Voter(self.vote_config)
        self.llm_clients = self._initialize_llm_clients()

    def _initialize_llm_clients(self) -> Dict[str, OpenAI]:
        """Initializes LLM clients based on configured models and providers."""
        clients = {}
        provider_config_path = self.llm_config.get('provider_config_path')
        model_names = self.llm_config.get('model_name', [])

        if not provider_config_path:
            print("Warning: LLM provider_config_path is not specified in config.")
            return clients

        for model_name in model_names:
            model_provider_mapping = self.llm_config.get('model_provider_mapping', {})
            provider_name = model_provider_mapping.get(model_name)
            if not provider_name:
                print(f"Warning: No provider mapping found for model: {model_name}. Skipping.")
                continue

            provider_file = os.path.join(provider_config_path, f'{provider_name}.yaml')
            
            if not os.path.exists(provider_file):
                print(f"Warning: Provider config file not found for {provider_name} at {provider_file}")
                continue

            try:
                with open(provider_file, 'r', encoding='utf-8') as f:
                    provider_config = yaml.safe_load(f)

                api_key = provider_config.get('api_key')
                base_url = provider_config.get('api_base')

                if not api_key or not base_url:
                    print(f"Warning: API key or base URL not found in {provider_file}")
                    continue
                
                # Initialize client based on provider
                clients[model_name] = OpenAI(api_key=api_key, base_url=base_url)
                print(f"Initialized client for {model_name} with base URL: {base_url}")
                # Add more client initializations for other providers

            except Exception as e:
                print(f"Error loading or initializing client for {model_name} from {provider_file}: {e}")
        return clients

    def _get_model_temperature(self, model_name: str) -> float:
        """Retrieves the temperature setting for a given model from its provider config."""
        provider_config_path = self.llm_config.get('provider_config_path')
        model_provider_mapping = self.llm_config.get('model_provider_mapping', {})
        provider_name = model_provider_mapping.get(model_name)

        if not provider_name:
            print(f"Warning: No provider mapping found for model: {model_name}. Using default temperature (0.7).")
            return 0.7

        provider_file = os.path.join(provider_config_path, f'{provider_name}.yaml')
        if not os.path.exists(provider_file):
            print(f"Warning: Provider config file not found for {provider_name} at {provider_file}. Using default temperature (0.7).")
            return 0.7

        try:
            with open(provider_file, 'r', encoding='utf-8') as f:
                provider_config = yaml.safe_load(f)
            return provider_config.get('models', {}).get(model_name, {}).get('params', {}).get('temperature', 0.7)
        except Exception as e:
            print(f"Error loading temperature for {model_name} from {provider_file}: {e}. Using default temperature (0.7).")
            return 0.7

    def _send_to_llm(self, system_prompt: str, user_content: str, model: str, temperature: float = 0.7) -> str:
        """Sends the prompt to the LLM and returns the response."""
        client = self.llm_clients.get(model)
        if not client:
            print(f"Error: LLM client not initialized for model: {model}")
            return ""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        try:
            chat_completion = client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=temperature,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error sending prompt to LLM ({model}): {e}")
            return ""

    def _write_response_to_file(self, response: str or dict, basename: str, voted: bool = False):
        """写入响应结果到JSON文件"""
        output_dir = self.output_paths.get('voted_json_dir' if voted else 'extracted_json_dir')
        if not output_dir:
            print(f"Warning: Output path for {'voted' if voted else 'extracted'} JSON not configured.")
            return
        
        os.makedirs(output_dir, exist_ok=True)

        filename = os.path.splitext(basename)[0] + '.json'
        output_path = os.path.join(output_dir, filename)

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                if isinstance(response, str):
                    json.dump({"response": response}, f, ensure_ascii=False, indent=2)
                else:
                    json.dump(response, f, ensure_ascii=False, indent=2)
            print(f"Saved response to {output_path}")
        except Exception as e:
            print(f"Error saving response to {output_path}: {e}")

    def run(self):
        """Main method to run the document extraction process."""
        if not self.config.get('prompt', {}).get('enable', False):
            print("Document extraction is disabled in configuration.")
            return

        prompts = self.prompt_contributor.run()
        if not prompts:
            print("No prompts generated by the prompt contributor. Exiting extraction.")
            return

        for doc_basename, prompt_parts in prompts.items():
            system_prompt = prompt_parts.get('system_prompt', '')
            user_content = prompt_parts.get('user_content', '')

            if not self.vote_config.get('enable', False):
                default_model = self.llm_config.get('default_model')
                if not default_model:
                    print("Default model not specified in config when vote is disabled. Skipping.")
                    continue
                if default_model not in self.llm_clients:
                    print(f"Error: Default model '{default_model}' client not initialized. Skipping.")
                    continue

                temperature = self._get_model_temperature(default_model)

                print(f"\n--- Extracting with {default_model} for {doc_basename} ---")
                response = self._send_to_llm(system_prompt, user_content, default_model, temperature)
                print(f"Response from {default_model}:\n{response}")
                
                # ✅ 写入未投票的结果
                self._write_response_to_file(response, doc_basename, voted=False)

            else:
                model_names = self.llm_config.get('model_name', [])
                if not model_names:
                    print("No models specified in config for voting. Skipping.")
                    continue

                responses = {}
                for model in model_names:
                    if model not in self.llm_clients:
                        print(f"Error: Model '{model}' client not initialized. Skipping.")
                        continue

                    temperature = self._get_model_temperature(model)

                    print(f"\n--- Sending prompt to {model} for {doc_basename} ---")
                    response = self._send_to_llm(system_prompt, user_content, model, temperature)
                    responses[model] = response
                    print(f"Response from {model}:\n{response}")

                final_response = self.voter.vote(responses)
                print(f"\n--- Final Voted Response for {doc_basename} ---\n{json.dumps(final_response, indent=2)}\n---")

                # ✅ 写入投票后的结果
                self._write_response_to_file(final_response, doc_basename, voted=True)
