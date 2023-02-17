from errbot import BotPlugin
import zulip
import os
import random
import requests


class Retromaster(BotPlugin):
    '''
      This bot will allow users to randomly pick the host of our biweekly retrospective meetings. 
    '''

    def activate(self):
        super(Retromaster, self).activate()

        #  send message every two weeks
        self.start_poller(1209600, self.send_message())

    def get_all_subscribers_from_stream(self, bot_handler, stream):
        return bot_handler.get_subscribers(stream=stream)['subscribers']

    def pick_random_user(self, all_users):
        return random.choice(all_users)

    def fetch_user_data(self, bot_handler, random_user):
        return bot_handler.get_user_by_id(random_user)['user']

    def generate_message(self, retromaster):
        return 'Our next retro master is @**{name}** 🎉. The expectations are super high!'.format(name=retromaster['full_name'])

    def send_message(self, stream, message):
        headers = dict()
        BOT_API_KEY = os.environ['BOT_RETROMASTER_KEY']
        params = {
            'api_key': BOT_API_KEY,
            'stream': stream,
            'topic': 'Retrospective'
        }
        
        response = requests.post("https://cern-rcs-sis.zulipchat.com/api/v1/retromaster",
                                 params=params,
                                 headers=headers,
                                 data=message)
        self.log.info(response.status_code)
        return "OK"


handler_class = Retromaster


bot_handler = zulip.Client(config_file="~/.zuliprc")
stream = 'test'
retromaster_bot = Retromaster()

all_users = retromaster_bot.get_all_subscribers_from_stream(
    bot_handler, stream)
random_user = retromaster_bot.pick_random_user(all_users)
retromaster = retromaster_bot.fetch_user_data(bot_handler, random_user)
message = retromaster_bot.generate_message(retromaster)

retromaster_bot.send_message(message)
