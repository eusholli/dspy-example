#!/usr/bin/env python3
"""
DSPy Director Bake-Off: A Beginner's Guide to DSPy Programming

This script demonstrates core DSPy concepts through a fun example:
comparing how different movie directors would approach filming the same video idea.

Key DSPy Concepts Demonstrated:
1. Signatures - Define input/output interfaces for LLM tasks
2. Modules - Combine multiple signatures into complex workflows
3. Structured Output - Use Pydantic models for reliable data extraction
4. Async Processing - Handle multiple LLM calls efficiently
5. Chain of Thought - Enable reasoning for complex decisions

Author: DSPy Learning Example
"""

# Standard library imports
import os
import sys
import asyncio
from typing import List

# Third-party imports
import dspy                    # The main DSPy framework for LLM programming
from dotenv import load_dotenv # For loading environment variables from .env file
from pydantic import BaseModel, Field  # For structured data validation

# Load environment variables from .env file (contains API keys)
load_dotenv()

# Global variable to store our configured language model
# This will be set up once and reused throughout the application
lm = None


# ==========================================================================
# SECTION 1: LLM SETUP AND CONFIGURATION
# ==========================================================================

def setup_dspy_provider():
    """
    Configure DSPy with an available LLM provider.
    
    DSPy supports many providers (OpenAI, Anthropic, OpenRouter, etc.)
    This function tries to connect to OpenRouter, which provides access
    to many different models through a single API.
    
    Returns:
        str: The name of the provider that was successfully configured
    """
    global lm  # We'll modify the global lm variable

    # Check if we have an OpenRouter API key in our environment variables
    if os.getenv('OPENROUTER_API_KEY'):
        print("✅ Configuring DSPy with OpenRouter...")
        
        # Create a DSPy Language Model object
        # Format: "provider/model_name"
        # Here we use a free model from Moonshot AI via OpenRouter
        lm = dspy.LM(
            model="openrouter/moonshotai/kimi-k2:free", 
            api_key=os.getenv('OPENROUTER_API_KEY')
        )
        
        # Configure DSPy to use this language model globally
        dspy.configure(lm=lm)
        return "openrouter"
    else:
        print("❌ No OpenRouter API key found in environment variables.")
        print("Please add OPENROUTER_API_KEY to your .env file")
        sys.exit(1)


# ==========================================================================
# SECTION 2: DATA STRUCTURES (PYDANTIC MODELS)
# ==========================================================================

class DirectorCut(BaseModel):
    """
    🎬 PYDANTIC MODEL: Structured Data for Cinematic Prompts
    
    This is a Pydantic model that defines the structure of our data.
    Pydantic ensures that the LLM returns data in exactly the format we expect.
    
    Think of this as a "template" that the LLM must fill out completely.
    Each field has a description that helps the LLM understand what to generate.
    
    Why use Pydantic with DSPy?
    - Guarantees consistent output format
    - Automatic validation of LLM responses
    - Type safety for your Python code
    - Clear documentation of expected data structure
    """
    
    # Basic information (echoed from input)
    director: str = Field(
        ..., 
        description="The director sent as part of input, echoed in the output."
    )
    video_idea: str = Field(
        ..., 
        description="The video idea sent as part of input, echoed in the output."
    )
    
    # The seven components of a cinematic prompt
    # Each field uses Field(...) where ... means "required"
    subject_description: str = Field(
        ..., 
        description="A detailed description of the main subject or character."
    )
    action_description: str = Field(
        ..., 
        description="A description of the specific action the subject is performing."
    )
    setting_description: str = Field(
        ..., 
        description="A rich description of the environment, location, and time of day."
    )
    cinematic_style: str = Field(
        ..., 
        description="The overall visual style or medium (e.g., 'Photorealistic, 8K')."
    )
    shot_and_framing: str = Field(
        ..., 
        description="The specific camera shot type and framing (e.g., 'Medium shot')."
    )
    camera_movement: str = Field(
        ..., 
        description="The movement of the camera during the shot (e.g., 'Slow dolly shot')."
    )
    lighting_and_color: str = Field(
        ..., 
        description="The lighting style and color palette that sets the mood."
    )

    def assemble_prompt(self) -> str:
        """
        Combines all cinematic components into a single, formatted prompt.
        
        This method takes all the individual pieces and creates a complete
        prompt that could be used with video generation AI models.
        
        Returns:
            str: A complete, formatted cinematic prompt
        """
        # Collect all the cinematic components (excluding director and video_idea)
        components = [
            self.subject_description,
            self.action_description,
            self.setting_description,
            self.cinematic_style,
            self.shot_and_framing,
            self.camera_movement,
            self.lighting_and_color,
        ]
        
        # Join components with commas, filtering out empty strings
        prompt_string = ", ".join(filter(None, [c.strip() for c in components if c]))
        
        # Return empty string if no components
        if not prompt_string:
            return ""
            
        # Capitalize first letter and add period
        return prompt_string[0].upper() + prompt_string[1:] + "."

    def pretty_print(self):
        """
        Displays the director's interpretation in a nice format.
        
        This is a helper method to make the output more readable
        when we're testing or debugging our code.
        """
        print(f"--- Director {self.director} ---")
        print(f"{self.assemble_prompt()}")
        print("--------------------------------")


