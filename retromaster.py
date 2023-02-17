from errbot import BotPlugin
import zulip
import os
import random


class Retromaster(BotPlugin):
    '''
      This bot will allow users to randomly pick the host of our biweekly retrospective meetings. 
    '''

    bot_handler = zulip.Client(site="https://cern-rcs-sis.zulipchat.com",
                               email="retro-bot@cern-rcs-sis.zulipchat.com",
                               api_key=os.environ['BOT_ZULIP_KEY'])
    stream = 'test'

    def activate(self):
        super(Retromaster, self).activate()

        #  send message every two weeks
        self.start_poller(1209600, self.send_message)

    def deactivate(self):
        super(Retromaster, self).deactivate()

    def get_all_subscribers_from_stream(self, bot_handler, stream):
        return bot_handler.get_subscribers(stream=stream)['subscribers']

    def pick_random_user(self, bot_handler, stream):
        return random.choice(self.get_all_subscribers_from_stream(bot_handler, stream))

    def fetch_user_data(self, bot_handler, stream):
        return bot_handler.get_user_by_id(self.pick_random_user(bot_handler, stream))['user']

    def generate_message(self, bot_handler, stream):
        return 'Our next retro master is @**{name}** 🎉. The expectations are super high!'.format(name=self.fetch_user_data(bot_handler, stream)['full_name'])

    def send_message(self, bot_handler = bot_handler, stream = stream):
        request = dict(
            type='stream',
            to=stream,
            subject='Retrospective',
            content=self.generate_message(bot_handler, stream),
        )

        response = bot_handler.send_message(request)

        self.log.info(response.status_code)
        return "OK"


handler_class = Retromaster
