---
title: dspy-example
app_file: gradio_interface.py
sdk: gradio
sdk_version: 5.38.2
---
# 🎬 DSPy Director Bake-Off: A Beginner's Guide to DSPy Programming

Welcome to the **DSPy Director Bake-Off**! This project demonstrates core DSPy concepts through a fun, practical example: comparing how different movie directors would approach filming the same video idea.

## 🎯 What You'll Learn

This tutorial teaches you the fundamental concepts of **DSPy** (Declarative Self-improving Python) through hands-on examples:

1. **Signatures** - Define input/output interfaces for LLM tasks
2. **Modules** - Combine multiple signatures into complex workflows  
3. **Structured Output** - Use Pydantic models for reliable data extraction
4. **Async Processing** - Handle multiple LLM calls efficiently
5. **Chain of Thought** - Enable reasoning for complex decisions

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- An OpenRouter API key (free tier available)

### Installation

1. **Clone or download this project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**
   Create a `.env` file in the project directory:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

4. **Run the demo:**
   ```bash
   python director_bake_off.py
   ```

5. **Try the web interface:**
   ```bash
   python gradio_interface.py
   ```
   Then open http://localhost:7860 in your browser.

## 🎭 How It Works

The Director Bake-Off follows this workflow:

1. **User Input**: You provide a video idea and list of directors
2. **AI Suggestion**: DSPy suggests an additional director perfect for your idea
3. **Parallel Generation**: Each director's unique interpretation is generated simultaneously
4. **Intelligent Ranking**: An AI judge ranks all interpretations and explains the reasoning
5. **Beautiful Results**: View the winner and detailed breakdowns

## 📚 Understanding the Code Structure

### 🏗️ Project Architecture

```
director_bake_off.py    # Main DSPy implementation (heavily commented)
gradio_interface.py     # Beautiful web interface
requirements.txt        # Python dependencies
.env                   # Your API keys (create this)
README.md              # This guide
```

### 🔍 Code Walkthrough

The `director_bake_off.py` file is organized into clear sections:

#### **Section 1: LLM Setup**
```python
def setup_dspy_provider():
    # Configure DSPy with your chosen LLM provider
    # Supports OpenAI, Anthropic, OpenRouter, and more
```

#### **Section 2: Data Structures**
```python
class DirectorCut(BaseModel):
    # Pydantic model defining the structure of cinematic prompts
    # Ensures consistent, validated output from the LLM
```

#### **Section 3: DSPy Signatures**
```python
class FindDirector(dspy.Signature):
    # Defines what inputs the LLM expects and what outputs it should produce
    # Think of these as "contracts" between your code and the LLM
```

#### **Section 4: DSPy Module**
```python
class DirectorBakeOff(dspy.Module):
    # Combines multiple signatures into a complete workflow
    # Orchestrates the entire director comparison process
```

#### **Section 5: Main Functions**
```python
def run_bake_off(video_idea, directors):
    # Easy-to-use interface that handles everything
    # This is what external code calls to use our system
```

## 🎓 DSPy Concepts Explained

### What is DSPy?

**DSPy** is a framework for programming with Large Language Models (LLMs). Instead of writing prompts as strings, you define structured interfaces that make your LLM applications more reliable, maintainable, and powerful.

### 🔥 Key Concepts

#### 1. **Signatures** - The Heart of DSPy

Signatures define the interface between your code and the LLM:

```python
class GenerateDirectorCut(dspy.Signature):
    """Transform a video idea into a cinematic prompt in a director's style."""
    
    # What goes IN to the LLM
    video_idea = dspy.InputField(desc="A simple video concept")
    director = dspy.InputField(desc="The director's name")
    
    # What comes OUT of the LLM  
    director_cut: DirectorCut = dspy.OutputField(desc="Structured cinematic prompt")
```

**Why this is powerful:**
- Clear contracts between code and LLM
- Automatic prompt generation
- Type safety and validation
- Reusable across different models

#### 2. **Structured Output with Pydantic**

Instead of parsing messy text, get structured data:

```python
class DirectorCut(BaseModel):
    director: str
    subject_description: str
    action_description: str
    setting_description: str
    # ... more fields
    
    def assemble_prompt(self) -> str:
        # Combine all parts into a complete prompt
        return ", ".join([self.subject_description, self.action_description, ...])
```

**Benefits:**
- Guaranteed data format
- Automatic validation
- Easy to work with in code
- No more regex parsing!

#### 3. **Modules** - Complex Workflows

Modules combine multiple signatures into sophisticated workflows:

