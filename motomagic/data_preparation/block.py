# -*- coding  utf-8 -*-

class Block:
    """Class defines a N-second block of sensor values"""

    def __init__(self, device_id, start_time, size, filtered_ratio, data):
        """
        Parameters
        ----------
        device_id : str
            id of user's logging device (smartphone)
        start_time : str
            datetime of the beginning of the block in 'YYYY-MM-DD hh:mm:ss' format
        size : float
            length of the block in seconds
        filtered_ratio : float
            ratio of points of the block which are left after filtering
        data : pandas.Dataframe
            measurements data
        """
        self.device_id = device_id
        self.start_time = start_time
        self.size = size
        self.filtered_ratio=filtered_ratio
        self.data=data
        print("block created. Device id: {}, start_time; {}, size: {}, measurements: {}"
              .format(self.device_id, self.start_time, self.size, len(self.data)))
