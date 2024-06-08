import pandas as pd


class TicketToRideTrainAI:
    def __init__(self):
        self.data = []

    def log_state_action(self, state, action):
        self.data.append({**state, 'action': action})

    def save_data(self, file_path):
        df = pd.DataFrame(self.data)
        df.to_csv(file_path, index=False)

    def clear_data(self):
        self.data = []
