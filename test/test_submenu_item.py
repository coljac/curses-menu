from threading import Thread

from base_test_case import BaseTestCase
from cursesmenu import CursesMenu
from cursesmenu.items import SubmenuItem


class TestSubmenuItem(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.menu = CursesMenu("Test menu 1", "Subtitle 1")
        self.submenu1 = CursesMenu("Test submenu 1", "Subtitle 2")
        self.item1 = SubmenuItem("Item1", self.menu, self.submenu1)
        self.submenu1_thread = Thread(target=self.item1.action, daemon=True)
        self.submenu2 = CursesMenu("Test submenu 2", "Subtitle 3")
        self.item2 = SubmenuItem("Item2", self.menu, self.submenu2)
        self.submenu2_thread = Thread(target=self.item2.action, daemon=True)
        self.menu.append_item(self.item1)
        self.menu.append_item(self.item2)
        self.menu_thread = Thread(target=self.menu.show, daemon=True)
        self.menu_thread.start()

    def test_action(self):
        self.submenu1_thread.start()
        self.assertIs(CursesMenu.currently_active_menu, self.submenu1)
        CursesMenu.currently_active_menu.exit()
        self.submenu1_thread.join(timeout=10)
        self.assertIs(CursesMenu.currently_active_menu, self.menu)
        self.submenu2_thread.start()
        self.assertIs(CursesMenu.currently_active_menu, self.submenu2)
