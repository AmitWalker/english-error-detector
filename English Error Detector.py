"""
English Sentence Error Detector
A professional application for finding mistakes in English sentences
Author: AmitWalker
Version: 1.0.0
"""

import re
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tkinter.font import Font
import threading
from collections import Counter
from datetime import datetime

class EnglishErrorDetector:
    """Main class for detecting errors in English sentences"""
    
    def __init__(self):
        # Common misspellings dictionary
        self.misspellings = {
            'accomodate': 'accommodate',
            'acknowlege': 'acknowledge',
            'agressive': 'aggressive',
            'alot': 'a lot',
            'appearence': 'appearance',
            'arguement': 'argument',
            'assasination': 'assassination',
            'basicly': 'basically',
            'belive': 'believe',
            'benifit': 'benefit',
            'bussiness': 'business',
            'calender': 'calendar',
            'cammunicate': 'communicate',
            'comittee': 'committee',
            'concious': 'conscious',
            'consious': 'conscious',
            'conveniant': 'convenient',
            'definately': 'definitely',
            'definatly': 'definitely',
            'dissappear': 'disappear',
            'embarass': 'embarrass',
            'enviornment': 'environment',
            'existance': 'existence',
            'experiance': 'experience',
            'goverment': 'government',
            'grammer': 'grammar',
            'grateful': 'greatful',
            'greatful': 'grateful',
            'happend': 'happened',
            'independant': 'independent',
            'indispensible': 'indispensable',
            'jewelery': 'jewelry',
            'judgement': 'judgment',
            'knowlege': 'knowledge',
            'laison': 'liaison',
            'maintanance': 'maintenance',
            'millenium': 'millennium',
            'minature': 'miniature',
            'mischievious': 'mischievous',
            'neccessary': 'necessary',
            'occassion': 'occasion',
            'occurence': 'occurrence',
            'occured': 'occurred',
            'omission': 'ommision',
            'ommision': 'omission',
            'percieve': 'perceive',
            'perserverance': 'perseverance',
            'phenomonon': 'phenomenon',
            'posession': 'possession',
            'potatoe': 'potato',
            'prefered': 'preferred',
            'priviledge': 'privilege',
            'pronounciation': 'pronunciation',
            'recieve': 'receive',
            'reccomend': 'recommend',
            'relevent': 'relevant',
            'remeber': 'remember',
            'seperate': 'separate',
            'sucess': 'success',
            'suprise': 'surprise',
            'tecnology': 'technology',
            'thier': 'their',
            'tommorow': 'tomorrow',
            'truely': 'truly',
            'untill': 'until',
            'weird': 'wierd',
            'wierd': 'weird',
            'writting': 'writing',
            'acheive': 'achieve',
            'apparant': 'apparent',
            'begining': 'beginning',
            'changeable': 'changable',
            'changable': 'changeable',
            'compatable': 'compatible',
            'confidant': 'confident',
            'consciencious': 'conscientious',
            'dilemna': 'dilemma',
            'drunkeness': 'drunkenness',
            'embarassed': 'embarrassed',
            'exhilirating': 'exhilarating',
            'foreward': 'forward',
            'guage': 'gauge',
            'harrass': 'harass',
            'imediately': 'immediately',
            'jewlery': 'jewelry',
            'judgemental': 'judgmental',
            'knew': 'new',
            'liscence': 'license',
            'managable': 'manageable',
            'medeval': 'medieval',
            'mispell': 'misspell',
            'neice': 'niece',
            'noticable': 'noticeable',
            'occured': 'occurred',
            'pendulum': 'pendulum',
            'persue': 'pursue',
            'posess': 'possess',
            'preceeding': 'preceding',
            'priviledge': 'privilege',
            'pronounciation': 'pronunciation',
            'prophacy': 'prophecy',
            'quarentine': 'quarantine',
            'relevent': 'relevant',
            'restaraunt': 'restaurant',
            'seige': 'siege',
            'sophmore': 'sophomore',
            'supersede': 'supersede',
            'tatoo': 'tattoo',
            'tendancy': 'tendency',
            'tolerance': 'tolarence',
            'tolarence': 'tolerance',
            'travelling': 'traveling',
            'unneccessary': 'unnecessary',
            'vaccum': 'vacuum',
            'villian': 'villain',
            'weather': 'whether',
            'whether': 'weather',
        }
        
        # Grammar patterns
        self.grammar_patterns = {
            'subject_verb_agreement': [
                (r'\b(I|You|We|They)\s+(\w+ed)\b', 'Check: Subject-verb agreement with "I/You/We/They" and past tense'),
                (r'\b(He|She|It)\s+(\w+ed)\b', 'Check: Subject-verb agreement with "He/She/It" and past tense'),
                (r'\b(He|She|It)\s+(\w+s)\b', 'Check: Subject-verb agreement - third person singular'),
            ],
            'double_negatives': [
                (r'\b(no|not|never|none)\s+\w+\s+(no|not|never|none)\b', 'Double negative detected'),
            ],
            'article_usage': [
                (r'\b(a|an)\s+(\w+)\s+(\w+)\b', 'Check: Article usage - possible missing article'),
                (r'\bthe\s+(\w+)\s+the\s+(\w+)\b', 'Check: Article usage - possible repetition'),
            ],
            'preposition_errors': [
                (r'\b(different\s+than)\b', 'Use "different from" instead of "different than"'),
                (r'\b(between\s+and)\s+(you|me|us|them)\b', 'Check: Between/among usage with pronouns'),
            ],
            'wordiness': [
                (r'\b(at\s+this\s+point\s+in\s+time)\b', 'Wordy phrase. Use "now" or "currently"'),
                (r'\b(due\s+to\s+the\s+fact\s+that)\b', 'Wordy phrase. Use "because"'),
                (r'\b(in\s+the\s+event\s+that)\b', 'Wordy phrase. Use "if"'),
                (r'\b(as\s+a\s+matter\s+of\s+fact)\b', 'Wordy phrase. Use "actually" or "in fact"'),
            ],
            'redundancy': [
                (r'\b(advance\s+planning)\b', 'Redundant: "advance planning" -> "planning"'),
                (r'\b(completely\s+finished)\b', 'Redundant: "completely finished" -> "finished"'),
                (r'\b(past\s+history)\b', 'Redundant: "past history" -> "history"'),
                (r'\b(true\s+facts)\b', 'Redundant: "true facts" -> "facts"'),
            ],
            'vague_pronouns': [
                (r'\b(it|this|that)\s+is\s+\w+\s+\w+\s+(it|this|that)\b', 'Vague pronoun reference - clarify what it refers to'),
            ],
            'parallel_structure': [
                (r'\b(and|or)\s+\w+ing\s+\w+\s+(and|or)\s+\w+ed\b', 'Check: Parallel structure - mixed verb forms'),
            ],
        }
        
        # Common confused words
        self.confused_words = {
            r'\b(their|there|they\'re)\b': 'Common confusion: their/there/they\'re',
            r'\b(your|you\'re)\b': 'Common confusion: your/you\'re',
            r'\b(its|it\'s)\b': 'Common confusion: its/it\'s',
            r'\b(to|too|two)\b': 'Common confusion: to/too/two',
            r'\b(affect|effect)\b': 'Common confusion: affect/effect',
            r'\b(than|then)\b': 'Common confusion: than/then',
            r'\b(who|whom)\b': 'Common confusion: who/whom',
            r'\b(which|that)\b': 'Common confusion: which/that',
            r'\b(less|fewer)\b': 'Common confusion: less/fewer',
            r'\b(among|between)\b': 'Common confusion: among/between',
            r'\b(lie|lay)\b': 'Common confusion: lie/lay',
            r'\b(accept|except)\b': 'Common confusion: accept/except',
            r'\b(advice|advise)\b': 'Common confusion: advice/advise',
            r'\b(beside|besides)\b': 'Common confusion: beside/besides',
            r'\b(complement|compliment)\b': 'Common confusion: complement/compliment',
            r'\b(emigrate|immigrate)\b': 'Common confusion: emigrate/immigrate',
            r'\b(hanged|hung)\b': 'Common confusion: hanged/hung',
            r'\b(historic|historical)\b': 'Common confusion: historic/historical',
            r'\b(imply|infer)\b': 'Common confusion: imply/infer',
            r'\b(lose|loose)\b': 'Common confusion: lose/loose',
        }
        
        # Informal words
        self.informal_words = {
            'gonna': 'going to',
            'wanna': 'want to',
            'gotta': 'have to',
            'kinda': 'kind of',
            'sorta': 'sort of',
            'ain\'t': 'isn\'t / aren\'t',
            'dunno': 'don\'t know',
            'yeah': 'yes',
            'yep': 'yes',
            'nope': 'no',
            'cuz': 'because',
            'cos': 'because',
            'thru': 'through',
            'tho': 'though',
            'u': 'you',
            'r': 'are',
            'ur': 'your / you\'re',
            'lol': 'laugh out loud (informal)',
            'omg': 'oh my God (informal)',
            'btw': 'by the way (informal)',
            'idk': 'I don\'t know',
            'smh': 'shaking my head (informal)',
        }
        
        # Punctuation patterns
        self.punctuation_patterns = [
            (r'\s+[,.:;?!]', 'Space before punctuation - remove space'),
            (r'[,.:;?!]\S', 'Missing space after punctuation'),
            (r'\.{2,}', 'Multiple periods - use single period or ellipsis (...)'),
            (r'[.!?]{2,}', 'Repeated punctuation - use single punctuation mark'),
            (r'\s\s+', 'Double spaces - use single space'),
            (r'\([^)]*\(', 'Nested parentheses - confusing structure'),
        ]
        
        self.errors = []
        
    def check_text(self, text):
        """Main method to check text for all types of errors"""
        self.errors = []
        
        if not text.strip():
            return self.errors
        
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        for sentence in sentences:
            if not sentence.strip():
                continue
            
            self.check_spelling(sentence)
            self.check_grammar(sentence)
            self.check_punctuation(sentence)
            self.check_informal_words(sentence)
            self.check_confused_words(sentence)
            self.check_capitalization(sentence)
            self.check_run_on_sentences(sentence)
        
        return self.errors
    
    def check_spelling(self, sentence):
        """Check for spelling errors"""
        words = re.findall(r'\b\w+\b', sentence)
        for word in words:
            word_lower = word.lower()
            if word_lower in self.misspellings:
                self.errors.append({
                    'type': 'Spelling',
                    'original': word,
                    'suggestion': self.misspellings[word_lower],
                    'context': sentence,
                    'position': sentence.find(word),
                    'severity': 'High'
                })
    
    def check_grammar(self, sentence):
        """Check for grammar errors"""
        for category, patterns in self.grammar_patterns.items():
            for pattern, message in patterns:
                matches = re.finditer(pattern, sentence, re.IGNORECASE)
                for match in matches:
                    self.errors.append({
                        'type': 'Grammar',
                        'original': match.group(0),
                        'suggestion': message,
                        'context': sentence,
                        'position': match.start(),
                        'severity': 'Medium'
                    })
    
    def check_punctuation(self, sentence):
        """Check for punctuation errors"""
        for pattern, message in self.punctuation_patterns:
            matches = re.finditer(pattern, sentence)
            for match in matches:
                self.errors.append({
                    'type': 'Punctuation',
                    'original': match.group(0),
                    'suggestion': message,
                    'context': sentence,
                    'position': match.start(),
                    'severity': 'Medium'
                })
    
    def check_informal_words(self, sentence):
        """Check for informal words"""
        words = re.findall(r'\b\w+\b', sentence)
        for word in words:
            word_lower = word.lower()
            if word_lower in self.informal_words:
                self.errors.append({
                    'type': 'Style',
                    'original': word,
                    'suggestion': f'Consider using "{self.informal_words[word_lower]}" (formal)',
                    'context': sentence,
                    'position': sentence.find(word),
                    'severity': 'Low'
                })
    
    def check_confused_words(self, sentence):
        """Check for commonly confused words"""
        for pattern, message in self.confused_words.items():
            matches = re.finditer(pattern, sentence, re.IGNORECASE)
            for match in matches:
                self.errors.append({
                    'type': 'Style',
                    'original': match.group(0),
                    'suggestion': message,
                    'context': sentence,
                    'position': match.start(),
                    'severity': 'Medium'
                })
    
    def check_capitalization(self, sentence):
        """Check for capitalization errors"""
        if sentence and sentence[0].islower():
            self.errors.append({
                'type': 'Capitalization',
                'original': sentence[:20] + '...' if len(sentence) > 20 else sentence,
                'suggestion': 'Start sentence with capital letter',
                'context': sentence,
                'position': 0,
                'severity': 'Low'
            })
    
    def check_run_on_sentences(self, sentence):
        """Check for run-on sentences"""
        if ',' in sentence:
            parts = sentence.split(',')
            if len(parts) > 2:
                for i in range(len(parts) - 1):
                    if re.search(r'\b\w+\s+\w+\b', parts[i]) and re.search(r'\b\w+\s+\w+\b', parts[i+1]):
                        if not re.search(r'\b(and|or|but|for|nor|yet|so)\b', parts[i]):
                            self.errors.append({
                                'type': 'Style',
                                'original': sentence,
                                'suggestion': 'Possible comma splice - use semicolon or conjunction',
                                'context': sentence,
                                'position': 0,
                                'severity': 'Medium'
                            })
                            break
    
    def get_statistics(self):
        """Get error statistics"""
        return {
            'total_errors': len(self.errors),
            'by_type': Counter(error['type'] for error in self.errors),
            'by_severity': Counter(error['severity'] for error in self.errors),
            'errors': self.errors
        }


