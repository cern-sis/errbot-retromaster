import random

from errbot import BotPlugin, botcmd
import logging

class RetromasterPicker(BotPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = logging.getLogger(__name__)

    def activate(self):
        super().activate()

    def deactivate(self):
        super().deactivate()


    def pick_retromaster(self):
        stream_name = "tools & services"
        topic = "retrospective"
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
            "Pascal Egner"
        ]
        retromaster = random.choice(users)
        message = f"Our next retro master is @**{retromaster}** 🎉. The expectations are super high!"
        destination = self.build_identifier(f"#{{{{{stream_name}}}}}*{{{{{topic}}}}}")
        self.log.info(f"Sending message to: {destination}")
        try:
            self.send(destination, message)
            self.log.info("Message sent successfully.")
        except Exception as e:
            self.log.error(f"Failed to send message: {e}")

    @botcmd
    def pick_manual_retromaster(self, msg, args):
        """Manually pick a retromaster."""
        self.pick_retromaster()
