from errbot import BotPlugin, botcmd
from apscheduler.schedulers.background import BackgroundScheduler
import random

class Retromaster(BotPlugin):
    '''
      This bot will allow users to randomly pick the host of our biweekly retrospective meetings. 
    '''

    def zulip(self):
        return self._bot.client

    def scheduler(self):
        scheduler = BackgroundScheduler()
        return scheduler

    def activate(self):
        super().activate()
        self.schedule_job()
        self.scheduler().start()

    def deactivate(self):
        super().deactivate()
        self.schedule_job().remove()

    def schedule_job(self):
        return self.scheduler().add_job(self.pick_retromaster, 'interval', days=14)

    def get_all_subscribers_from_stream(self, bot_handler, stream):
        return bot_handler.get_subscribers(stream=stream)['subscribers']

    def pick_random_user(self, bot_handler, stream):
        return random.choice(self.get_all_subscribers_from_stream(bot_handler, stream))

    def fetch_user_data(self, bot_handler, stream):
        return bot_handler.get_user_by_id(self.pick_random_user(bot_handler, stream))['user']

    def generate_message(self, bot_handler, stream):
        name = self.fetch_user_data(bot_handler, stream)['full_name']
        return f'Our next retro master is **{name}** 🎉. The expectations are super high!'

    @botcmd
    def pick_retromaster(self, msg, args):
        bot_handler = self.zulip()
        stream = 'test'

        request = dict(
            type='stream',
            to=stream,
            subject='Retrospective',
            content=self.generate_message(bot_handler, stream),
        )

        bot_handler.send_message(request)
