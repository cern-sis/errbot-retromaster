import random

from errbot import BotPlugin, botcmd
from apscheduler.schedulers.background import BackgroundScheduler

TWO_WEEKS_IN_SECONDS = 60  # 1 Minute


class RetromasterPicker(BotPlugin):
    def activate(self):
        super().activate()
        self.start_periodic_task()

    def start_periodic_task(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.pick_retromaster, 'interval', seconds=TWO_WEEKS_IN_SECONDS)
        scheduler.start()

    def pick_retromaster(self):
        stream_name = "test"  # Replace with the name of the stream
        topic = "Retromaster"  # Replace with the topic
        users = [
            "Benjamin Bergia",
            "Ernesta Petraityte",
            "Harris Tzovanakis",
            "Karolina Siemieniuk-Morawska",
            "Marcjanna Jedrych",
            "Miguel Garcia Garcia",
            "Jimil Desai",
            "Pamfilos F",
            "Parth Shandilya",
        ]
        retromaster = random.choice(users)
        message = f"Our next retro master is **{retromaster}** 🎉. The expectations are super high!"
        destination = self.build_identifier(f"#{{{{{stream_name}}}}}*{{{{{topic}}}}}")
        self.send(destination, message)
        self.start_periodic_task()

    @botcmd
    def pick_manual_retromaster(self, msg, args):
        """Manually pick a retromaster."""
        self.pick_retromaster()
