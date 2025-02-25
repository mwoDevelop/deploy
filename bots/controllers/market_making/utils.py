# Metody integracji

# # Update processed data
# from .utils import ai_signals
# self.processed_data["signal"] = ai_signals(trading_pair=self.config.trading_pair)
# self.processed_data["features"] = df

# # Update processed data
# from .utils import combine_signals
# self.processed_data["signal"] = combine_signals(df["signal"].iloc[-1], self.config.trading_pair)
# self.processed_data["features"] = df

# Update processed data
# from .utils import ai_signals
# trade_type = ai_signals(trading_pair=self.config.trading_pair)

@staticmethod
def ai_signals(trading_pair: str) -> int:
    external_sig = external_signal(trading_pair).strip().lower()
    print(f"External signal is {external_sig}")
    if external_sig == "buy":
        return 1
    if external_sig == "sell":
        return -1
    return 0

@staticmethod
def combine_signals(original: int, trading_pair: str) -> int:
    external_sig = external_signal(trading_pair).strip().lower()
    print(f"External signal is {external_sig} and original is {original}")
    if external_sig == "buy" and original == 1:
        return 1
    if external_sig == "sell" and original == -1:
        return -1
    if external_sig == "ignore":
        return original
    return 0

@staticmethod
def external_signal(trading_pair: str) -> int:
    import time
    signal = 0
    signal_file = f"{trading_pair.replace('-', '')}_signal.txt"
    file_path = "/home/hummingbot/data/" + signal_file
    print(f"Reading signal from {file_path}")
    with open(file_path, "r") as f:
        try:
            signal = f.read()
        finally:
            time.sleep(1)
        return signal
