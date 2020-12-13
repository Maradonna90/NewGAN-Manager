from dhooks import Webhook, Embed, File
from xmlparser import XML_Parser


class Reporter:
    def __init__(self, webhook_url, config_xml):
        self.xml_parser = XML_Parser()
        self.webhook = Webhook(webhook_url)
        self.xml = config_xml

    def send_report(self, id):
        embed = Embed(
            description='A user reported the following face',
            color=0x5CDBF0,
            timestamp='now'  # sets the timestamp to current time
            )
        img_file = self.xml_parser.get_imgpath_from_uid(self.xml, id)
        if img_file:
            img_file = self.xml.replace("config.xml", "") + img_file + ".png"
            file = File(img_file)
            embed.add_field(name='File', value=img_file)

            self.webhook.send(embed=embed, file=file)
        return img_file