class ErrorDetectorGUI:
    """GUI Application for the English Error Detector"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("English Error Detector Pro")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e1e')
        
        # Set dark theme colors
        self.bg_color = '#1e1e1e'
        self.text_bg = '#2d2d2d'
        self.text_fg = '#d4d4d4'
        self.accent_color = '#007acc'
        
        self.detector = EnglishErrorDetector()
        self.create_widgets()
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="🔍 English Error Detector Pro", 
            font=("Segoe UI", 18, "bold"),
            foreground=self.accent_color
        )
        title_label.pack(pady=10)
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Find and fix spelling, grammar, and style errors",
            font=("Segoe UI", 10)
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Input area
        input_label = ttk.Label(main_frame, text="📝 Enter your text below:", font=("Segoe UI", 10, "bold"))
        input_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.input_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=80,
            height=12,
            font=("Segoe UI", 11),
            bg=self.text_bg,
            fg=self.text_fg,
            insertbackground='white',
            relief=tk.FLAT,
            borderwidth=2
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Button styling
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'))
        
        check_button = ttk.Button(
            button_frame,
            text="🔍 Check Errors",
            command=self.check_text,
            style='Accent.TButton'
        )
        check_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = ttk.Button(
            button_frame,
            text="🗑️ Clear All",
            command=self.clear_all
        )
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        example_button = ttk.Button(
            button_frame,
            text="📝 Load Example",
            command=self.load_example
        )
        example_button.pack(side=tk.LEFT)
        
        # Statistics frame
        self.stats_frame = ttk.LabelFrame(main_frame, text="📊 Statistics", padding="10")
        self.stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_label = ttk.Label(
            self.stats_frame,
            text="No text checked yet",
            font=("Segoe UI", 10)
        )
        self.stats_label.pack()
        
        # Results area
        results_label = ttk.Label(main_frame, text="📋 Detected Errors:", font=("Segoe UI", 10, "bold"))
        results_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.results_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=80,
            height=12,
            font=("Consolas", 10),
            bg=self.text_bg,
            fg=self.text_fg,
            relief=tk.FLAT,
            borderwidth=2
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Configure tags for colored text
        self.results_text.tag_configure("high", foreground="#f48771")
        self.results_text.tag_configure("medium", foreground="#d4b96a")
        self.results_text.tag_configure("low", foreground="#6a9955")
        self.results_text.tag_configure("header", foreground="#007acc", font=("Consolas", 10, "bold"))
        
        # Status bar
        self.status_label = ttk.Label(
            main_frame,
            text="✅ Ready - Enter text and click 'Check Errors'",
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Segoe UI", 9)
        )
        self.status_label.pack(fill=tk.X, pady=(5, 0))
        
        # Keyboard shortcuts hint
        shortcut_label = ttk.Label(
            main_frame,
            text="💡 Tip: Press Ctrl+Enter to check errors",
            font=("Segoe UI", 8),
            foreground="gray"
        )
        shortcut_label.pack(pady=(2, 0))
    
    def check_text(self):
        """Execute the error checking"""
        text = self.input_text.get("1.0", tk.END)
        
        if not text.strip():
            messagebox.showwarning("Warning", "Please enter some text to check.")
            return
        
        self.results_text.delete("1.0", tk.END)
        self.status_label.config(text="⏳ Checking text... Please wait")
        self.root.update()
        
        # Run in a separate thread
        def check_thread():
            errors = self.detector.check_text(text)
            self.root.after(0, lambda: self.display_results(errors))
        
        threading.Thread(target=check_thread, daemon=True).start()
    
    def display_results(self, errors):
        """Display results in the GUI"""
        if not errors:
            self.results_text.insert("1.0", "✅ No errors found! Your text looks great!\n\n", "low")
            self.results_text.insert(tk.END, "✨ Perfect writing! Keep up the good work!", "header")
            self.stats_label.config(text="✅ No errors found - Perfect text!")
            self.status_label.config(text="✅ Check complete - No errors found")
            return
        
        # Show header
        self.results_text.insert("1.0", f"📊 Found {len(errors)} errors\n", "header")
        self.results_text.insert(tk.END, "=" * 60 + "\n\n")
        
        # Display each error
        for i, error in enumerate(errors, 1):
            severity = error['severity'].lower()
            
            msg = f"{i}. [{error['type']}] "
            msg += f"'{error['original']}' → {error['suggestion']}\n"
            msg += f"   📝 Context: \"{error['context'][:100]}{'...' if len(error['context']) > 100 else ''}\"\n"
            msg += f"   ⚠️ Severity: {error['severity']}\n\n"
            
            self.results_text.insert(tk.END, msg, severity)
        
        # Update statistics
        stats = self.detector.get_statistics()
        stats_text = f"📊 Total: {stats['total_errors']} errors"
        if stats['by_type']:
            stats_text += " | " + " | ".join([f"{k}: {v}" for k, v in stats['by_type'].items()])
        
        self.stats_label.config(text=stats_text)
        self.status_label.config(text=f"✅ Check complete - Found {len(errors)} errors")
    
    def clear_all(self):
        """Clear all text and results"""
        self.input_text.delete("1.0", tk.END)
        self.results_text.delete("1.0", tk.END)
        self.stats_label.config(text="Cleared")
        self.status_label.config(text="✅ Ready - Enter text and click 'Check Errors'")
    
    def load_example(self):
        """Load an example text with errors"""
        example = """This is a example sentence with varios errors. 
I have alot of things to say about this topic. 
The weather was to hot for me to handle.
Their going to the store to buy some groceries.
I cant beleive we made it to the end of the project.
The team needs to be more pro-active in there approach.
He don't know what to do with the extra time.
The principle reason for the delay was the weather.
Its important to check your work carefully.
We should of finished the project yesterday.
The data is insufficient to draw a conclusion at this point in time.
Between you and I, the presentation could have been better."""
        
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", example)
        self.status_label.config(text="📝 Example loaded - Click 'Check Errors' to analyze")
        
        # Auto-check
        self.check_text()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ErrorDetectorGUI(root)
    
    # Bind Ctrl+Enter to check
    root.bind('<Control-Return>', lambda e: app.check_text())
    
    root.mainloop()

if __name__ == "__main__":
    main()