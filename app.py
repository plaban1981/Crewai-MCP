import streamlit as st
import subprocess
import sys
import os
from pathlib import Path
import glob
from PIL import Image
import re

def find_venv_python():
    """Find the correct Python executable from virtual environment"""
    current_dir = Path(__file__).parent
    possible_venv_paths = [
        os.path.join(current_dir, ".venv", "Scripts", "python.exe"),
        os.path.join(current_dir, "venv", "Scripts", "python.exe"),
        os.path.join(current_dir, ".venv", "bin", "python"),
        os.path.join(current_dir, "venv", "bin", "python"),
    ]
    
    for path in possible_venv_paths:
        if os.path.exists(path):
            return path
    return sys.executable

def run_research(topic):
    """Run main.py with the given topic and return the result"""
    current_dir = Path(__file__).parent
    python_executable = find_venv_python()
    
    # Prepare environment with UTF-8 encoding
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONLEGACYWINDOWSSTDIO'] = '1'
    
    try:
        # Run main.py as subprocess
        process = subprocess.Popen(
            [python_executable, "main.py"],
            cwd=current_dir,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',
            env=env
        )
        
        # Send topic as input
        stdout, stderr = process.communicate(input=topic + "\n", timeout=300)
        
        if process.returncode == 0:
            # Extract final result from stdout
            return extract_final_result(stdout), None
        else:
            return None, f"Error (return code {process.returncode}):\n{stderr}"
            
    except subprocess.TimeoutExpired:
        process.kill()
        return None, "Research timed out after 5 minutes"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

def extract_final_result(output):
    """Extract the final result from main.py CrewAI output"""
    lines = output.split('\n')
    
    # First, try to find the final result section
    final_result_start = -1
    for i, line in enumerate(lines):
        if "FINAL RESULT:" in line or "==================================================\nFINAL RESULT:" in output:
            final_result_start = i
            break
    
    if final_result_start != -1:
        # Extract everything after "FINAL RESULT:" until end
        result_lines = []
        for line in lines[final_result_start:]:
            # Skip the "FINAL RESULT:" line itself
            if "FINAL RESULT:" in line:
                # Get content after the marker if it exists on same line
                content_after = line.split("FINAL RESULT:", 1)
                if len(content_after) > 1 and content_after[1].strip():
                    result_lines.append(content_after[1].strip())
                continue
            
            # Skip CrewAI formatting and empty lines
            cleaned_line = re.sub(r'[╭│╰═─└├┤┬┴┼╔╗╚╝║╠╣╦╩╬▓▒░]', '', line)
            cleaned_line = cleaned_line.strip()
            
            if cleaned_line:
                result_lines.append(cleaned_line)
        
        if result_lines:
            return '\n'.join(result_lines).strip()
    
    # Second attempt: Look for ## Final Answer pattern
    final_answer_lines = []
    capturing = False
    
    for line in lines:
        if "## Final Answer" in line or "Final Answer:" in line:
            capturing = True
            # Include content after the marker if it exists
            if "Final Answer:" in line:
                content = line.split("Final Answer:", 1)
                if len(content) > 1 and content[1].strip():
                    final_answer_lines.append(content[1].strip())
            continue
        
        if capturing:
            # Skip CrewAI box drawing characters and progress indicators
            cleaned = re.sub(r'[╭│╰═─└├┤┬┴┼╔╗╚╝║╠╣╦╩╬▓▒░🚀📋🔧✅]', '', line)
            cleaned = cleaned.strip()
            
            # Stop at certain patterns that indicate end of answer
            if any(pattern in line.lower() for pattern in [
                'crew execution completed', 'task completion', 'crew completion',
                '└──', 'assigned to:', 'status:', 'used'
            ]):
                break
            
            # Only include substantial content
            if cleaned and len(cleaned) > 10:
                final_answer_lines.append(cleaned)
    
    if final_answer_lines:
        return '\n'.join(final_answer_lines).strip()
    
    # Third attempt: Get the last substantial paragraph before crew completion messages
    substantial_blocks = []
    current_block = []
    
    for line in lines:
        # Skip obvious CrewAI UI elements
        if any(skip in line for skip in ['╭', '│', '╰', '🚀', '📋', '└──', 'Assigned to:', 'Status:']):
            if current_block:
                substantial_blocks.append('\n'.join(current_block))
                current_block = []
            continue
        
        cleaned = line.strip()
        if cleaned and len(cleaned) > 30:  # Only substantial lines
            current_block.append(cleaned)
        elif current_block:  # Empty line ends a block
            substantial_blocks.append('\n'.join(current_block))
            current_block = []
    
    # Add the last block
    if current_block:
        substantial_blocks.append('\n'.join(current_block))
    
    # Return the last substantial block (likely the final answer)
    if substantial_blocks:
        return substantial_blocks[-1].strip()
    
    return "Research completed successfully. Please check the console output for detailed results."