```python
class DirectorBakeOff(dspy.Module):
    def __init__(self):
        self.findDirector = dspy.Predict(FindDirector)
        self.genDirectorCut = dspy.Predict(GenerateDirectorCut)
        self.directorJudge = dspy.ChainOfThought(DirectorJudge)
    
    async def aforward(self, video_idea, directors):
        # Orchestrate multiple LLM calls
        # 1. Find additional director
        # 2. Generate interpretations (in parallel!)
        # 3. Judge and rank results
```

#### 4. **Different Predictor Types**

- **`dspy.Predict`**: Basic, fast predictions
- **`dspy.ChainOfThought`**: Enables step-by-step reasoning
- **`dspy.ReAct`**: Combines reasoning with actions
- **`dspy.ProgramOfThought`**: For mathematical/logical problems

#### 5. **Async Processing**

Handle multiple LLM calls efficiently:

```python
# Instead of calling one by one (slow):
for director in directors:
    result = self.genDirectorCut(video_idea=idea, director=director)

# Call them all at once (fast!):
results = await asyncio.gather(
    *[self.genDirectorCut.acall(video_idea=idea, director=d) for d in directors]
)
```

## 🛠️ Building Your Own DSPy Applications

### Step 1: Define Your Data Structure

Start with a Pydantic model for your expected output:

```python
class MyOutput(BaseModel):
    field1: str = Field(..., description="What this field should contain")
    field2: int = Field(..., description="A number representing...")
    # Add more fields as needed
```

### Step 2: Create Signatures

Define the interface for each LLM task:

```python
class MyTask(dspy.Signature):
    """Clear description of what this task should do."""
    
    # Inputs
    user_input = dspy.InputField(desc="What the user provides")
    
    # Outputs  
    result: MyOutput = dspy.OutputField(desc="The structured result")
```

### Step 3: Build a Module

Combine signatures into a workflow:

```python
class MyModule(dspy.Module):
    def __init__(self):
        self.task = dspy.Predict(MyTask)
    
    def forward(self, user_input):
        return self.task(user_input=user_input)
```

### Step 4: Configure and Run

```python
# Configure DSPy with your LLM
dspy.configure(lm=dspy.LM("openrouter/model-name", api_key="your-key"))

# Use your module
module = MyModule()
result = module.forward("user input here")
print(result.result.field1)  # Access structured output
```

## 🎨 Customization Ideas

Try modifying the Director Bake-Off to explore DSPy further:

### 🎬 **Different Creative Domains**
- **Music Producer Bake-Off**: Compare how different producers would approach a song
- **Chef Bake-Off**: See how famous chefs would prepare the same dish
- **Architect Bake-Off**: Compare building designs for the same space

### 🔧 **Technical Enhancements**
- **Add More Signatures**: Include budget estimation, casting suggestions
- **Different Predictors**: Try `dspy.ReAct` for more complex reasoning
- **Optimization**: Use DSPy's optimization features to improve performance
- **Multiple Models**: Compare results from different LLMs

### 🎯 **New Applications**
- **Content Planning**: Generate social media strategies
- **Product Design**: Compare design approaches for products
- **Educational Content**: Create lesson plans in different teaching styles

## 🔗 Useful Resources

### DSPy Documentation
- [Official DSPy Documentation](https://dspy-docs.vercel.app/)
- [DSPy GitHub Repository](https://github.com/stanfordnlp/dspy)
- [DSPy Paper](https://arxiv.org/abs/2310.03714)

### LLM Providers
- [OpenRouter](https://openrouter.ai/) - Access to many models through one API
- [OpenAI](https://platform.openai.com/) - GPT models
- [Anthropic](https://www.anthropic.com/) - Claude models

### Learning More
- [Pydantic Documentation](https://docs.pydantic.dev/) - For data validation
- [Gradio Documentation](https://gradio.app/docs/) - For building web interfaces
- [Python Asyncio](https://docs.python.org/3/library/asyncio.html) - For async programming

## 🤝 Contributing

Found this helpful? Here are ways to contribute:

1. **Try it out** and share your results
2. **Create variations** for different domains
3. **Improve the documentation** with your learnings
4. **Share examples** of your own DSPy applications

## 📝 License

This project is open source and available under the MIT License.

## 🎉 What's Next?

After mastering this example, you'll be ready to:

- Build production DSPy applications
- Optimize prompts automatically with DSPy's built-in tools
- Create complex multi-step reasoning systems
- Integrate DSPy into larger applications

**Happy coding with DSPy!** 🚀

---

*This tutorial was created to make DSPy accessible to beginners. The heavily commented code and step-by-step explanations should help you understand not just how to use DSPy, but why it's such a powerful framework for LLM programming.*
