def keep_altitude_callback(self, attr, value):
    """
    保持无人机现有高度
    Args:
        self(Vehicle):
        attr:
        value:
    Returns:
    """
    current_altitude = self.location.global_relative_frame.alt
    
