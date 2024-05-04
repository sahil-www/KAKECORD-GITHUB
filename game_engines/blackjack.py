from typing_extensions import ParamSpecArgs
from settings import *

import discord
import asyncio
from data import cards

class BotBlackjack:
    name = "Blackjack"
    icon = I_BJ
    def __init__(self, bot, ctx, player, bet, currency):
        self.bot = bot
        self.ctx = ctx
        self.player = player
        self.bet = bet
        self.currency = currency
        self.channel = ctx.channel

    async def start_game(self):
        # Initialising variables
        self.deck_in_use = cards.Deck()        # Deck() has an attribute .deck that has all of the cards stored as a list
        player_stand = False
        # Distributing the cards
        player_hand = self.deck_in_use.distribute(2)
        dealer_hand = self.deck_in_use.distribute(2)
        
        player_value, player_string, player_bust = self.value_calculator(player_hand)
        dealer_value, dealer_string, dealer_bust = self.value_calculator([dealer_hand[0]])        # Making the item of dealer_hand a list because value_calculator takes a list

        # Here starts the loop
        while (player_bust == False and player_stand == False):
            embed = discord.Embed(
                description = "**Respond with:**\n`h/hit` to take another card\n`s/stand` to stand\n`d/double down` to double your bet, hit once then stand",
                colour = 0xFF0000
            )
            embed.set_author(name=self.player, icon_url=self.player.avatar_url)

            embed.add_field(name=f"Your hand [`{player_string}`]", value=self.hand_string_maker(player_hand), inline=False)
            embed.add_field(name=f"My hand [`{dealer_string}` + ?]", value=dealer_hand[0].emoji + dealer_hand[0].rank + ", ?", inline=False)
            embed.set_footer(text="Use `<prefix>instructions blackjack for instructions.")
            await self.ctx.send(embed=embed)

            # Here the player performs the actions
            def check(message):
                return (
                    message.channel == self.channel and
                    message.author == self.player and
                    message.content.lower() in ["h", "hit", "s", "stand", "dd", "doubledown", "double down"]
                )
            try:
                msg = await self.bot.wait_for("message", timeout=45, check=check)
                msg_cont = msg.content.lower()
                
                # For stand
                if msg_cont in ["s", "stand"]:
                    player_stand = True
                
                else:
                    # For hit
                    new_cards = self.deck_in_use.distribute(1)
                    player_hand += new_cards
                    player_value, player_string, player_bust = self.value_calculator(player_hand)

                    # For double down
                    if msg_cont in ["dd", "doubledown", "double down"]:
                        player_stand = True
                        try:
                            await self.bot.db.subtract_balance(self.player.id, self.bet, self.currency.name)
                            self.bet += self.bet
                        
                        except Exception:
                            await self.ctx.send("You don't have enough chips to double down, so you stand after hitting once, without doubling down!")
                            await asyncio.sleep(1)
            
            # A timeout error ofcourse
            except Exception as e:
                print(e)
                await self.ctx.send("Because you didn't give a correct response on time, you stand!")
                await asyncio.sleep(1)
                player_stand = True

        # After the loop breaks, comes the turn of dealer, only if player_bust == False
        if player_bust:
            # Player loses
            # The dealer doesn't have to move, player loses instantly and the second card of dealer is revealed
            dealer_value, dealer_string, dealer_bust = self.value_calculator(dealer_hand)
            embed = discord.Embed(
                colour = 0xFF0000
            )
            embed.set_author(name=self.player, icon_url=self.player.avatar_url)
            embed.add_field(name=f"Your hand [`{player_string}`]", value=self.hand_string_maker(player_hand), inline=False)
            embed.add_field(name=f"My hand [`{dealer_string}`]", value=self.hand_string_maker(dealer_hand), inline=False)
            embed.add_field(name="You lose!", value=f"You bust!\nI win {self.bet}{self.currency.emoji}!")
            await self.ctx.send(embed=embed)
        
        # When the player stood and bust is false
        else:
            # The dealer takes its chances
            dealer_value, dealer_string, dealer_bust = self.value_calculator(dealer_hand)

            while dealer_value < 17:
                new_cards = self.deck_in_use.distribute(1)
                dealer_hand += new_cards
                dealer_value, dealer_string, dealer_bust = self.value_calculator(dealer_hand)

            if dealer_bust == True:
                # Player wins
                await self.bot.db.add_balance(self.player.id, self.bet * 2, self.currency.name)
                embed = discord.Embed(
                colour = 0xFF0000
                )
                embed.set_author(name=self.player, icon_url=self.player.avatar_url)
                embed.add_field(name=f"Your hand [`{player_string}`]", value=self.hand_string_maker(player_hand), inline=False)
                embed.add_field(name=f"My hand [`{dealer_string}`]", value=self.hand_string_maker(dealer_hand), inline=False)
                embed.add_field(name="You win!", value=f"I bust!\nYou win {self.bet}{self.currency.emoji}!")
                await self.ctx.send(embed=embed)
            
            else:
                # Player loses
                if dealer_value > player_value:
                    embed = discord.Embed(
                    colour = 0xFF0000
                    )
                    embed.set_author(name=self.player, icon_url=self.player.avatar_url)
                    embed.add_field(name=f"Your hand [`{player_string}`]", value=self.hand_string_maker(player_hand), inline=False)
                    embed.add_field(name=f"My hand [`{dealer_string}`]", value=self.hand_string_maker(dealer_hand), inline=False)
                    embed.add_field(name="You lose!", value=f"You have __{player_value}__ and I have __{dealer_value}__!\nI win {self.bet}{self.currency.emoji}!")
                    await self.ctx.send(embed=embed)

                elif player_value > dealer_value:
                    # Player wins
                    await self.bot.db.add_balance(self.player.id, self.bet * 2, self.currency.name)
                    embed = discord.Embed(
                    colour = 0xFF0000
                    )
                    embed.set_author(name=self.player, icon_url=self.player.avatar_url)
                    embed.add_field(name=f"Your hand [`{player_string}`]", value=self.hand_string_maker(player_hand), inline=False)
                    embed.add_field(name=f"My hand [`{dealer_string}`]", value=self.hand_string_maker(dealer_hand), inline=False)
                    embed.add_field(name="You win!", value=f"You have __{player_value}__ and I have __{dealer_value}__\nYou win {self.bet}{self.currency.emoji}!")
                    await self.ctx.send(embed=embed)

                # player_value == dealer_value
                else:
                    # Draws
                    await self.bot.db.add_balance(self.player.id, self.bet, self.currency.name)
                    embed = discord.Embed(
                    colour = 0xFF0000
                    )
                    embed.set_author(name=self.player, icon_url=self.player.avatar_url)
                    embed.add_field(name=f"Your hand [`{player_string}`]", value=self.hand_string_maker(player_hand), inline=False)
                    embed.add_field(name=f"My hand [`{dealer_string}`]", value=self.hand_string_maker(dealer_hand), inline=False)
                    embed.add_field(name="Draw!", value=f"We both have __{player_value}__\nYour {self.bet}{self.currency.emoji} have been returned!")
                    await self.ctx.send(embed=embed)


    # Will return the value of the hand and also the string that represent the value (Soft 11, 11 etc.)
    def value_calculator(self, hand):
        soft  = False
        value = 0        # The value of the whole hand
        # For every card in hand (a list)
        for card in hand:
            index = card.index

            # If the card index is not one of these, the value of that card is simply its index
            if index not in [1, 11, 12, 13]:
                value += index
            
            # If the card value is one of these, the value of that card is 10
            elif index in [11, 12, 13]:
                value += 10

            # That card is an ace
            else:

                # If the Ace keeps the sum less than 21, the ace will be counted as 11 and soft will be set to True
                if value + 11 <= 21:
                    value += 11
                    soft = True
                
                # The Ace will be counted as 1
                else:
                    value += 1
        
        # At the end of the loop if the hand exceeds 21, if the soft is True, it will reduce 10 from the value (making the ace 1)
        if value > 21 and soft:
            value -= 10
            soft = False

        # If the value is still > 21
        if value > 21:
            bust = True
        else:
            bust = False
        
        # This is the part where the string that shows the value of the hand is generated
        string = ""
        if soft:
            string += "Soft "

        string += str(value)
        return value, string, bust


    ## Will return the player cards in str(), i.e. with emoji and number format that is displayed as the embed content of the hand (in future, I plan on changing it to real card emojis)
    def hand_string_maker(self, hand):
        string = ""
        for i in hand:
            string += i.emoji + i.rank + ", "
        
        string = string.strip(", ")         # Strips the extra ", " in the end
        return string