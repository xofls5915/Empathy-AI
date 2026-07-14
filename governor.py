class SafetyGovernor:

    def mode(self, danger_score):
        if danger_score >= 7:
            return "SAFETY"
        return "NORMAL"

    def safety_message(self):
        return (
            "현재 위험도가 높게 감지되었습니다.\n"
            "혼자 감당하려 하지 말고 가까운 사람과 이야기해보세요."
        )