class ResultClass:
    """
    📦 SIMPLE DATA CONTAINER: Holds All Results
    
    This is a simple class to package up all our results.
    We could use a Pydantic model here too, but since this is just
    for internal use (not LLM output), a simple class works fine.
    """
    def __init__(self, additional_director, director_ideas, director_ranks):
        self.additional_director = additional_director  # The AI-suggested director
        self.director_ideas = director_ideas            # List of all DirectorCut objects
        self.director_ranks = director_ranks            # Ranking results from the judge


# ==========================================================================
# SECTION 3: DSPY SIGNATURES (THE HEART OF DSPY)
# ==========================================================================

"""
🔥 WHAT ARE DSPY SIGNATURES?

DSPy Signatures are like "function signatures" but for LLM tasks.
They define:
1. What inputs the LLM should expect
2. What outputs the LLM should produce
3. The task description (in the docstring)

Think of them as contracts between your code and the LLM.
The LLM will try to fulfill this contract every time.

Key Components:
- InputField: Data going INTO the LLM
- OutputField: Data coming OUT of the LLM
- Docstring: Instructions for the LLM about what to do
"""

class FindDirector(dspy.Signature):
    """
    🎯 SIGNATURE 1: Find Additional Director
    
    This signature asks the LLM to suggest one additional director
    who would be perfect for the given video idea, but isn't already
    in the user's list.
    
    This demonstrates how DSPy can handle creative, open-ended tasks
    where there's no single "correct" answer.
    """
    
    # === INPUTS ===
    video_idea = dspy.InputField(
        desc="A simple, high-level user idea or concept for a video."
    )
    director_list: List[str] = dspy.InputField(
        desc="The names of directors the user wants to use."
    )

    # === OUTPUTS ===
    additonal_director: str = dspy.OutputField(
        desc="The best possible director based on the wanted video idea, that is not already in the provided director list."
    )


class GenerateDirectorCut(dspy.Signature):
    """
    🎬 SIGNATURE 2: Generate Cinematic Interpretation
    
    This is the core signature that transforms a simple video idea
    into a detailed cinematic prompt in the style of a specific director.
    
    Notice how the output is a Pydantic model (DirectorCut).
    DSPy will automatically ensure the LLM returns data in exactly
    that structure, with all required fields filled out.
    
    This demonstrates DSPy's structured output capabilities.
    """
    
    # === INPUTS ===
    video_idea = dspy.InputField(
        desc="A simple, high-level user idea or concept for a video."
    )
    director = dspy.InputField(
        desc="The name of the director to generate a cinematic prompt for (optional).",
        default=None,
        optional=True
    )

    # === OUTPUTS ===
    director_cut: DirectorCut = dspy.OutputField(
        desc="A structured object containing all seven deconstructed cinematic aspects."
    )


