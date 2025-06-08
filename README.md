# Crewai-MCP
## Build an MCP agent using Crewai
##

### Workflow of MCP powered Crewai RStudy Assistant

```

graph TD
    %% User Interface Layer
    A["🌐 User Interface<br/>Streamlit App<br/>(streamlit_app.py)"] --> B["⚙️ API Layer<br/>main_api.py"]
    
    %% API Processing
    B --> C["🚀 Subprocess Call<br/>python main.py {topic}"]
    
    %% CrewAI Core
    C --> D["🤖 CrewAI Application<br/>(main.py)<br/>Research Agent + Writer Agent"]
    
    %% MCP Protocol Communication
    D --> E["📡 MCP Protocol<br/>Model Context Protocol<br/>Communication Layer"]
    
    %% MCP Servers
    E --> F["🔍 Search MCP Server<br/>(servers/search_server.py)<br/>Python Implementation"]
    E --> G["🎨 Image MCP Server<br/>(servers/image_server.py)<br/>Python Implementation"]
    E --> H["📁 Filesystem MCP Server<br/>(NPX - Disabled)<br/>Node.js v14 Issue"]
    
    %% External APIs
    F --> I["🦁 Brave Search API<br/>Web Search Results"]
    G --> J["🎭 Segmind API<br/>AI Image Generation"]
    
    %% File Output Generation
    D --> K["📄 File Generation"]
    K --> L["📊 search_results.json<br/>Search Data"]
    K --> M["📝 summary.txt<br/>Research Summary"]
    K --> N["🖼️ generated_images/<br/>AI Generated Images"]
    
    %% Result Processing
    B --> O["🔄 Result Extraction<br/>File Detection & Parsing"]
    O --> P["📋 Summary Extraction<br/>Multiple Pattern Recognition"]
    O --> Q["🔍 Search Results Parsing<br/>JSON Processing"]
    O --> R["🖼️ Image Collection<br/>File Listing"]
    
    %% Display Results
    P --> S["📑 Summary Tab<br/>Streamlit Display"]
    Q --> T["🔍 Search Results Tab<br/>Streamlit Cards"]
    R --> U["🎨 Generated Images Tab<br/>Streamlit Gallery"]
    
    %% User Features
    S --> V["💾 Download Summary<br/>Text File"]
    U --> W["💾 Download Images<br/>ZIP Archive"]
    
    %% System Monitoring
    A --> X["📊 System Status<br/>MCP Server Health Check"]
    
    %% Styling for different component types
    classDef streamlit fill:#ff6b6b,stroke:#ff5252,stroke-width:3px,color:#fff
    classDef crewai fill:#4ecdc4,stroke:#26a69a,stroke-width:3px,color:#fff
    classDef mcp fill:#45b7d1,stroke:#039be5,stroke-width:3px,color:#fff
    classDef api fill:#96ceb4,stroke:#66bb6a,stroke-width:3px,color:#fff
    classDef files fill:#feca57,stroke:#ff9800,stroke-width:3px,color:#fff
    
    %% Apply styles
    class A,S,T,U,V,W,X streamlit
    class D crewai
    class E,F,G,H mcp
    class I,J api
    class K,L,M,N,O,P,Q,R files
    class B,C streamlit

```

<img width="1277" alt="image" src="https://github.com/user-attachments/assets/6a21b515-0c29-41e3-bfa1-3f1ba7991cd9" />




## 🏗️ Architecture Breakdown

#### 📱 Frontend Layer
* streamlit_app.py - Main web interface with beautiful UI
* streamlit_app_backup.py - Backup version for safety

#### 🔄 API & Integration Layer

* main_api.py - Bridge between Streamlit and CrewAI
* app.py - Alternative interface implementation
  
#### 🤖 AI Core Layer

* main.py - CrewAI agents (Research + Writer)
* debug_summary.py - Summary extraction utilities


#### 📡 MCP Server Layer

* servers/search_server.py - Web search via Brave API
* servers/image_server.py - Image generation via Segmind API
  
#### 📊 Data Storage Layer

* servers/search_results/ - JSON files with search data (40+ topics)
* servers/images/ - Generated AI images (30+ visuals)

#### ⚙️ Configuration & Utilities
* requirements.txt - Dependencies management
* setup_nodejs.py - Environment setup
* test_python_version.py - Compatibility testing

<img width="878" alt="image" src="https://github.com/user-attachments/assets/1a5634c3-e354-4301-8b00-eab738c1182c" />

## Run the Application without the UI 

```
python main.py
```

## Run the Application using streamlit

```
# Launch Streamlit app
 streamlit run streamlit_app.py
```


## Streamlit Interface 

<img width="1186" alt="image" src="https://github.com/user-attachments/assets/ec4adf38-e9a6-4232-b0a9-27b391965dca" />



<img width="1085" alt="image" src="https://github.com/user-attachments/assets/d7ff1352-865e-44ef-b813-ac092a0dc2f5" />


<img width="1019" alt="image" src="https://github.com/user-attachments/assets/13e1f173-b191-4bb5-8661-08d0812ef4c9" />


