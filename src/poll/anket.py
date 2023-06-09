class Anket:
    def __init__(self, config):
        self.config = config
        self.length = len(config)
        self.answers = None
        self.scores = 0
        
    def add_answers(self, answers: list):
        self.scores = 0
        self.answers = answers
        self._counter()
        return self.scores
    
    def get_question(self,k):
      return self.config[k].get('text')
  
    def _counter(self):
        for i in range(self.length):
            qtype = self.config[i].get('qtype') or self.config[i].get('type')
            qoptions =  self.config[i].get('options')
            right_answer =  self.config[i].get('right_answer')
            qanswer = self.answers[i]
            if qtype == 'closed':
                self.scores += 1 if qanswer == 'Да' else + 0
            if qtype == 'multiple_choice':
                if qanswer == right_answer:
                    self.scores += 5
            if qtype == 'number':
                if int(qanswer) == right_answer:
                    self.scores += 1
                else:
                    self.scores -= 1
            # No scoring for open questions

        
    def get_final_text(self, score):
        if score > 10:
            return f'Спасибо за ответы, ты набрал: {score} баллов из 28 возможных, красавчик'
        elif 1 <= score <= 4:
            return f'Всего {score} балл{"а" if 2 <= score <= 4 else ""}??? Чел посмотри заново Шрека, не позорься'
        else:
            return f'Всего {score} баллов??? Чел посмотри заново Шрека, не позорься'