class DirectorJudge(dspy.Signature):
    """
    ⚖️ SIGNATURE 3: Judge and Rank Director Ideas
    
    This signature handles the complex task of comparing multiple
    creative interpretations and ranking them objectively.
    
    Notice this takes a List[DirectorCut] as input and returns
    both rankings AND an explanation. This shows how DSPy can
    handle complex, multi-part outputs.
    
    This demonstrates DSPy's ability to handle reasoning tasks.
    """
    
    # === INPUTS ===
    director_ideas: List[DirectorCut] = dspy.InputField(
        desc="A list of director interpretations to be ranked"
    )
    
    # === OUTPUTS ===
    director_rankings: List[int] = dspy.OutputField(
        description="Rank between 1, 2, 3 ... N where 1 is best"
    )
    explanation: str = dspy.OutputField(
        description="Explain why the ranking was given and the winner selected. Format your response with clear sections for each director using HTML formatting: use <h4> tags for director names with their rank, <p> tags for paragraphs, and <br> tags for line breaks. Make it well-structured and easy to read."
    )


# ==========================================================================
# SECTION 4: DSPY MODULE (COMBINING SIGNATURES INTO WORKFLOWS)
# ==========================================================================

class DirectorBakeOff(dspy.Module):
    """
    🏗️ DSPY MODULE: The Complete Workflow
    
    A DSPy Module combines multiple Signatures into a complete workflow.
    Think of it like a class that orchestrates several LLM calls to solve
    a complex problem.
    
    This module demonstrates:
    1. How to combine multiple signatures
    2. Different types of DSPy predictors (Predict vs ChainOfThought)
    3. Async processing for efficiency
    4. Complex workflow orchestration
    
    The workflow:
    1. Find an additional director suggestion
    2. Generate cinematic interpretations for all directors (in parallel)
    3. Judge and rank all interpretations
    4. Return the best result with explanations
    """
    
    def __init__(self):
        """
        Initialize the module with three different DSPy predictors.
        
        Notice the different types:
        - dspy.Predict: Basic prediction (fast, direct)
        - dspy.ChainOfThought: Reasoning-enabled prediction (slower, more thoughtful)
        """
        # Basic predictor for finding additional director
        self.findDirector = dspy.Predict(FindDirector)
        
        # Basic predictor for generating director cuts
        self.genDirectorCut = dspy.Predict(GenerateDirectorCut)
        
        # Chain-of-thought predictor for complex ranking decisions
        # This will make the LLM "think step by step" before ranking
        self.directorJudge = dspy.ChainOfThought(DirectorJudge)

    async def aforward(self, video_idea: str, directors: List[str] = ["Quentin Tarantino", "Alfred Hitchcock", "Richard Curtis"]):
        """
        🚀 ASYNC FORWARD: The Main Workflow
        
        This is where the magic happens! This method orchestrates the entire
        director bake-off process using multiple LLM calls.
        
        Key DSPy concepts demonstrated:
        1. Sequential LLM calls (find director first)
        2. Parallel LLM calls (generate all director cuts simultaneously)
        3. Complex data flow between signatures
        4. Async processing for efficiency
        
        Args:
            video_idea: The user's video concept
            directors: List of director names to compare
            
        Returns:
            ResultClass: Complete results including rankings and explanations
        """
        
        # === STEP 1: Display user input ===
        print("\n🎬 User Wanted Directors:")
        for director in directors:
            print(f"   - {director}")

        # === STEP 2: Find additional director suggestion ===
        print("\n🤖 Finding AI-suggested director...")
        additional_director_result = self.findDirector(
            video_idea=video_idea, 
            director_list=directors
        )
        additional_director = additional_director_result.additonal_director
        print(f"   ✨ DSPy Suggested Director: {additional_director}")

        # === STEP 3: Generate director interpretations (IN PARALLEL!) ===
        print("\n⚡ Generating director interpretations in parallel...")
        
        # Combine user directors + AI suggestion
        all_directors = directors + [additional_director]
        
        # Use asyncio.gather to run multiple LLM calls simultaneously
        # This is much faster than calling them one by one!
        director_ideas = await asyncio.gather(
            *[self.genDirectorCut.acall(video_idea=video_idea, director=director) 
              for director in all_directors]
        )
        
        # Display all generated ideas
        print("\n🎭 Generated Director Ideas:")
        for idea in director_ideas:
            idea.director_cut.pretty_print()

        # === STEP 4: Judge and rank all interpretations ===
        print("\n⚖️ Judging and ranking director ideas...")
        
        # Extract just the DirectorCut objects for judging
        director_cuts = [idea.director_cut for idea in director_ideas]
        
        # Use Chain-of-Thought for complex ranking decision
        director_ranks = self.directorJudge(director_ideas=director_cuts)

        # === STEP 5: Display rankings ===
        print("\n🏆 Director Rankings:")
        for rank, idea in zip(director_ranks.director_rankings, director_ideas):
            print(f"   Rank {rank}: {idea.director_cut.director}")

        # === STEP 6: Find and display the winner ===
        best_rank = min(director_ranks.director_rankings)
        best_index = director_ranks.director_rankings.index(best_rank)
        best_idea = director_ideas[best_index]
        
        print("\n🥇 WINNER - Best Ranked Director Idea:")
        best_idea.director_cut.pretty_print()
        
        print(f"\n💭 Judge's Reasoning:")
        print(f"   {director_ranks.explanation}")
        print("=" * 50)

        # === STEP 7: Return complete results ===
        return ResultClass(
            additional_director=additional_director,
            director_ideas=director_ideas,
            director_ranks=director_ranks
        )


