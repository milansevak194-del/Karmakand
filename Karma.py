class KarmaAI:

    def process(self, text):
        text = text.lower()

        if "hello" in text:
            return "Pranam 🙏 How can I help you?"

        elif "money" in text:
            return "Lakshmi Puja is recommended for wealth."

        elif "marriage" in text:
            return "Gauri Shankar Puja helps in marriage."

        elif "health" in text:
            return "Mahamrityunjay Jaap is best for health."

        elif "vastu" in text:
            return "Vastu Shanti is recommended."

        else:
            return "Ask me about astrology, vastu or rituals." 