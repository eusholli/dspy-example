#!/usr/bin/env python3

import gradio as gr
import asyncio
from director_bake_off import run_bake_off
import traceback

# Swedish-inspired color palette and styling
SWEDISH_CSS = """
/* Swedish Minimalist Design */
:root {
    --primary-white: #FFFFFF;
    --soft-gray: #F5F5F5;
    --muted-blue: #4A90A4;
    --warm-beige: #E8DCC6;
    --charcoal: #2C2C2C;
    --light-blue: #E8F4F8;
    --accent-gold: #D4AF37;
    --success-green: #7FB069;
    --border-gray: #E0E0E0;
}

/* Global styling */
.gradio-container {
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    background: linear-gradient(135deg, var(--soft-gray) 0%, var(--primary-white) 100%) !important;
    min-height: 100vh;
}

/* Header styling */
.main-header {
    text-align: center;
    padding: 2rem 0;
    background: var(--primary-white);
    border-bottom: 1px solid var(--border-gray);
    margin-bottom: 2rem;
}

.main-title {
    font-size: 2.5rem;
    font-weight: 300;
    color: var(--charcoal);
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}

.main-subtitle {
    font-size: 1.1rem;
    color: var(--muted-blue);
    font-weight: 400;
    margin-bottom: 0;
}

/* Input section styling */
.input-section {
    background: var(--primary-white);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 2px 20px rgba(0,0,0,0.05);
    border: 1px solid var(--border-gray);
    margin-bottom: 2rem;
}

.input-label {
    font-size: 1rem;
    font-weight: 500;
    color: var(--charcoal);
    margin-bottom: 0.5rem;
    display: block;
}

/* Button styling */
.submit-btn {
    background: linear-gradient(135deg, var(--muted-blue) 0%, #5BA0B5 100%) !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 32px !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
    color: white !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(74, 144, 164, 0.3) !important;
}

.submit-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(74, 144, 164, 0.4) !important;
}

/* Results section */
.results-container {
    background: var(--primary-white);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 2px 20px rgba(0,0,0,0.05);
    border: 1px solid var(--border-gray);
    margin-top: 2rem;
}

.director-card {
    background: var(--light-blue);
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border-left: 4px solid var(--muted-blue);
    transition: all 0.3s ease;
}

.director-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.rank-badge {
    display: inline-block;
    background: var(--accent-gold);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.rank-1 { background: var(--accent-gold); }
.rank-2 { background: #C0C0C0; }
.rank-3 { background: #CD7F32; }

.director-name {
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--charcoal);
    margin-bottom: 1rem;
}

.prompt-text {
    font-size: 1rem;
    line-height: 1.6;
    color: var(--charcoal);
    background: var(--primary-white);
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid var(--border-gray);
    margin-bottom: 1rem;
}

.additional-director {
    background: var(--warm-beige);
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    border-left: 4px solid var(--success-green);
}

.explanation-section {
    background: var(--soft-gray);
    border-radius: 10px;
    padding: 1.5rem;
    margin-top: 2rem;
    border-left: 4px solid var(--muted-blue);
}

.section-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--charcoal);
    margin-bottom: 1rem;
}

/* Loading animation */
.loading {
    text-align: center;
    padding: 2rem;
    color: var(--muted-blue);
}

/* Responsive design */
@media (max-width: 768px) {
    .main-title {
        font-size: 2rem;
    }
    
    .input-section, .results-container {
        padding: 1.5rem;
        margin: 1rem;
    }
    
    .director-card {
        padding: 1rem;
    }
}

/* Custom textbox styling */
.gr-textbox {
    border-radius: 8px !important;
    border: 1px solid var(--border-gray) !important;
}

.gr-textbox:focus {
    border-color: var(--muted-blue) !important;
    box-shadow: 0 0 0 3px rgba(74, 144, 164, 0.1) !important;
}
"""

def format_results_html(result):
    """Format the results into beautiful HTML with Swedish design."""
    if not result:
        return "<div class='loading'>No results to display.</div>"
    
    try:
        # Header with additional director suggestion
        html = f"""
        <div class="results-container">
            <div class="additional-director">
                <div class="section-title">🎬 AI Suggested Director</div>
                <div style="font-size: 1.1rem; color: var(--charcoal);">
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
                    <summary style="cursor: pointer; font-weight: 500; color: var(--muted-blue);">
                        View Detailed Breakdown
                    </summary>
                    <div style="margin-top: 1rem; padding: 1rem; background: var(--soft-gray); border-radius: 6px;">
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
                <div style="line-height: 1.8; color: var(--charcoal); font-size: 1rem;">
                    {result.director_ranks.explanation}
                </div>
            </div>
        </div>
        """
        
        return html
        
    except Exception as e:
        return f"""
        <div class="results-container">
            <div style="color: #e74c3c; padding: 1rem; background: #fdf2f2; border-radius: 8px;">
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
        <div class='loading' style='background: var(--light-blue); padding: 2rem; border-radius: 12px; border-left: 4px solid var(--muted-blue);'>
            <div style='font-size: 1.3rem; font-weight: 600; color: var(--charcoal); margin-bottom: 1rem;'>
                🎬 Director Bake-Off in Progress...
            </div>
            <div style='font-size: 1rem; color: var(--muted-blue); margin-bottom: 1.5rem; line-height: 1.6;'>
                Please be patient, this may take some minutes...<br>
                We're consulting with legendary directors to bring your vision to life!<br>
                <strong>This process typically takes 30-60 seconds.</strong><br>
                ✨
            </div>
            <div style='background: var(--primary-white); padding: 1rem; border-radius: 8px; border-left: 3px solid var(--accent-gold);'>
                <div style='font-size: 0.9rem; color: var(--charcoal);'>
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
    with gr.Blocks(css=SWEDISH_CSS, title="Director Bake-Off Studio") as interface:
        # Header
        gr.HTML("""
        <div class="main-header">
            <h1 class="main-title">Director Bake-Off Studio</h1>
            <p class="main-subtitle">Let legendary directors compete to bring your vision to life</p>
        </div>
        """)
        
        # How it Works section - moved to top
        gr.HTML("""
        <div style="background: var(--light-blue); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; border-left: 4px solid var(--muted-blue);">
            <h3 style="margin-top: 0; color: var(--charcoal);">How it works:</h3>
            <ol style="color: var(--charcoal); line-height: 1.6;">
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
        <div style="text-align: center; padding: 2rem; color: var(--muted-blue); font-size: 0.9rem;">
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
