class Question:
    def __init__(self, text, qtype: str, options):
        self.text = text  # contains the data
        self.qtype = qtype  # contains the reference to the next node
        self.options = options
        self.answer = None
        self.score = 0

    def add_answers(self, answer):
        self.answer = answer
        self._counter()

    def _counter(self):
        if self.qtype == 'closed':
            self.score = 1 if self.answer == 'Да' else 0
        if self.qtype == 'multiple_choice':
            pass
        if self.qtype == 'number':
            pass


class Node:
    def __init__(self):
        self.data = None  # contains the data
        self.next = None  # contains the reference to the next node


class LinkedList:
    def __init__(self):
        self.cur_node = None

    def add_node(self, data):
        new_node = Node()  # create a new node
        new_node.data = data
        new_node.next = self.cur_node  # link the new node to the 'previous' node.
        self.cur_node = new_node  # set the current node to the new one.

    def head(self):
        return self.cur_node


# from config import questions


def get_question_node(questions):
    qlist = LinkedList()
    for i in range(len(questions))[::-1]:
        qtext = questions[i].get('text')
        qtype = questions[i].get('qtype')
        qoptions = questions[i].get('options')
        question = Question(qtext, qtype, qoptions)
        qlist.add_node(question)
    return qlist.head()

def sum_linked_list(head):
  total = 0
  current = head
  while current != None:
        total += current.data.score
        current = current.next
  return total

# head = back = get_question_node(questions)
#
# back.data.add_answers('Да')
# back.next.data.add_answers('Да')
# back.next.next.data.add_answers('Да')
#
# print(head.data.score, head.data.text)
# print(head.next.data.score, head.next.data.text)
# print(head.next.next.data.score, head.next.next.data.text)
#
# print(sum_linked_list(head))
