GREETING_MESSAGES = [
    'Hi! I came across your profile on Vetted and wanted to discuss potential opportunities.'
    ' Please let me know when you would be available to discuss.',
]


class MessageQueue:
    def __init__(self, messages):
        self.messages = messages
        self.index = 0

    def next_message(self):
        message = self.messages[self.index]
        self.index = (self.index + 1) % len(self.messages)
        return message


message_queue = MessageQueue(GREETING_MESSAGES)

if __name__ == '__main__':
    message_queue = MessageQueue(GREETING_MESSAGES)
    for _ in range(10):
        print(message_queue.next_message())


