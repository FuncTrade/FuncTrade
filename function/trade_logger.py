from function.act import TradeLogger

import matplotlib.pyplot as plt
import numpy as np


from typing import Any


class SimplePyplotLogger(TradeLogger):
    def export(self) -> Any:
        fig, ax = plt.subplots()

        values = [dt.value for dt in self.data]
        dts = [dt.timestamp for dt in self.data]
        dts = np.array(dts, dtype='datetime64[ns]')

        dots = dict(zip(dts, values))

        ax.plot(dts, values, 'bo')

        sig_dts = [sig.timestamp for sig in self.signal]
        sig_values = [dots[dt] for dt in sig_dts]
        sig_dts = np.array(sig_dts, dtype='datetime64[ns]')

        for i in range(len(sig_dts)):
            action = self.signal[i].action
            x = sig_dts[i]
            y = sig_values[i]
            color = 'g' if action == 'buy' else 'r'
            ax.plot(x, y, color=color)
            ax.annotate(action, (x, y))

        plt.show()