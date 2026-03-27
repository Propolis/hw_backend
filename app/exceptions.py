class TaskNotFound(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id


class CommentNotFound(Exception):
    def __init__(self, comment_id: int):
        self.comment_id = comment_id
