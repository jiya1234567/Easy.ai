class CognitiveCore:
    def __init__(self):
        self.state = "Neutral"
        
    def evaluate_valence(self, api_key_present):
        if not api_key_present:
            self.state = "Uneasy"
        else:
            self.state = "Convinced"
        return self.state
