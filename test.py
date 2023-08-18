from rubpy import Client, Message, handlers
from asyncio import run

# تعریف یک صفحه بازی خالی
board = [' '] * 9
joined = []

# تابع برای نمایش منو
def display_menu():
    return "به بازی دوز خوش آمدید!\n" \
           "برای شروع بازی، کلمه 'شروع' را ارسال کنید.\n" \
           "برای پیوستن به بازی، کلمه 'جوین' را ارسال کنید."

# تابع برای نمایش صفحه بازی
def display_board(board):
    rows = [f"{board[i]}   {board[i+1]}   {board[i+2]}" for i in range(0, 9, 3)]
    separator = "\n" + "═╬═╬═\n"
    return separator.join(rows)

# تابع برای بررسی برنده
def check_winner(board, player):
    win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for combo in win_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

async def main():
    async with Client(session="bot") as client:
        async def process_message(message: Message):
            global board, joined
            group = "g0ChCjw034fd201dbcad5d4c252603b3"
            if message.object_guid in group:
                if message.raw_text == "شروع":
                    joined = []
                    await message.reply(display_menu())
                elif message.raw_text == "جوین":
                    if len(joined) < 2:
                        result = await client.get_user_info(message.author_guid)
                        first_name = result.user.first_name
                        joined.append(message.author_guid)
                        await message.reply(f"کاربر [{first_name}]({message.author_guid}) با موفقیت به بازی دوز پیوست.")
                    else:
                        await message.reply("ظرفیت بازی تکمیل شده است. بازی قبلاً شروع شده یا تعداد بازیکنان به حداکثر رسیده است.")
                elif any([c.isdigit() for c in message.raw_text]):
                    if len(joined) < 2:
                        await message.reply("برای شروع بازی، لازم است حداقل دو بازیکن به بازی دوز ملحق شوند.")
                        return
                    move = int(next(c for c in message.raw_text if c.isdigit())) - 1
                    if not (0 <= move < 9) or board[move] != ' ':
                        await message.reply("جایگاه انتخاب شده معتبر نیست. لطفاً دوباره تلاش کنید.")
                        return
                    current_player = 'X' if board.count('X') <= board.count('O') else 'O'
                    if message.author_guid != joined[len(joined) - 1]:
                        await message.reply("نوبت شما نیست.")
                        return
                    board[move] = current_player
                    if check_winner(board, current_player):
                        winner = next((user_id for user_id in joined if user_id == message.author_guid), "بازیکن ناشناخته")
                        first_name = result.user.first_name if result else "کاربر ناشناخته"
                        await message.reply(display_board(board) + f"\nبازیکن [{first_name}]({winner}) برنده شد!")
                        board = [' '] * 9  # بازی را شروع مجدد می‌کنیم
                    elif ' ' not in board:
                        await message.reply(display_board(board) + "\nبازی مساوی شد!")
                        board = [' '] * 9  # بازی را شروع مجدد می‌کنیم
                        joined = []
                    else:
                        await message.reply(display_board(board))

        @client.on(handlers.MessageUpdates())
        async def updates(message: Message):
            await process_message(message)

        await client.run_until_disconnected()

run(main())
