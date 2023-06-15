from rouge import Rouge

# 예시 요약과 참조 요약
summary = "The cat sat on the mat"
reference = "The cat is on the mat"

# Rouge 객체 생성
rouge = Rouge()

# ROUGE-1 계산
scores = rouge.get_scores(summary, reference)
rouge_1_score = scores[0]['rouge-1']['f']

# ROUGE-2 계산
scores = rouge.get_scores(summary, reference)
rouge_2_score = scores[0]['rouge-2']['f']

# ROUGE-L 계산
scores = rouge.get_scores(summary, reference)
rouge_l_score = scores[0]['rouge-l']['f']

# 결과 출력
print("ROUGE-1 Score:", rouge_1_score)
print("ROUGE-2 Score:", rouge_2_score)
print("ROUGE-L Score:", rouge_l_score)
