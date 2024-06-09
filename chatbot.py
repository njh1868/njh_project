import pandas as pd

class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers

    def find_best_answer(self, input_sentence):
        similarities = [calc_distance(input_sentence, question) for question in self.questions]
        best_match_index = similarities.index(min(similarities))  # 가장 거리가 작은 질문의 인덱스를 찾습니다.
        return self.answers[best_match_index]

def calc_distance(a, b):
    ''' 레벤슈타인 거리 계산하기 '''
    if a == b: return 0
    a_len = len(a)
    b_len = len(b)
    if a == "": return b_len
    if b == "": return a_len

    matrix = [[0] * (b_len + 1) for _ in range(a_len + 1)]

    for i in range(a_len + 1):
        matrix[i][0] = i
    for j in range(b_len + 1):
        matrix[0][j] = j

    for i in range(1, a_len + 1):
        for j in range(1, b_len + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            matrix[i][j] = min(matrix[i-1][j] + 1,  # 삽입
                               matrix[i][j-1] + 1,  # 삭제
                               matrix[i-1][j-1] + cost)  # 치환

    return matrix[a_len][b_len]

# CSV 파일 경로를 지정
filepath = 'ChatbotData.csv'

# 챗봇 인스턴스 생성
chatbot = SimpleChatBot(filepath)

# 챗봇과의 대화 반복
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)