def get_latest_images():
    """Get the latest images from the images folder"""
    images_dir = Path("servers/images")
    if not images_dir.exists():
        return []
    
    # Get all image files
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(str(images_dir / ext)))
    
    if not image_files:
        return []
    
    # Sort by modification time (newest first)
    image_files.sort(key=os.path.getmtime, reverse=True)
    
    # Return top 5 most recent images
    return image_files[:1]

def main():
    st.set_page_config(
        page_title="CrewAI-MCP Research Assistant",
        page_icon="🔬",
        layout="wide"
    )
    
    st.title("🔬 CrewAI-MCP Study Assistant")
    st.markdown("Enter a topic to research and generate comprehensive insights with visual diagrams.")
    
    # Topic input
    topic = st.text_input(
        "Research Topic:",
        placeholder="e.g., Explain photosynthesis process, Machine learning algorithms, etc.",
        help="Enter any topic you want to research in detail"
    )
    
    # Research button
    if st.button("🚀 Start Research", type="primary", disabled=not topic.strip()):
        if topic.strip():
            with st.spinner(f"🔍 Researching '{topic}'... This may take a few minutes."):
                result, error = run_research(topic.strip())
                print(f"Result from CREWAI : {result}")
            
            if result:
                st.success("✅ Research completed successfully!")
                print(f"Result from CREWAI : {result}")
                # Store results in session state
                st.session_state['research_result'] = result
                st.session_state['research_topic'] = topic.strip()
                st.session_state['latest_images'] = get_latest_images()
            else:
                st.error(f"❌ Research failed: {error}")
    
    # Display results and images side by side
    if 'research_result' in st.session_state:
        # Create a divider
        st.divider()
        st.subheader(f"Research Results: {st.session_state.get('research_topic', 'Unknown Topic')}")
        
        # Create two columns for side-by-side display
        col1, col2 = st.columns([2, 1])  # Results get 2/3 width, Images get 1/3 width
        
        # Left column - Research Results
        with col1:
            st.markdown("### 📋 Summary Results")
            
            # Display the result in markdown format
            result_text = st.session_state['research_result']
            pattern = re.compile(r'\x1b\[[\d;]*m')
            result_text = pattern.sub('', result_text)
            
            # Create a scrollable container for long content
            with st.container():
                st.markdown(result_text)
            
            # Add download button for the result
            st.download_button(
                label="📥 Download Results as Text",
                data=result_text,
                file_name=f"research_{st.session_state.get('research_topic', 'topic').replace(' ', '_')}.txt",
                mime="text/plain"
            )
        
        # Right column - Generated Images
        with col2:
            st.markdown("### 🎨 Generated Images")
            
            images = st.session_state.get('latest_images', [])
            
            if images:
                st.success(f"Found {len(images)} image(s)")
                
                # Display images vertically stacked
                for idx, image_path in enumerate(images):
                    try:
                        # Open and display image
                        img = Image.open(image_path)
                        
                        st.image(
                            img, 
                            caption=f"Generated: {Path(image_path).name}",
                            use_container_width=True
                        )
                        
                        # Add download button for each image
                        with open(image_path, "rb") as file:
                            st.download_button(
                                label=f"⬇️ Download",
                                data=file.read(),
                                file_name=Path(image_path).name,
                                mime="image/jpeg",
                                key=f"download_img_{idx}"
                            )
                        
                        # Add spacing between images if there are multiple
                        if idx < len(images) - 1:
                            st.markdown("---")
                            
                    except Exception as e:
                        st.error(f"Error loading image: {str(e)}")
            else:
                st.info("🖼️ Images will appear here after research completion.")
                with st.expander("ℹ️ About Images"):
                    st.markdown("""
                    **How it works:**
                    - Images are automatically generated during research
                    - Saved to `servers/images/` folder
                    - Displayed here sorted by creation time
                    - Download button available for each image
                    """)

if __name__ == "__main__":
    main() 