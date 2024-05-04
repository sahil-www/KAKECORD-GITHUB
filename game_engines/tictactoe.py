from settings import *
import discord
from itertools import cycle
import asyncio

class TicTacToe:
    name = "Tic Tac Toe"
    icon = I_TTT
    def __init__(self, bot, ctx, player1, player2, bet, currency):
        self.bot = bot
        self.ctx = ctx
        self.player1 = player1
        self.player2 = player2
        self.bet = bet
        self.currency = currency
        self.board = {"a" : E_A,"b" : E_B,"c" : E_C,"d" : E_D ,"e" : E_E,"f" : E_F,"g" : E_G,"h" : E_H,"i" : E_I}
        self.available_moves = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        self.players = {player1 : [E_X, I_X], player2 : [E_O, I_O]}
        self.player_turns = cycle(self.players.keys())
        self.channel = ctx.channel

    async def start_game(self):

        # Will go on until someone wins or there are no available moves or timeouts
        while bool(self.available_moves) and not (
            self.board["a"] == self.board["b"] == self.board["c"] or
            self.board["g"] == self.board["h"] == self.board["i"] or
            self.board["a"] == self.board["e"] == self.board["i"] or
            self.board["c"] == self.board["e"] == self.board["g"] or
            self.board["a"] == self.board["d"] == self.board["g"] or
            self.board["b"] == self.board["e"] == self.board["h"] or
            self.board["c"] == self.board["f"] == self.board["i"]
        ):
            
            # Sets the turn of the player
            self.current_turn = next(self.player_turns)
            embed = discord.Embed(
                title="Tic Tac Toe",
                description=f"{self.player1.mention} {E_VS} {self.player2.mention}",
                colour=0xFF0000
            )
            board_view=""
            for i, j in zip(self.board.keys(), range(1, 10)):
                if j % 3 != 0:
                    board_view += self.board[i] + " "
                elif j % 3 == 0:
                    board_view += f"{self.board[i]}\n"
            
            embed.add_field(name="Board", value=board_view)
            embed.add_field(name="Turn", value=self.current_turn.name)
            embed.set_footer(text="Use `<prefix>instructions tictactoe` for instructions.")
            await self.ctx.send(embed=embed)
            
            # The part where code accepts user input
            def check(message):
                return message.author == self.current_turn and message.content.lower() in self.available_moves and message.channel == self.channel
            
            try:
                message = await self.bot.wait_for("message", timeout=90, check=check)
                move = message.content.lower()
                self.available_moves.remove(move)
                self.board[move] = self.players[self.current_turn][0]

            except asyncio.TimeoutError:
                await self.ctx.send(f"{self.current_turn.mention}, you couldn't make a successful move on time, you've been removed from the game.")
                self.current_turn = next(self.player_turns)
                break
        
        # After the player wins, the board gets sent for one more time
        embed = discord.Embed(
                title="Tic Tac Toe Results",
                description=f"{self.player1.mention} {E_VS} {self.player2.mention}",
                colour=0xFF0000
            )
        board_view=""
        for i, j in zip(self.board.keys(), range(1, 10)):
            if j % 3 != 0:
                board_view += self.board[i] + " "
            elif j % 3 == 0:
                board_view += f"{self.board[i]}\n"

        # Adding the board to the embed
        embed.add_field(name="Board", value=board_view)
        # Checking the winner
        winner, symbol = await self.winner_check()

        if winner:
            result_string = f"**{winner.name}** wins!"
            # If there is bet
            if self.bet:
                await self.bot.db.add_balance(winner.id, self.bet * 2, self.currency.name)
                result_string = f"**{winner.name}** wins {self.bet}{self.currency.emoji}!"

        else:
            result_string = "It's a draw!"
            if self.bet:
                await self.bot.db.add_balance(self.player1.id, self.bet, self.currency.name)
                await self.bot.db.add_balance(self.player2.id, self.bet, self.currency.name)
                result_string += " Both of the players take back their bets."
            
        # The message is updated and sent
        embed.add_field(name="Result", value=result_string)
        embed.set_thumbnail(url=symbol)
        await self.ctx.send(embed=embed)

    # The method to find out the winner
    async def winner_check(self):
        # If loop stops while there are moves still available, the last player to move was obviously the winner
        if bool(self.available_moves):
            return self.current_turn, self.players[self.current_turn][1]
        # If loop stops and no moves are available, we will need to check if the last player actually scored
        else:
            # Checking if the last moving player actually scored
            if (
                self.board["a"] == self.board["b"] == self.board["c"] == self.players[self.current_turn] or
                self.board["g"] == self.board["h"] == self.board["i"] == self.players[self.current_turn] or
                self.board["a"] == self.board["e"] == self.board["i"] == self.players[self.current_turn] or
                self.board["c"] == self.board["e"] == self.board["g"] == self.players[self.current_turn] or
                self.board["a"] == self.board["d"] == self.board["g"] == self.players[self.current_turn] or
                self.board["b"] == self.board["e"] == self.board["h"] == self.players[self.current_turn] or
                self.board["c"] == self.board["f"] == self.board["i"] == self.players[self.current_turn]
            ):
                return self.current_turn, self.players[self.current_turn][1]
            
            # If the last player doesn't score, it's obviously a draw
            else:
                return None, I_TTT