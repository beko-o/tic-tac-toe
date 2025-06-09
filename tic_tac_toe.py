#!/usr/bin/env python3
"""
Tic Tac Toe GUI Game
Графическая версия игры Крестики-Нолики с использованием tkinter
"""

import tkinter as tk
from tkinter import messagebox, font


class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Крестики-Нолики")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Игровые переменные
        self.current_player = 'X'
        self.board = ['' for _ in range(9)]
        self.buttons = []
        
        # Счетчик побед
        self.score_x = 0
        self.score_o = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        # Заголовок
        title_font = font.Font(family="Arial", size=20, weight="bold")
        title_label = tk.Label(
            self.root, 
            text="Крестики-Нолики", 
            font=title_font,
            fg="#2c3e50",
            pady=10
        )
        title_label.pack()
        
        # Информация о текущем игроке
        self.player_info = tk.Label(
            self.root,
            text=f"Ход игрока: {self.current_player}",
            font=("Arial", 14),
            fg="#e74c3c"
        )
        self.player_info.pack(pady=5)
        
        # Счетчик очков
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(pady=5)
        
        self.score_label = tk.Label(
            self.score_frame,
            text=f"X: {self.score_x}  |  O: {self.score_o}",
            font=("Arial", 12),
            fg="#34495e"
        )
        self.score_label.pack()
        
        # Игровое поле
        self.game_frame = tk.Frame(self.root, bg="#34495e", padx=10, pady=10)
        self.game_frame.pack(pady=20)
        
        # Создание кнопок для игрового поля
        button_font = font.Font(family="Arial", size=24, weight="bold")
        
        for i in range(9):
            row = i // 3
            col = i % 3
            
            button = tk.Button(
                self.game_frame,
                text="",
                font=button_font,
                width=4,
                height=2,
                bg="#ecf0f1",
                fg="#2c3e50",
                relief="raised",
                bd=3,
                command=lambda idx=i: self.make_move(idx)
            )
            button.grid(row=row, column=col, padx=2, pady=2)
            self.buttons.append(button)
        
        # Кнопки управления
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=20)
        
        # Кнопка новой игры
        new_game_btn = tk.Button(
            self.control_frame,
            text="Новая игра",
            font=("Arial", 12),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=5,
            command=self.new_game
        )
        new_game_btn.grid(row=0, column=0, padx=10)
        
        # Кнопка сброса счета
        reset_score_btn = tk.Button(
            self.control_frame,
            text="Сбросить счет",
            font=("Arial", 12),
            bg="#e67e22",
            fg="white",
            padx=20,
            pady=5,
            command=self.reset_score
        )
        reset_score_btn.grid(row=0, column=1, padx=10)
        
        # Кнопка выхода
        quit_btn = tk.Button(
            self.control_frame,
            text="Выход",
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=5,
            command=self.root.quit
        )
        quit_btn.grid(row=0, column=2, padx=10)
    
    def make_move(self, position):
        """Совершить ход"""
        if self.board[position] == '':
            # Делаем ход
            self.board[position] = self.current_player
            self.buttons[position].config(
                text=self.current_player,
                state="disabled",
                bg="#bdc3c7" if self.current_player == 'X' else "#f39c12",
                fg="white"
            )
            
            # Проверяем победу
            if self.check_winner():
                self.handle_win()
                return
            
            # Проверяем ничью
            if self.is_board_full():
                self.handle_tie()
                return
            
            # Переключаем игрока
            self.switch_player()
    
    def check_winner(self):
        """Проверка на победу"""
        # Выигрышные комбинации
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Горизонтали
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Вертикали
            [0, 4, 8], [2, 4, 6]              # Диагонали
        ]
        
        for pattern in win_patterns:
            if (self.board[pattern[0]] == self.board[pattern[1]] == 
                self.board[pattern[2]] != ''):
                # Подсвечиваем выигрышную комбинацию
                for pos in pattern:
                    self.buttons[pos].config(bg="#27ae60")
                return True
        return False
    
    def is_board_full(self):
        """Проверка на заполненность доски"""
        return '' not in self.board
    
    def switch_player(self):
        """Переключение игрока"""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        color = "#e74c3c" if self.current_player == 'X' else "#f39c12"
        self.player_info.config(
            text=f"Ход игрока: {self.current_player}",
            fg=color
        )
    
    def handle_win(self):
        """Обработка победы"""
        # Обновляем счет
        if self.current_player == 'X':
            self.score_x += 1
        else:
            self.score_o += 1
        
        self.update_score_display()
        
        # Отключаем все кнопки
        for button in self.buttons:
            button.config(state="disabled")
        
        # Показываем сообщение о победе
        messagebox.showinfo(
            "Победа!", 
            f"🎉 Игрок {self.current_player} победил! 🎉"
        )
        
        # Предлагаем новую игру
        if messagebox.askyesno("Новая игра", "Хотите сыграть еще раз?"):
            self.new_game()
    
    def handle_tie(self):
        """Обработка ничьей"""
        messagebox.showinfo("Ничья!", "🤝 Ничья! Хорошая игра! 🤝")
        
        if messagebox.askyesno("Новая игра", "Хотите сыграть еще раз?"):
            self.new_game()
    
    def new_game(self):
        """Начать новую игру"""
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        
        # Сбрасываем кнопки
        for button in self.buttons:
            button.config(
                text="",
                state="normal",
                bg="#ecf0f1",
                fg="#2c3e50"
            )
        
        # Обновляем информацию об игроке
        self.player_info.config(
            text=f"Ход игрока: {self.current_player}",
            fg="#e74c3c"
        )
    
    def reset_score(self):
        """Сброс счета"""
        if messagebox.askyesno("Сброс счета", "Вы уверены, что хотите сбросить счет?"):
            self.score_x = 0
            self.score_o = 0
            self.update_score_display()
    
    def update_score_display(self):
        """Обновление отображения счета"""
        self.score_label.config(text=f"X: {self.score_x}  |  O: {self.score_o}")
    
    def run(self):
        """Запуск игры"""
        self.root.mainloop()


def main():
    """Главная функция"""
    game = TicTacToeGUI()
    game.run()


if __name__ == "__main__":
    main()