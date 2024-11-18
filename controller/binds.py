from enum import Enum

class AppBinds(Enum):
    SELECT_ALL = ("treeview", "<Control-a>", "select_all_items")
    CLICK_ON_ENABLE_COLUMN = ("treeview", "<Double-1>", "bind_treeview_enable")
    SHOW_CONTEXTUAL_MENU = ("treeview", "<Button-3>", "show_contextual_menu")
    PLAY_THIS_MUSIC = ("treeview", "<Return>", "play_this_music")
    
    DECREASE_VOLUME = ("root", "-", "update_volume", -0.1)
    INCREASE_VOLUME = ("root", "+", "update_volume", 0.1)

    @property
    def parent(self):
        return self.value[0]
    @property
    def control(self):
        return self.value[1]
    
    def command(self, controller):
        if len(self.value) > 3:
            return lambda event: getattr(controller, self.value[2])(event, self.value[3])
        else:
            return lambda event: getattr(controller, self.value[2])(event)