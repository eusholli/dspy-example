#!/usr/bin/env python3

import gradio as gr
import asyncio
from director_bake_off import run_bake_off
import traceback

# Clean, professional light mode styling
LIGHT_MODE_CSS = """
/* Force light mode and override system preferences */
* {
    color-scheme: light !important;
}

/* Override any dark mode media queries */
@media (prefers-color-scheme: dark) {
    :root {
        color-scheme: light !important;
    }
    
    body, .gradio-container {
        background: #ffffff !important;
        color: #1f2937 !important;
    }
}

/* Clean, professional styling */
.gradio-container {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background: #ffffff !important;
    color: #1f2937 !important;
}

/* Header styling */
.main-header {
    text-align: center;
    padding: 2rem 0;
    background: #ffffff;
    border-bottom: 1px solid #e5e7eb;
    margin-bottom: 2rem;
}

.main-title {
    font-size: 2.25rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 0.5rem;
}

.main-subtitle {
    font-size: 1.125rem;
    color: #6b7280;
    font-weight: 400;
}

/* Force light backgrounds for ALL input containers and elements */
.gr-textbox, .gr-textarea, input, textarea,
.gr-textbox *, .gr-textarea *,
.gr-textbox > div, .gr-textarea > div,
.gradio-textbox, .gradio-textarea {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #1f2937 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 6px !important;
}

/* Force the container backgrounds to be light */
.gr-textbox, .gr-textarea {
    background: #ffffff !important;
    background-color: #ffffff !important;
}

/* Force all child elements to have light backgrounds */
.gr-textbox > *, .gr-textarea > *,
.gr-textbox > div > *, .gr-textarea > div > * {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #1f2937 !important;
}

.gr-textbox:focus, .gr-textarea:focus, input:focus, textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    outline: none !important;
    background: #ffffff !important;
    background-color: #ffffff !important;
}

/* Button styling */
.submit-btn {
    background: #3b82f6 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    transition: background-color 0.2s !important;
}

.submit-btn:hover {
    background: #2563eb !important;
}

/* Results styling */
.results-container {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1.5rem;
    margin-top: 1.5rem;
}

.director-card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.rank-badge {
    display: inline-block;
    background: #3b82f6;
    color: #ffffff;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.rank-1 { background: #f59e0b; }
.rank-2 { background: #6b7280; }
.rank-3 { background: #d97706; }

.director-name {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 1rem;
}

.prompt-text {
    background: #ffffff;
    color: #1f2937;
    padding: 1rem;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    line-height: 1.6;
    margin-bottom: 1rem;
}

.additional-director {
    background: #ecfdf5;
    border: 1px solid #d1fae5;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

.explanation-section {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1.5rem;
    margin-top: 1.5rem;
}

.section-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 1rem;
}

.loading {
    text-align: center;
    padding: 2rem;
    color: #6b7280;
}

/* Ensure all Gradio components use light mode */
.gr-block, .gr-form, .gr-box {
    background: #ffffff !important;
    color: #1f2937 !important;
}

/* Override any remaining dark mode styles */
.dark, [data-theme="dark"] {
    background: #ffffff !important;
    color: #1f2937 !important;
}

/* Force all text elements to be visible */
h1, h2, h3, h4, h5, h6, p, div, span, li, ol, ul {
    color: #1f2937 !important;
}

/* Ensure HTML content is visible */
.gr-html * {
    color: #1f2937 !important;
}

/* Force visibility for all text content */
* {
    color: #1f2937 !important;
}

/* Override Gradio's default text colors */
.gradio-container * {
    color: #1f2937 !important;
}

/* AGGRESSIVE LABEL VISIBILITY - Override all Gradio label styles */
.gr-label, .gr-label *, label, .label,
.gradio-textbox label, .gradio-textarea label,
[data-testid*="textbox"] label, [data-testid*="textarea"] label,
.gr-textbox .gr-label, .gr-textarea .gr-label,
.gr-textbox span[data-testid*="label"], .gr-textarea span[data-testid*="label"],
.gr-textbox .label, .gr-textarea .label,
.gr-form .gr-label, .gr-block .gr-label,
.gradio-container .gr-label, .gradio-container label,
.gr-textbox > span, .gr-textarea > span,
.gr-textbox > div > span, .gr-textarea > div > span,
.gr-textbox .svelte-*, .gr-textarea .svelte-*,
span[class*="label"], div[class*="label"],
.gr-textbox span:first-child, .gr-textarea span:first-child {
    color: #1f2937 !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    margin-bottom: 0.5rem !important;
    display: block !important;
    opacity: 1 !important;
    visibility: visible !important;
    background: transparent !important;
}

/* Target Gradio's internal label structure more aggressively */
.gr-textbox > div:first-child, .gr-textarea > div:first-child,
.gr-textbox > div:first-child > *, .gr-textarea > div:first-child > *,
.gr-textbox .svelte-1gfkn6j, .gr-textarea .svelte-1gfkn6j,
.gr-textbox .svelte-*, .gr-textarea .svelte-* {
    color: #1f2937 !important;
    font-weight: 600 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

/* Force all possible label selectors */
.gradio-container [class*="label"],
.gradio-container [data-testid*="label"],
.gradio-container .gr-textbox *:first-child,
.gradio-container .gr-textarea *:first-child {
    color: #1f2937 !important;
    font-weight: 600 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

/* Nuclear option - force ALL text in textbox containers to be visible */
.gr-textbox *, .gr-textarea * {
    color: #1f2937 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

/* NUCLEAR BACKGROUND OVERRIDE - Force all containers to be white */
.gr-textbox, .gr-textarea, 
.gr-textbox *, .gr-textarea *,
.gr-textbox > div, .gr-textarea > div,
.gr-textbox > div > div, .gr-textarea > div > div,
.gr-textbox > div > div > div, .gr-textarea > div > div > div,
[class*="textbox"], [class*="textarea"],
[data-testid*="textbox"], [data-testid*="textarea"] {
    background: #ffffff !important;
    background-color: #ffffff !important;
}

/* Override any blue/dark backgrounds specifically */
.gr-textbox [style*="background"], .gr-textarea [style*="background"],
.gr-textbox [style*="background-color"], .gr-textarea [style*="background-color"] {
    background: #ffffff !important;
    background-color: #ffffff !important;
}

/* Force white background on any element with blue/dark styling */
[style*="background: rgb("], [style*="background-color: rgb("],
[style*="background:#"], [style*="background-color:#"] {
    background: #ffffff !important;
    background-color: #ffffff !important;
}
"""

