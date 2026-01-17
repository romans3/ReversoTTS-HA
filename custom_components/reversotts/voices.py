"""voices.py for Reverso TTS integration."""

VOICES = {
    "Arabic": [
        "Leila22k_NT", "Nizar22k_NT", "Nizar22k_HQ",
        "Leila22k_HQ", "Mehdi22k_HQ", "Mehdi22k_NT",
        "Salma22k_HQ", "Salma22k_NT"
    ],
    "Catalan": ["Laia22k_HQ", "Laia22k_NT"],
    "Chinese": ["Lulu22k_NT", "Lulu22k_HQ"],
    "Czech": ["Eliska22k_NT", "Eliska22k_HQ"],
    "Danish": [
        "Mette22k_NT", "Rikke22k_NT", "Mette22k_HQ",
        "Rikke22k_HQ", "Rasmus22k_HQ", "Rasmus22k_NT"
    ],
    "Dutch": [
        "Daan22k_HQ", "Max22k_NT", "Daan22k_NT",
        "Femke22k_HQ", "Femke22k_NT", "Max22k_HQ",
        "Jasmijn22k_NT", "Jasmijn22k_HQ"
    ],
    "Dutch (Belgium)": [
        "Sofie22k_HQ", "Zoe22k_HQ", "Jeroen22k_HQ",
        "Jeroen22k_NT", "Zoe22k_NT", "Sofie22k_NT"
    ],
    "English": [
        "en-US-AndrewMultilingualNeural", "en-US-AvaMultilingualNeural",
        "Sharon22k_NT", "Tracy22k_HQ", "Darius22k_HQ",
        "Karen22k_HQ", "Karen22k_NT", "Will22k_HQ",
        "Ryan22k_NT", "Ryan22k_HQ", "Rod22k_NT",
        "Laura22k_HQ", "Micah22k_HQ", "Sharon22k_HQ",
        "Tracy22k_NT", "Micah22k_NT", "Rod22k_HQ",
        "Tamira22k_HQ", "Tamira22k_NT", "Sharona22k_HQ",
        "Darius22k_NT", "Will22k_NT", "Laura22k_NT"
    ],
    "English (Australian)": [
        "Tyler22k_NT", "Lisa22k_HQ", "Lisa22k_NT", "Tyler22k_HQ"
    ],
    "English (Canada)": ["Melany22k_NT", "Melany22k_HQ"],
    "English (United Kingdom)": [
        "Rhona22k_NT", "Rhona22k_HQ", "Peter22k_NT",
        "QueenElizabeth22k_HQ", "Rachel22k_NT",
        "Nizareng22k_NT", "Lucy22k_HQ", "Rachel22k_HQ",
        "Peter22k_HQ", "Graham22k_HQ", "Graham22k_NT",
        "Lucy22k_NT", "Queenelizabeth22k_NT"
    ],
    "Faroese": [
        "Hanus22k_NT", "Hanna22k_NT", "Hanna22k_HQ", "Hanus22k_HQ"
    ],
    "Finnish": ["Sanna22k_HQ", "Sanna22k_NT"],
    "French": [
        "fr-FR-HenriNeural", "fr-FR-DeniseNeural", "Margaux22k_NT",
        "Bruno22k_NT", "Anais22k_NT", "Claire22k_HQ",
        "Alice22k_NT", "Manon22k_HQ", "Margaux22k_HQ",
        "Manon22k_NT", "Julie22k_NT", "Alice22k_HQ",
        "Anais22k_HQ", "Antoine22k_HQ", "Antoine22k_NT",
        "Julie22k_HQ", "Claire22k_NT", "Bruno22k_HQ"
    ],
    "French (Belgium)": [
        "Margaux-BE22k_NT", "Bruno-BE22k_NT", "Anais-BE22k_NT",
        "Claire-BE22k_HQ", "Alice-BE22k_NT", "Manon-BE22k_HQ",
        "Margaux-BE22k_HQ", "Manon-BE22k_NT", "Julie-BE22k_NT",
        "Alice-BE22k_HQ", "Anais-BE22k_HQ", "Antoine-BE22k_HQ",
        "Antoine-BE22k_NT", "Julie-BE22k_HQ", "Claire-BE22k_NT",
        "Bruno-BE22k_HQ"
    ],
    "French (Canada)": [
        "Louise22k_HQ", "Louise22k_NT", "Melanie22k_HQ",
        "Anthony22k_NT", "Melanie22k_NT", "Anthony22k_HQ"
    ],
    "German": [
        "Claudia22k_HQ", "Andreas22k_NT", "Julia22k_NT",
        "Julia22k_HQ", "Sarah22k_NT", "Claudia22k_NT",
        "Klaus22k_HQ", "Andreas22k_HQ", "Klaus22k_NT",
        "Sarah22k_HQ"
    ],
    "Greek": ["Dimitris22k_HQ", "Dimitris22k_NT"],
    "Hebrew": ["he-IL-AvriNeural", "he-IL-HilaNeural"],
    "Hindi": ["Vidhi22k_NT", "Vidhi22k_HQ"],
    "Indian English": [
        "Deepa22k_HQ", "VidhiEnglish22k_NT", "Deepa22k_NT",
        "Vidhienglish22k_HQ"
    ],
    "Italian": [
        "Chiara22k_NT", "Vittorio22k_HQ", "Fabiana22k_NT",
        "Vittorio22k_NT", "Chiara22k_HQ", "Fabiana22k_HQ"
    ],
    "Japanese": ["Sakura22k_HQ", "Sakura22k_NT"],
    "Korean": ["Minji22k_NT", "Minji22k_HQ"],
    "Norwegian": [
        "Kari22k_NT", "Bente22k_NT", "Olav22k_HQ",
        "Bente22k_HQ", "Kari22k_HQ", "Olav22k_NT"
    ],
    "Polish": ["Ania22k_NT", "Piotr22k_NT", "Piotr22k_HQ", "Ania22k_HQ"],
    "Portuguese": ["Isabel22k_HQ", "Isabel22k_NT"],
    "Portuguese Brazilian": [
        "Marcia22k_HQ", "Sergio22k_HQ", "Sergio22k_NT", "Marcia22k_NT"
    ],
    "Romanian": ["ro-RO-EmilNeural", "ro-RO-AlinaNeural"],
    "Russian": ["Alyona22k_NT", "Alyona22k_HQ"],
    "Spanish": [
        "Ines22k_HQ", "Maria22k_NT", "Maria22k_HQ",
        "Antonio22k_NT", "Antonio22k_HQ", "Ines22k_NT"
    ],
    "Spanish (United States)": [
        "Rosa22k_HQ", "Rodrigo22k_HQ",
        "Rosa22k_NT", "Rodrigo22k_NT"
    ]
}
