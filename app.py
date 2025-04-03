import streamlit as st
import pandas as pd
import io
import base64
import humanizer
import text_utils
import time
import os
from datetime import datetime
import achievements  # Import our achievements module

# Initialize NLTK data if needed
try:
    import nltk
    nltk.download('punkt', quiet=True)
except ImportError:
    # If NLTK is not available, we'll use our fallback functions in text_utils
    pass

# Set page config
st.set_page_config(
    page_title="Dx3n Text Humanizer",
    page_icon="📝",
    layout="wide"
)

# Initialize session state for examples and achievements
if 'show_example' not in st.session_state:
    st.session_state.show_example = False
    
# Initialize the achievement system
if 'achievement_system' not in st.session_state:
    st.session_state.achievement_system = achievements.AchievementSystem()

# Header with welcoming design
st.title("✨ Dx3n Text Humanizer ✨")
st.markdown("""
### Make your AI-written content sound like it was written by a human
Created by **Huzaifah Tahir** (aka **Dx3n**) | No technical knowledge required - just paste your text and click a button!
""")

# Add some space
st.write("")

# Create tabs for main content
tab1, tab2, tab3, tab4, tab5 = st.tabs(["✏️ Humanize Text", "❓ How It Works", "📊 Examples", "💾 My Saved Texts", "🏆 Achievements"])