def format_results_html(result):
    """Format the results into clean, professional HTML."""
    if not result:
        return "<div class='loading'>No results to display.</div>"
    
    try:
        # Header with additional director suggestion
        html = f"""
        <div class="results-container">
            <div class="additional-director">
                <div class="section-title">🎬 AI Suggested Director</div>
                <div style="font-size: 1.1rem; color: #1f2937;">
                    <strong>{result.additional_director}</strong> - A perfect match for your vision!
                </div>
            </div>
        """
        
        # Director ideas with rankings
        html += '<div class="section-title">🏆 Director Interpretations (Ranked)</div>'
        
        # Sort director ideas by ranking
        ranked_ideas = []
        for i, idea in enumerate(result.director_ideas):
            rank = result.director_ranks.director_rankings[i]
            ranked_ideas.append((rank, idea.director_cut))
        
        ranked_ideas.sort(key=lambda x: x[0])  # Sort by rank (1 is best)
        
        for rank, director_cut in ranked_ideas:
            rank_class = f"rank-{min(rank, 3)}"  # Use rank-1, rank-2, rank-3 classes
            
            html += f"""
            <div class="director-card">
                <div class="rank-badge {rank_class}">#{rank}</div>
                <div class="director-name">{director_cut.director}</div>
                <div class="prompt-text">{director_cut.assemble_prompt()}</div>
                
                <details style="margin-top: 1rem;">
                    <summary style="cursor: pointer; font-weight: 500; color: #3b82f6;">
                        View Detailed Breakdown
                    </summary>
                    <div style="margin-top: 1rem; padding: 1rem; background: #f8fafc; border-radius: 6px; color: #1f2937;">
                        <div style="margin-bottom: 0.8rem;"><strong>Subject:</strong> {director_cut.subject_description}</div>
                        <div style="margin-bottom: 0.8rem;"><strong>Action:</strong> {director_cut.action_description}</div>
                        <div style="margin-bottom: 0.8rem;"><strong>Setting:</strong> {director_cut.setting_description}</div>
                        <div style="margin-bottom: 0.8rem;"><strong>Style:</strong> {director_cut.cinematic_style}</div>
                        <div style="margin-bottom: 0.8rem;"><strong>Shot & Framing:</strong> {director_cut.shot_and_framing}</div>
                        <div style="margin-bottom: 0.8rem;"><strong>Camera Movement:</strong> {director_cut.camera_movement}</div>
                        <div style="margin-bottom: 0.8rem;"><strong>Lighting & Color:</strong> {director_cut.lighting_and_color}</div>
                    </div>
                </details>
            </div>
            """
        
        # Explanation section with HTML formatting from DSPy
        html += f"""
            <div class="explanation-section">
                <div class="section-title">🤔 Judge's Reasoning</div>
                <div style="line-height: 1.8; color: #1f2937; font-size: 1rem;">
                    {result.director_ranks.explanation}
                </div>
            </div>
        </div>
        """
        
        return html
        
    except Exception as e:
        return f"""
        <div class="results-container">
            <div style="color: #dc2626; padding: 1rem; background: #fef2f2; border-radius: 8px;">
                <strong>Error formatting results:</strong> {str(e)}
            </div>
        </div>
        """

