import os
import os
import re
from typing import Dict, Any, List
from langchain.text_splitter import MarkdownHeaderTextSplitter

class DocumentSplitter:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.input_dir = config['input_dir']
        self.output_dir = config['output_dir']
        self.method = config['method']
        self.level = config.get('level', 3) # Max heading level to consider for splitting
        self.max_lines = config.get('max_lines', 200) # Max lines per chunk

        os.makedirs(self.output_dir, exist_ok=True)

    def _split_document(self, content: str) -> List[str]:
        """Split the document based on configuration."""
        if self.method == 'heading':
            return self._split_by_heading(content)
        else:
            return self._split_by_line_count(content)

    def _split_by_heading(self, content: str) -> List[str]:
        """Split document by heading level and line count, preserving hierarchical structure."""
        lines = content.split('\n')
        chunks = []
        current_chunk_lines = []
        current_chunk_line_count = 0
        
        # Store headings and their content
        parsed_sections = []
        current_section = {"level": 0, "title": "", "content": []}
        
        for line in lines:
            match = re.match(r'^(#+)\s*(.*)', line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                
                # If a new section starts, save the previous one
                if current_section["content"]:
                    parsed_sections.append(current_section)
                
                current_section = {"level": level, "title": title, "content": [line]}
            else:
                current_section["content"].append(line)
        
        if current_section["content"]:
            parsed_sections.append(current_section)

        # Now, iterate through parsed sections to create chunks based on max_lines and hierarchy
        for i, section in enumerate(parsed_sections):
            section_content = "\n".join(section["content"])
            section_line_count = len(section["content"])

            # If adding this section exceeds max_lines, start a new chunk
            if current_chunk_line_count + section_line_count > self.max_lines and current_chunk_lines:
                chunks.append("\n".join(current_chunk_lines))
                current_chunk_lines = []
                current_chunk_line_count = 0

            # Add the current section to the current chunk
            current_chunk_lines.append(section_content)
            current_chunk_line_count += section_line_count

            # Check if the next section is a lower level heading (child) or if it's the last section
            # If it's a child, we want to keep it with the parent if possible
            # If it's a sibling or higher level, and we are close to max_lines, we might want to split
            if i + 1 < len(parsed_sections):
                next_section = parsed_sections[i+1]
                # If the next section is a sibling or higher level, and current chunk is substantial
                if next_section["level"] <= section["level"] and current_chunk_line_count >= self.max_lines * 0.8:
                    chunks.append("\n".join(current_chunk_lines))
                    current_chunk_lines = []
                    current_chunk_line_count = 0
            else:
                # Last section, add remaining content
                if current_chunk_lines:
                    chunks.append("\n".join(current_chunk_lines))

        return chunks

    def _split_by_line_count(self, content: str) -> List[str]:
        """Split document by line count."""
        lines = content.split('\n')
        return ['\n'.join(lines[i:i + self.max_lines]) 
                for i in range(0, len(lines), self.max_lines)]

    def run(self) -> None:
        """Process all markdown files in the input directory and split them."""
        if not self.config.get('enable', False):
            print("Document splitting is disabled in configuration.")
            return

        for root, _, files in os.walk(self.input_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    try:
                        print(f"Splitting document: {file_path}")
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        split_documents = self._split_document(content)
                        
                        base_filename = os.path.splitext(file)[0]
                        for i, doc_content in enumerate(split_documents, 1):
                            filename = f"{base_filename}_{i:02d}.md"
                            filepath = os.path.join(self.output_dir, filename)
                            
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(doc_content)
                            print(f"Saved split document: {filename}")
                    except Exception as e:
                        print(f"Error splitting file {file_path}: {str(e)}")