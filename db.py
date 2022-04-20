import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    #USERS

    def check_user(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, username):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (user_id, username) VALUES (?, ?)", (user_id, username,))

    def user_count(self):
        with self.connection:
            result = self.cursor.execute("SELECT user_id FROM `users`").fetchall()
            return len(result)

    def get_user_answer(self, user_id, question_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT question_{question_id} FROM `users` WHERE user_id = ?", (user_id,)).fetchall()
            return result[0][0]

    #QUESTIONS

    def get_question(self, question_id):
        with self.connection:
            result = self.cursor.execute("SELECT question FROM `questions` WHERE id = ?", (question_id,)).fetchall()
            return result[0][0]

    def get_answers(self, question_id):
        with self.connection:
            result = self.cursor.execute("SELECT answers FROM `questions` WHERE id = ?", (question_id,)).fetchall()
            return result[0][0]

    #ANSWERS

    def set_answer(self, user_id, question_id, answer):
        with self.connection:
            return self.cursor.execute(f"UPDATE `users` SET question_{question_id} = ? WHERE user_id = ?", (answer, user_id))

    def get_answer_count(self):
        with self.connection:
            result1 = self.cursor.execute("SELECT question_1 FROM `users`").fetchall()
            result2 = self.cursor.execute("SELECT question_2 FROM `users`").fetchall()
            result3 = self.cursor.execute("SELECT question_3 FROM `users`").fetchall()
            empty1 = self.cursor.execute("SELECT question_1 FROM `users` WHERE question_1 = ?", ('None',)).fetchall()
            empty2 = self.cursor.execute("SELECT question_2 FROM `users` WHERE question_2 = ?", ('None',)).fetchall()
            empty3 = self.cursor.execute("SELECT question_3 FROM `users` WHERE question_3 = ?", ('None',)).fetchall()
            result = len(result1) - len(empty1) + len(result2) - len(empty2) + len(result3) - len(empty3)
            return result

    def get_answer_count_1(self):
        with self.connection:
            result1 = self.cursor.execute("SELECT question_1 FROM `users`").fetchall()
            empty1 = self.cursor.execute("SELECT question_1 FROM `users` WHERE question_1 = ?", ('None',)).fetchall()
            result = len(result1) - len(empty1)
            return result

    def get_answer_count_2(self):
        with self.connection:
            result2 = self.cursor.execute("SELECT question_2 FROM `users`").fetchall()
            empty2 = self.cursor.execute("SELECT question_2 FROM `users` WHERE question_2 = ?", ('None',)).fetchall()
            result = len(result2) - len(empty2)
            return result

    def get_answer_count_3(self):
        with self.connection:
            result3 = self.cursor.execute("SELECT question_3 FROM `users`").fetchall()
            empty3 = self.cursor.execute("SELECT question_3 FROM `users` WHERE question_3 = ?", ('None',)).fetchall()
            result = len(result3) - len(empty3)
            return result