def run_director_bakeoff(video_idea, directors):
    """Run the director bake-off and return formatted results."""
    if not video_idea or not video_idea.strip():
        return "<div class='loading'>Please enter a video idea to get started!</div>"
    
    try:
        # Initial loading message with expectations
        yield """
        <div class='loading' style='background: #f0f9ff; padding: 2rem; border-radius: 8px; border-left: 4px solid #3b82f6;'>
            <div style='font-size: 1.3rem; font-weight: 600; color: #1f2937; margin-bottom: 1rem;'>
                🎬 Director Bake-Off in Progress...
            </div>
            <div style='font-size: 1rem; color: #6b7280; margin-bottom: 1.5rem; line-height: 1.6;'>
                Please be patient, this may take some minutes...<br>
                We're consulting with legendary directors to bring your vision to life!<br>
                <strong>This process typically takes 30-60 seconds.</strong><br>
                ✨
            </div>
            <div style='background: #ffffff; padding: 1rem; border-radius: 8px; border-left: 3px solid #f59e0b;'>
                <div style='font-size: 0.9rem; color: #1f2937;'>
                    <strong>What's happening:</strong><br>
                    • Finding the perfect additional director for your concept<br>
                    • Generating unique interpretations from each director<br>
                    • Ranking all concepts to find the best match<br>
                </div>
            </div>
        </div>
        """
        
        # Run the bake-off
        result = run_bake_off(video_idea, directors)
        
        # Format and return results
        formatted_html = format_results_html(result)
        yield formatted_html
        
    except Exception as e:
        error_html = f"""
        <div class="results-container">
            <div style="color: #e74c3c; padding: 1.5rem; background: #fdf2f2; border-radius: 8px; border-left: 4px solid #e74c3c;">
                <div style="font-weight: 600; margin-bottom: 0.5rem;">Something went wrong!</div>
                <div style="margin-bottom: 1rem;">{str(e)}</div>
                <details>
                    <summary style="cursor: pointer; color: #c0392b;">View technical details</summary>
                    <pre style="margin-top: 1rem; font-size: 0.85rem; background: #f8f8f8; padding: 1rem; border-radius: 4px; overflow-x: auto;">
{traceback.format_exc()}
                    </pre>
                </details>
            </div>
        </div>
        """
        yield error_html

# Create the Gradio interface
def create_interface():
    # Force light mode theme
    light_theme = gr.themes.Default(
        primary_hue="blue",
        secondary_hue="gray", 
        neutral_hue="gray"
    )
    
    with gr.Blocks(css=LIGHT_MODE_CSS, theme=light_theme, title="Director Bake-Off Studio") as interface:
        # Header
        gr.HTML("""
        <div class="main-header">
            <h1 class="main-title">Director Bake-Off Studio</h1>
            <p class="main-subtitle">Let legendary directors compete to bring your vision to life</p>
        </div>
        """)
        
        # How it Works section - moved to top
        gr.HTML("""
        <div style="background: #f0f9ff; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; border-left: 4px solid #3b82f6;">
            <h3 style="margin-top: 0; color: #1f2937;">How it works:</h3>
            <ol style="color: #1f2937; line-height: 1.6;">
                <li>Enter your video idea in the text area below</li>
                <li>List your favorite directors (or use our defaults)</li>
                <li>Our AI will suggest an additional director perfect for your vision</li>
                <li>Watch as each director creates their unique interpretation</li>
                <li>See them ranked by how well they match your concept!</li>
            </ol>
        </div>
        """)
        
        # Results section - will only show content when there are actual results
        results_html = gr.HTML(
            value="",
            elem_classes=["results-display"],
            visible=False
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                # Input section
                
                video_idea = gr.Textbox(
                    label="🎥 Your Video Idea",
                    placeholder="Describe your video concept... (e.g., 'A futuristic cityscape with flying cars and neon lights')",
                    lines=4,
                    elem_classes=["input-field"]
                )
                
                directors = gr.Textbox(
                    label="🎬 Directors (comma-separated)",
                    placeholder="e.g., Quentin Tarantino, Alfred Hitchcock",
                    value="Quentin Tarantino, Alfred Hitchcock",
                    lines=2,
                    elem_classes=["input-field"]
                )
                
                submit_btn = gr.Button(
                    "🚀 Start the Bake-Off!",
                    elem_classes=["submit-btn"],
                    variant="primary"
                )
                        
        # Set up the interaction - removed show_progress=True to eliminate progress bar
        def handle_submit(video_idea, directors):
            # Make results visible and update content
            for result in run_director_bakeoff(video_idea, directors):
                yield gr.update(value=result, visible=True)
        
        submit_btn.click(
            fn=handle_submit,
            inputs=[video_idea, directors],
            outputs=[results_html]
        )
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; padding: 2rem; color: #6b7280; font-size: 0.9rem;">
            <p>Powered by DSPy and the creative genius of legendary directors 🎬</p>
        </div>
        """)
    
    return interface

if __name__ == "__main__":
    # Create and launch the interface
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        debug=True
    )
