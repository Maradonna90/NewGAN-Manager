import toga


class Progressbar(toga.widgets.textinput.TextInput):

    def __init__(
        self,
        id=None,
        style=None,
        factory=None,
        initial=None,
        placeholder=None,
        readonly=False,
        on_change=None,
        on_gain_focus=None,
        on_lose_focus=None,
        validators=None,
        label=None
    ):
        super().__init__(id=id, style=style, factory=factory)

        self.on_change = on_change
        self.placeholder = placeholder
        self.readonly = readonly

        # Set the actual value after on_change, as it may trigger change events, etc.
        self.value = initial
        self.validators = validators
        self.on_lose_focus = on_lose_focus
        self.on_gain_focus = on_gain_focus

        self.label = label
        self.max_progress = 100
        self.progress = 0
        self.step_size = 2
        self.sign = '█'
        self.label_sign = '...'
        self.running = False
        self.label_flavor = ''

    def start(self):
        self.running = True

    def stop(self):
        self.running = False
        self.reset()

    def update_progress(self, value):
        self.progress += value
        for i in range(value):
            if i % self.step_size == 0:
                self.value += self.sign

    def update_label(self, text):
        self.label.text = text
        self.label_flavor = text

    def animate_label(self):
        # eg. doing., doing.., doing..., doing. etc.
        while self.running:
            for char in self.label_sign:
                self.label.text = self.label_flavor + char

    def reset(self):
        self.label.text = ''
        self.label_flavor = ''
        self.progress = 0
        self.value = ''
