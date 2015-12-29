from base_test_case import BaseTestCase, ThreadedReturnGetter
from cursesmenu import SelectionMenu
from threading import Thread
from cursesmenu import CursesMenu


class TestSelectionMenu(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_select(self):
        selection_menu = SelectionMenu(strings=["a", "b", "c"], title="Select a letter")

        menu_thread = Thread(target=selection_menu.show, daemon=True)
        menu_thread.start()
        selection_menu.go_down()
        selection_menu.select()
        menu_thread.join(timeout=5)
        self.assertEqual(selection_menu.selected_option, 1)

    def test_get_selection(self):
        self.menu_thread = ThreadedReturnGetter(SelectionMenu.get_selection, ["One", "Two", "Three"])
        self.menu_thread.start()
        CursesMenu.currently_active_menu.go_down()
        CursesMenu.currently_active_menu.select()
        self.menu_thread.join(timeout=5)
        self.assertEqual(self.menu_thread.return_value, 1)