with tab1:
    # Main content area with instructions
    st.markdown("""
    ### 👇 Just follow these simple steps:
    1. Paste your text in the box below or upload a file
    2. Adjust the humanization level if needed (or keep the default)
    3. Click the "Humanize My Text" button
    4. Get your human-sounding text in seconds!
    """)

    # Main content columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Your Original Text")
        
        # Text input options with explanatory text
        input_method = st.radio(
            "Choose how to add your text:", 
            ["✍️ Type or paste text", "📁 Upload a text file"],
            captions=["Copy-paste directly from any source", "Upload a .txt file from your computer"]
        )
        
        if input_method == "✍️ Type or paste text":
            input_text = st.text_area(
                "Paste your AI-generated text here:",
                height=300,
                placeholder="Enter text to humanize...\n\nFor example: The utilization of artificial intelligence in educational contexts provides numerous advantages for students and educators alike. It facilitates personalized learning experiences, automates administrative tasks, and enables data-driven decision making."
            )
            
            # Example button
            if not input_text:
                if st.button("📝 Load Example Text"):
                    st.session_state.show_example = True
                    
            if st.session_state.show_example:
                example_text = """"Hello" is a monosyllable of extraordinary power, a cultural bridge across linguistic divides, called upon to initiate conversation, express solidarity, and create relationship. Whether in physical presence or executed through electronic interfaces, to greet a person with "hello" is the manner of initiating communication and creating human connections. It is a term that sums up friendliness, interest, and receptiveness to engagement with the other, however fleeting or casual the encounter may be. From a warm wave to a warm smile, the act of greeting a person with "hello" can be the initiation of momentous conversation with someone, be it a stranger, acquaintance, or close person"""
                input_text = example_text
                st.rerun()
                
        else:
            uploaded_file = st.file_uploader(
                "Upload a text file", 
                type=["txt"],
                help="Your file will be processed securely and not stored permanently"
            )
            if uploaded_file is not None:
                input_text = uploaded_file.getvalue().decode("utf-8")
                st.text_area("File content:", input_text, height=300)
                
                # Track achievement for file upload if not already tracked in this session
                if 'file_uploaded' not in st.session_state or not st.session_state.file_uploaded:
                    newly_unlocked = st.session_state.achievement_system.track_file_upload()
                    st.session_state.file_uploaded = True
                    
                    # Show achievement notifications if any were unlocked
                    if newly_unlocked:
                        for achievement in newly_unlocked:
                            st.balloons()
                            st.success(f"🏆 Achievement Unlocked: **{achievement['name']}** ({achievement['points']} points)")
            else:
                input_text = ""
                st.info("👆 Upload a .txt file to see its content here")
        
        # Display text statistics for input
        if input_text:
            with st.expander("📊 Text Statistics", expanded=False):
                stats = text_utils.get_text_statistics(input_text)
                st.write(f"**Word Count:** {stats['word_count']}")
                st.write(f"**Sentence Count:** {stats['sentence_count']}")
                st.write(f"**Average Sentence Length:** {stats['avg_sentence_length']:.1f} words")
                st.write(f"**Average Word Length:** {stats['avg_word_length']:.1f} characters")
    
    # Settings panel between columns
    st.write("")
    with st.expander("⚙️ Adjust Settings (optional)", expanded=False):
        humanize_level = st.slider(
            "Humanization Level", 
            min_value=1, 
            max_value=5, 
            value=3,
            help="Different levels provide varying styles of humanization, from subtle to scholarly"
        )
        st.caption("""
        **What does this mean?**
        - **Level 1:** Subtle changes, very close to original
        - **Level 3:** Balanced approach (recommended)
        - **Level 5:** Scholarly formality with sophisticated vocabulary and elegant structure
        """)
        
        # Advanced settings
        st.write("---")
        st.write("**Advanced Options** (requires API keys)")
        
        # Optional API integrations
        use_gemini = st.checkbox(
            "Use Gemini AI for enhanced processing", 
            value=False,
            help="Requires Gemini API key in environment variables"
        )
        
        if use_gemini and not os.getenv("GEMINI_API_KEY"):
            st.warning("⚠️ Gemini API key not found. The app will use the built-in humanizer instead.")
            st.caption("To use Gemini, you'll need to add your API key in the settings.")
        
        use_plagiarism_check = st.checkbox(
            "Run plagiarism check on humanized text", 
            value=False,
            help="Requires Google API key in environment variables"
        )
        
        if use_plagiarism_check and not os.getenv("GOOGLE_API_KEY"):
            st.warning("⚠️ Google API key not found. Plagiarism check will not run.")
            st.caption("To enable this feature, you'll need to add your Google API key in the settings.")
    
    # Action button between columns
    st.write("")
    if not input_text:
        st.info("👆 Enter some text above to get started")
    
    humanize_button = st.button(
        "🪄 Humanize My Text", 
        type="primary", 
        disabled=not input_text,
        use_container_width=True
    )
    
    with col2:
        st.markdown("### 👤 Humanized Result")
        
        if humanize_button:
            if not input_text:
                st.error("Please enter some text first.")
            else:
                with st.spinner("✨ Working magic on your text..."):
                    # Process text with progress bar and friendly messages
                    progress_bar = st.progress(0)
                    
                    # Simulate processing stages with friendly messages
                    progress_messages = [
                        "Analyzing text patterns...",
                        "Finding natural alternatives...",
                        "Adding human-like variations...",
                        "Finalizing your text..."
                    ]
                    
                    for i, message in enumerate(progress_messages):
                        progress_value = (i + 1) * 20
                        progress_bar.progress(progress_value)
                        st.caption(message)
                        time.sleep(0.3)
                    
                    # Apply humanization
                    try:
                        humanized_text = humanizer.humanize_text(
                            input_text, 
                            level=humanize_level,
                            use_gemini=use_gemini
                        )
                        progress_bar.progress(90)
                        st.caption("Putting final touches...")
                        time.sleep(0.2)
                        
                        # Run plagiarism check if requested
                        plagiarism_result = None
                        if use_plagiarism_check:
                            with st.spinner("🔍 Checking for plagiarism..."):
                                plagiarism_result = text_utils.check_plagiarism(humanized_text)
                        
                        progress_bar.progress(100)
                        
                        # Store the result in session state
                        st.session_state.humanized_text = humanized_text
                        st.session_state.plagiarism_result = plagiarism_result
                        st.session_state.original_text = input_text
                        
                        # Track achievement for humanizing text
                        newly_unlocked = st.session_state.achievement_system.track_humanization(
                            humanized_text, 
                            humanize_level
                        )
                        
                        # Show achievement notifications if any were unlocked
                        if newly_unlocked:
                            for achievement in newly_unlocked:
                                st.balloons()
                                st.success(f"🏆 Achievement Unlocked: **{achievement['name']}** ({achievement['points']} points)")
                                time.sleep(0.5)
                        
                    except Exception as e:
                        st.error(f"Oops! Something went wrong: {str(e)}")
                        st.info("Try again with different text or settings")
                        st.session_state.humanized_text = None
                        st.session_state.plagiarism_result = None
        
        # Display the humanized text if available
        if hasattr(st.session_state, 'humanized_text') and st.session_state.humanized_text:
            humanized_text = st.session_state.humanized_text
            st.text_area("Your human-like text is ready:", humanized_text, height=300)
            
            st.success("✅ Text successfully humanized!")
            
            # Action buttons for the result
            col_a, col_b = st.columns(2)
            
            with col_a:
                # Download button
                bio = io.BytesIO()
                bio.write(humanized_text.encode())
                bio.seek(0)
                
                st.download_button(
                    label="📥 Download as Text File",
                    data=bio,
                    file_name="humanized_text.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col_b:
                # Copy button
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    st.success("✓ Text copied to clipboard!")
            
            # Comparison
            with st.expander("📊 Before & After Comparison", expanded=True):
                if hasattr(st.session_state, 'original_text'):
                    similarity = text_utils.calculate_similarity(st.session_state.original_text, humanized_text)
                    
                    st.write("**Text Similarity:** How much of the original text was preserved")
                    st.progress(similarity/100)
                    st.caption(f"{similarity:.1f}% similar to original text")
                    
                    # Side-by-side comparison
                    st.write("**Quick Comparison:**")
                    comparison_df = pd.DataFrame({
                        "Original Text": [st.session_state.original_text[:100] + "..."],
                        "Humanized Text": [humanized_text[:100] + "..."]
                    })
                    st.dataframe(comparison_df, use_container_width=True)
            
            # Display detailed statistics
            with st.expander("📊 Detailed Text Statistics", expanded=False):
                col_stats1, col_stats2 = st.columns(2)
                
                with col_stats1:
                    st.subheader("Original Text")
                    stats = text_utils.get_text_statistics(st.session_state.original_text)
                    st.write(f"**Word Count:** {stats['word_count']}")
                    st.write(f"**Sentence Count:** {stats['sentence_count']}")
                    st.write(f"**Avg Sentence Length:** {stats['avg_sentence_length']:.1f} words")
                    st.write(f"**Avg Word Length:** {stats['avg_word_length']:.1f} characters")
                
                with col_stats2:
                    st.subheader("Humanized Text")
                    stats = text_utils.get_text_statistics(humanized_text)
                    st.write(f"**Word Count:** {stats['word_count']}")
                    st.write(f"**Sentence Count:** {stats['sentence_count']}")
                    st.write(f"**Avg Sentence Length:** {stats['avg_sentence_length']:.1f} words")
                    st.write(f"**Avg Word Length:** {stats['avg_word_length']:.1f} characters")
            
            # Display plagiarism check results if available
            if hasattr(st.session_state, 'plagiarism_result') and st.session_state.plagiarism_result:
                with st.expander("🔍 Plagiarism Check Results", expanded=False):
                    st.write(st.session_state.plagiarism_result)
        
        else:
            # Show empty state with instructions
            st.info("👈 Enter your text on the left and click the 'Humanize My Text' button to see results here")
            st.write("")
            st.write("Your humanized text will appear in this box.")

# How it works tab
with tab2:
    st.markdown("""
    ## 🔍 How Dx3n Text Humanizer Works
    
    Created by **Huzaifah Tahir** (aka **Dx3n**), this tool transforms AI-generated writing into text that sounds naturally human-written.
    It's perfect for:
    
    - ✅ Students who want to make AI-assisted work sound more authentic
    - ✅ Content creators looking to humanize AI-generated drafts
    - ✅ Anyone who needs to make ChatGPT content more conversational and bypass AI detection
    
    ### The Advanced Process:
    
    1. **Text Analysis**: We analyze your AI-generated text patterns and content fingerprints
    2. **Style Selection**: We determine the appropriate humanization style (casual, business, scholarly)
    3. **Natural Variations**: We add human-like inconsistencies, typos, and self-corrections
    4. **Language Enhancement**: We adjust phrasing to match natural human language patterns
    5. **Stealth Features**: We implement advanced anti-detection technology including homoglyphs, invisible Unicode patterns, and linguistic deception techniques
    
    ### Humanization Levels Explained:
    
    | Level | What It Does | Best For |
    |-------|-------------|----------|
    | 1️⃣ | Subtle changes, preserves almost all original content | Academic/professional content |
    | 2️⃣ | Light humanization with minor phrasing adjustments | Business communications |
    | 3️⃣ | Balanced approach - our recommended setting | General purpose |
    | 4️⃣ | Significant humanization with more casual style | Blog posts, social media |
    | 5️⃣ | Scholarly style with elevated vocabulary and sophisticated structure | Formal academic writing |
    
    ### Advanced Anti-Detection Features
    
    - **Unicode Homoglyphs**: Replaces select characters with visually identical ones from other alphabets
    - **Human Error Patterns**: Adds realistic typos, punctuation errors, and self-corrections
    - **Invisible Timing Markers**: Inserts hidden characters that mimic human typing rhythm
    - **Statistical Pattern Breaking**: Disrupts AI-generated statistical patterns with human-like variations
    - **Golden Ratio Positioning**: Places special characters at positions that match natural human writing patterns
    
    ### API Integrations
    
    - **Gemini AI**: For premium quality humanization (requires API key)
    - **Plagiarism Check**: Verify your text is unique (requires Google API key)
    """)

# Examples tab
with tab3:
    st.markdown("""
    ## 📝 Example Transformations
    
    See how Dx3n Text Humanizer transforms various types of content:
    """)
    
    example_tabs = st.tabs(["Academic", "Business", "Creative", "Scholarly"])
    
    with example_tabs[0]:
        st.subheader("Academic Writing Example")
        
        st.markdown("**🤖 Original AI-Generated:**")
        st.markdown("""
        The implementation of machine learning algorithms in healthcare settings has demonstrated significant potential for improving diagnostic accuracy. Studies indicate that neural networks can identify patterns in medical imaging with precision comparable to or exceeding that of trained professionals. Furthermore, the utilization of predictive analytics facilitates early intervention strategies and optimizes resource allocation.
        """)
        
        st.markdown("**👤 Humanized Version:**")
        st.markdown("""
        Machine learning algorithms in healthcare have shown remarkable promise in boosting diagnostic accuracy. Research suggests that neural networks can spot patterns in medical images just as well as—or sometimes better than—trained professionals. Plus, using predictive analytics helps doctors intervene earlier and make better use of available resources.
        """)

    with example_tabs[1]:
        st.subheader("Business Content Example")
        
        st.markdown("**🤖 Original AI-Generated:**")
        st.markdown("""
        Our quarterly financial analysis indicates a 15% increase in revenue attributed to the implementation of our new customer engagement strategy. The optimization of our digital marketing channels resulted in a 22% reduction in customer acquisition costs while simultaneously enhancing conversion rates. We anticipate continued growth in the subsequent fiscal period.
        """)
        
        st.markdown("**👤 Humanized Version:**")
        st.markdown("""
        Our quarterly financial analysis shows we've seen a 15% revenue bump, thanks to our new customer engagement strategy. We've also managed to cut our customer acquisition costs by about 22% by fine-tuning our digital marketing channels, and at the same time, we're actually converting more customers. I'm pretty confident we'll keep this momentum going into the next quarter.
        """)

    with example_tabs[2]:
        st.subheader("Creative Writing Example")
        
        st.markdown("**🤖 Original AI-Generated:**")
        st.markdown("""
        The protagonist, faced with an insurmountable challenge, exhibited remarkable resilience in their pursuit of justice. The narrative arc demonstrates the character's evolution from uncertainty to empowerment, culminating in a resolution that subverts audience expectations while maintaining thematic consistency.
        """)
        
        st.markdown("**👤 Humanized Version:**")
        st.markdown("""
        The main character, up against what seemed like an impossible challenge, showed incredible grit while fighting for justice. Throughout the story, you can see them transform from someone filled with doubt to a person who really owns their power. The ending catches you off guard but still feels right for the themes of the story.
        """)
        
    with example_tabs[3]:
        st.subheader("Scholarly Writing Example (Level 5)")
        
        st.markdown("**🤖 Original AI-Generated:**")
        st.markdown("""
        The analysis of linguistic patterns across multiple domains shows that language evolution is affected by social dynamics and technological change. Research has demonstrated that digital communication platforms accelerate the adoption of neologisms and grammatical simplifications. Furthermore, the spread of linguistic innovations follows predictable network patterns similar to those observed in other complex systems.
        """)
        
        st.markdown("**👤 Scholarly Humanized Version:**")
        st.markdown("""
        The examination of linguistic patterns across diverse domains manifests that language evolution is influenced by social dynamics and technological transformation. Research demonstrates that digital communication interfaces expedite the adoption of neologisms and grammatical reductions. Moreover, the dissemination of linguistic innovations adheres to predictable network configurations analogous to those observed in alternative complex systems. It is noteworthy that these patterns, heretofore unexplained through conventional models, operate within the established parameters of evolutionary linguistics, notwithstanding their accelerated tempo.
        """)

# Now using the fourth tab for database functionality

with tab4:
    import database
    
    # Initialize the database
    db = database.TextDatabase()
    
    st.title("💾 My Saved Texts")
    st.markdown("""
    Keep track of all your humanized texts. You can save, view, and manage your text transformations here.
    No account needed - your texts are stored locally.
    """)
    
    # Get database statistics
    stats = db.get_stats()
    
    # Show stats in a nice format
    st.write("")
    st.subheader("📈 Your Activity")
    
    # Display stats in columns
    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
    
    with col_stats1:
        st.metric("Total Saved Texts", stats["total_entries"])
    
    with col_stats2:
        st.metric("Words Processed", stats["total_words_processed"])
    
    with col_stats3:
        st.metric("Avg. Humanize Level", stats["avg_humanize_level"])
    
    with col_stats4:
        if stats["most_recent"]:
            # Format date for display
            try:
                date_str = datetime.fromisoformat(stats["most_recent"]).strftime("%Y-%m-%d")
                st.metric("Last Activity", date_str)
            except:
                st.metric("Last Activity", "Recent")
        else:
            st.metric("Last Activity", "None")
    
    # Create tabs for viewing and managing saved texts
    saved_tabs = st.tabs(["View Saved Texts", "Save Current Text", "Search"])
    
    with saved_tabs[0]:
        st.subheader("Previously Saved Texts")
        
        all_texts = db.get_all_texts()
        
        if not all_texts:
            st.info("You haven't saved any texts yet. Humanize some text and save it to see it here!")
        else:
            for i, text in enumerate(all_texts):
                with st.expander(f"Text #{i+1} - Level {text['humanize_level']} - {text['created_at'][:10]}"):
                    st.markdown("**Original Text:**")
                    st.text(text["original_text"][:200] + "..." if len(text["original_text"]) > 200 else text["original_text"])
                    
                    st.markdown("**Humanized Text:**")
                    st.text(text["humanized_text"][:200] + "..." if len(text["humanized_text"]) > 200 else text["humanized_text"])
                    
                    # Action buttons
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button(f"Load Text #{i+1}", key=f"load_{text['id']}"):
                            # Set session state values to load this text in the main interface
                            st.session_state.show_example = False
                            st.session_state.original_text = text["original_text"]
                            st.session_state.humanized_text = text["humanized_text"]
                            st.session_state.loaded_from_db = True
                            st.rerun()
                    
                    with col2:
                        if st.button(f"Delete #{i+1}", key=f"delete_{text['id']}"):
                            db.delete_text(text["id"])
                            st.success(f"Text #{i+1} deleted!")
                            time.sleep(1)
                            st.rerun()
    
    with saved_tabs[1]:
        st.subheader("Save Current Text")
        
        # Check if there's text to save
        if hasattr(st.session_state, 'humanized_text') and st.session_state.humanized_text:
            st.info("Your current humanized text is ready to save.")
            
            # Collect additional metadata
            note = st.text_input("Add a note (optional):", 
                                placeholder="E.g., 'Essay introduction', 'Blog post', etc.")
            
            tags = st.text_input("Add tags (comma separated, optional):", 
                                placeholder="E.g., academic, business, creative")
            
            if st.button("💾 Save Current Text", type="primary"):
                # Save the current text to the database
                entry_id = db.save_text(
                    original_text=st.session_state.original_text,
                    humanized_text=st.session_state.humanized_text,
                    humanize_level=humanize_level,
                    metadata={
                        "note": note,
                        "tags": [tag.strip() for tag in tags.split(",")] if tags else []
                    }
                )
                
                st.success("✅ Text successfully saved!")
                
                # Track achievement for saving text
                newly_unlocked = st.session_state.achievement_system.track_text_save()
                
                # Show achievement notifications if any were unlocked
                if newly_unlocked:
                    for achievement in newly_unlocked:
                        st.balloons()
                        st.success(f"🏆 Achievement Unlocked: **{achievement['name']}** ({achievement['points']} points)")
        else:
            st.warning("No humanized text available to save. Please create one first.")
            
            if st.button("Go to Text Humanizer"):
                # Switch to the humanize tab
                st.session_state.active_tab = "humanize"
                st.rerun()
    
    with saved_tabs[2]:
        st.subheader("Search Saved Texts")
        
        search_query = st.text_input("Search term:", placeholder="Enter keywords to search")
        
        if search_query:
            results = db.search_texts(search_query)
            
            # Track achievement for searching saved texts
            newly_unlocked = st.session_state.achievement_system.track_text_search()
            
            # Show achievement notifications if any were unlocked
            if newly_unlocked:
                for achievement in newly_unlocked:
                    st.balloons()
                    st.success(f"🏆 Achievement Unlocked: **{achievement['name']}** ({achievement['points']} points)")
            
            if not results:
                st.info(f"No texts found containing '{search_query}'")
            else:
                st.success(f"Found {len(results)} results for '{search_query}'")
                
                for i, text in enumerate(results):
                    with st.expander(f"Result #{i+1}"):
                        st.markdown("**Original Text:**")
                        st.text(text["original_text"][:200] + "..." if len(text["original_text"]) > 200 else text["original_text"])
                        
                        st.markdown("**Humanized Text:**")
                        st.text(text["humanized_text"][:200] + "..." if len(text["humanized_text"]) > 200 else text["humanized_text"])
                        
                        if st.button(f"Load Result #{i+1}", key=f"load_result_{text['id']}"):
                            st.session_state.show_example = False
                            st.session_state.original_text = text["original_text"]
                            st.session_state.humanized_text = text["humanized_text"]
                            st.session_state.loaded_from_db = True
                            st.rerun()

# Achievements tab
with tab5:
    st.title("🏆 Your Achievements")
    st.markdown("""
    Unlock achievements as you use the Dx3n Text Humanizer. Track your progress, earn points, and level up!
    """)
    
    # Get user stats
    achievement_system = st.session_state.achievement_system
    stats = achievement_system.get_stats()
    level_progress = achievement_system.get_level_progress()
    
    # Display user level and points in a prominent way
    st.markdown(f"## 👑 Current Level: **{stats['level']}**")
    
    # Create a progress bar for level progress
    if level_progress['next_level'] is not None:
        st.markdown(f"**Progress to {level_progress['next_level']}**")
        st.progress(level_progress['progress_percent'] / 100)
        st.text(f"{stats['total_points']} points / {level_progress['points_needed']} more points needed")
    else:
        st.markdown("**🌟 Maximum Level Reached!**")
        st.progress(1.0)
        st.text(f"Total: {stats['total_points']} points")
    
    # Show achievement statistics
    st.markdown("## 📊 Your Progress")
    
    # Display key metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Points", stats["total_points"])
    
    with col2:
        st.metric("Achievements Unlocked", f"{stats['achievements_unlocked']} / {len(achievement_system.get_all_achievements())}")
    
    with col3:
        # Calculate completion percentage
        completion = int((stats['achievements_unlocked'] / len(achievement_system.get_all_achievements())) * 100)
        st.metric("Completion", f"{completion}%")
    
    # Create tabs for different views of achievements
    achievement_tabs = st.tabs(["🔓 Unlocked", "🔒 Locked", "📋 All Achievements", "📊 By Category"])
    
    with achievement_tabs[0]:
        unlocked = achievement_system.get_unlocked_achievements()
        if not unlocked:
            st.info("You haven't unlocked any achievements yet. Start using the humanizer to earn some!")
        else:
            st.markdown(f"### 🏆 Unlocked Achievements ({len(unlocked)})")
            for ach in unlocked:
                with st.expander(f"{ach['icon']} {ach['name']} (+{ach['points']} pts)"):
                    st.markdown(f"**Description:** {ach['description']}")
                    st.markdown(f"**Category:** {achievements.CATEGORIES[ach['category']]}")
                    if ach.get('date_unlocked'):
                        try:
                            # Format the date string
                            from datetime import datetime
                            date_obj = datetime.fromisoformat(ach['date_unlocked'])
                            formatted_date = date_obj.strftime("%Y-%m-%d %H:%M")
                            st.markdown(f"**Unlocked on:** {formatted_date}")
                        except:
                            st.markdown(f"**Unlocked on:** {ach['date_unlocked']}")
    
    with achievement_tabs[1]:
        locked = achievement_system.get_locked_achievements()
        if not locked:
            st.success("Congratulations! You've unlocked all achievements!")
        else:
            st.markdown(f"### 🔒 Locked Achievements ({len(locked)})")
            for ach in locked:
                with st.expander(f"{ach['icon']} {ach['name']} (+{ach['points']} pts)"):
                    st.markdown(f"**Description:** {ach['description']}")
                    st.markdown(f"**Category:** {achievements.CATEGORIES[ach['category']]}")
                    
                    # Show progress bar
                    progress = min(ach['progress'], ach['progress_max'])
                    progress_percent = (progress / ach['progress_max']) * 100 if ach['progress_max'] > 0 else 0
                    st.markdown(f"**Progress:** {progress}/{ach['progress_max']} ({progress_percent:.1f}%)")
                    st.progress(progress_percent / 100)
    
    with achievement_tabs[2]:
        st.markdown("### 📋 All Achievements")
        
        all_achievements = achievement_system.get_all_achievements()
        for ach in all_achievements:
            status = "✅ " if ach['unlocked'] else "⏳ "
            with st.expander(f"{status}{ach['icon']} {ach['name']} (+{ach['points']} pts)"):
                st.markdown(f"**Description:** {ach['description']}")
                st.markdown(f"**Category:** {achievements.CATEGORIES[ach['category']]}")
                st.markdown(f"**Status:** {'Unlocked' if ach['unlocked'] else 'Locked'}")
                
                # Show progress bar
                progress = min(ach['progress'], ach['progress_max'])
                progress_percent = (progress / ach['progress_max']) * 100 if ach['progress_max'] > 0 else 0
                st.markdown(f"**Progress:** {progress}/{ach['progress_max']} ({progress_percent:.1f}%)")
                st.progress(progress_percent / 100)
    
    with achievement_tabs[3]:
        st.markdown("### 📊 Achievements by Category")
        
        # Create expander for each category
        for category, display_name in achievements.CATEGORIES.items():
            category_achievements = achievement_system.get_achievements_by_category(category)
            unlocked_count = sum(1 for a in category_achievements if a['unlocked'])
            
            with st.expander(f"{display_name} ({unlocked_count}/{len(category_achievements)})"):
                for ach in category_achievements:
                    status = "✅ " if ach['unlocked'] else "⏳ "
                    st.markdown(f"{status} **{ach['icon']} {ach['name']}** - {ach['description']} (+{ach['points']} pts)")
                    
                    # Show progress bar for locked achievements
                    if not ach['unlocked']:
                        progress = min(ach['progress'], ach['progress_max'])
                        progress_percent = (progress / ach['progress_max']) * 100 if ach['progress_max'] > 0 else 0
                        st.progress(progress_percent / 100)
                        st.caption(f"{progress}/{ach['progress_max']} ({progress_percent:.1f}%)")
                    
                    st.markdown("---")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <h4>Dx3n Text Humanizer | Created by Huzaifah Tahir</h4>
    <p>Make AI-generated text appear naturally human-written in seconds</p>
    <p style="color: #888; font-size: 0.8em;">© 2025 Dx3n Text Humanizer - All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