# ==========================================================================
# SECTION 5: MAIN FUNCTIONS AND ENTRY POINT
# ==========================================================================

def run_bake_off(video_idea: str, directors: str = None) -> ResultClass:
    """
    🎯 MAIN FUNCTION: Easy-to-use interface for the Director Bake-Off
    
    This function provides a simple interface that handles:
    1. LLM setup and configuration
    2. Input validation and parsing
    3. Running the complete workflow
    4. Error handling
    
    This is the function that external code (like our Gradio interface)
    calls to use our DSPy system.
    
    Args:
        video_idea: A description of the video concept
        directors: Comma-separated string of director names (optional)
        
    Returns:
        ResultClass: Complete results from the bake-off
    """
    
    print("🚀 Running Director Bake-Off...")
    
    # === STEP 1: Ensure LLM is configured ===
    global lm
    if not lm:
        provider = setup_dspy_provider()
        print(f"   ✅ DSPy configured with {provider} provider.")
    
    # === STEP 2: Parse and validate director input ===
    if not (isinstance(directors, str) and directors.strip()):
        # Use default directors if none provided
        directors = ["Quentin Tarantino", "Alfred Hitchcock", "Richard Curtis"]
        print("   📝 Using default directors")
    else:
        # Parse comma-separated string into list
        directors = [d.strip() for d in directors.split(",") if d.strip()]
        if not directors:
            # Fallback to defaults if parsing failed
            directors = ["Quentin Tarantino", "Alfred Hitchcock", "Richard Curtis"]
            print("   📝 Parsing failed, using default directors")

    # === STEP 3: Create and run the bake-off ===
    bake_off = DirectorBakeOff()
    result_class = asyncio.run(bake_off.aforward(video_idea=video_idea, directors=directors))
    
    return result_class


# ==========================================================================
# SECTION 6: SCRIPT ENTRY POINT
# ==========================================================================

if __name__ == "__main__":
    """
    🎬 DEMO: Run the script directly to see it in action!
    
    This section only runs when you execute this file directly
    (not when it's imported as a module).
    
    Try running: python director_bake_off.py
    """
    print("🎭 DSPy Director Bake-Off Demo")
    print("=" * 40)
    
    # Run with a sample video idea
    sample_idea = "A futuristic cityscape with flying cars and neon lights."
    print(f"📝 Sample Video Idea: {sample_idea}")
    
    result = run_bake_off(sample_idea)
    
    print("\n🎉 Demo completed! Check the output above to see how each director")
    print("   would approach filming this futuristic cityscape.")
