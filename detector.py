class DangerDetector:

    def __init__(self):

        # 위험 키워드
        self.keyword_rules = {
            "죽고 싶": 5,
            "죽고싶": 5,
            "자살": 5,
            "사라지고 싶": 4,
            "끝내고 싶": 4,
            "방법": 3,
            "계획": 3,
            "힘들": 1,
            "지쳤": 1,
            "무기력": 1,
            "외롭": 2,
            "혼자": 2
        }

        # 감정 키워드
        self.emotion_rules = {
            "슬프": 1,
            "눈물": 1,
            "우울": 2,
            "공허": 2,
            "허무": 2,
            "불안": 1,
            "의미 없": 2,
            "절망": 3,
            "포기": 2
        }

        # 강조 표현
        self.intensity_rules = {
            "너무": 1,
            "정말": 1,
            "진짜": 1,
            "엄청": 1,
            "계속": 1,
            "매일": 1,
            "항상": 1
        }

    # --------------------------
    # Keyword Score
    # --------------------------
    def keyword_score(self, text):

        score = 0

        for word, weight in self.keyword_rules.items():

            if word in text:
                score += weight

        return score

    # --------------------------
    # Emotion Score
    # --------------------------
    def emotion_score(self, text):

        score = 0

        for word, weight in self.emotion_rules.items():

            if word in text:
                score += weight

        return score

    # --------------------------
    # Intensity Score
    # --------------------------
    def intensity_score(self, text):

        score = 0

        for word, weight in self.intensity_rules.items():

            if word in text:
                score += weight

        return score

    # --------------------------
    # Total
    # --------------------------
    def update(self, text):

        keyword = self.keyword_score(text)

        emotion = self.emotion_score(text)

        intensity = self.intensity_score(text)

        total = keyword + emotion + intensity

        total = min(total, 10)

        return {
            "total": total,
            "keyword": keyword,
            "emotion": emotion,
            "intensity": intensity
        }