import pathlib
from datetime import datetime
from gi.repository import Gtk
from datetime_popover import DateTimeButton
from recurrence_popover.recurrence_popover import RecurrenceButton


# Task Editor ##########################################################################################################
class TaskEditor:
    """
    This class contains the logic for the task editor dialog, which edits individual tasks.
    """
    def __init__(self, dialog_parent=None):

        # gtk builder setup
        glade_file_path = str((pathlib.Path(__file__).parent / 'task_editor.glade').resolve())
        builder = Gtk.Builder()
        builder.add_from_file(glade_file_path)
        builder.connect_signals(self)

        # Widget setup
        self._dialog = builder.get_object('task_editor_dialog')
        if dialog_parent:
            self._dialog.set_transient_for(dialog_parent)
        self._grid = builder.get_object('grid')
        self._title_entry = builder.get_object('title_entry')
        self._note_buffer = builder.get_object('note_buffer')
        self._notes_tag = builder.get_object('notes_tag')
        self.start_date_picker = DateTimeButton(
            date_format_string='Starts %B %d, %Y', datetime_format_string="Starts %B %d, %Y at %H:%M",
            no_date_string='No Start Date')
        self.start_date_picker.button.show()
        self._grid.attach(self.start_date_picker.button, 0, 2, 1, 1)
        self.due_date_picker = DateTimeButton(
            date_format_string='Due on %B %d, %Y', datetime_format_string="Due on %B %d, %Y at %H:%M",
            no_date_string='No Due Date')
        self.due_date_picker.button.show()
        self._grid.attach(self.due_date_picker.button, 1, 2, 1, 1)
        self._mark_done_button = builder.get_object('mark_done_button')
        self._mark_undone_button = builder.get_object('mark_undone_button')
        self._recurrence_picker = RecurrenceButton()
        self._recurrence_picker.button.show()
        self._grid.attach(self._recurrence_picker.button, 0, 3, 2, 1)
        self.__done_date = None
        self._delete_button = builder.get_object('delete_button')
        self._new_subtask_button = builder.get_object('new_subtask_button')

    # Handlers -------------------------------------------------------------------------------------------------
    def _on_mark_done_button_clicked(self, *_):
        self.__done_date = datetime.now()
        self._update_mark_done_buttons()

    def _on_mark_undone_button_clicked(self, *_):
        self.__done_date = None
        self._update_mark_done_buttons()

    # Updating Methods -------------------------------------------------------------------------------------------------
    def _update_mark_done_buttons(self):
        self._mark_done_button.set_visible(not bool(self.__done_date))
        self._mark_undone_button.set_visible(bool(self.__done_date))

    # Dialog Management ------------------------------------------------------------------------------------------------
    def open_dialog(self):
        self._dialog.show()

    def close_dialog(self):
        self._dialog.destroy()

    # Changed signal connector -----------------------------------------------------------------------------------------
    def connect_task_changed(self, function):
        self._title_entry.connect('changed', function)
        self._note_buffer.connect('changed', function)
        self.start_date_picker.picker.connect_datetime_changed_signal(function)
        self.due_date_picker.picker.connect_datetime_changed_signal(function)
        self._mark_done_button.connect('clicked', function)
        self._mark_undone_button.connect('clicked', function)
        self._recurrence_picker.popover.connect_recurrence_changed_signal(function)

    def connect_delete_button_signal(self, function):
        self._delete_button.connect('clicked', function)

    def connect_new_subtask_button_signal(self, function):
        self._new_subtask_button.connect('clicked', function)

    # Saving methods ---------------------------------------------------------------------------------------------------
    @property
    def title(self):
        return self._title_entry.get_text()

    @title.setter
    def title(self, title):
        self._title_entry.set_text(title)

    @property
    def notes(self):
        start_iter = self._note_buffer.get_start_iter()
        end_iter = self._note_buffer.get_end_iter()
        return self._note_buffer.get_text(start_iter, end_iter, True)

    @notes.setter
    def notes(self, notes):
        self._note_buffer.set_text(notes)

    @property
    def start_date(self):
        return self.start_date_picker.picker.datetime

    @start_date.setter
    def start_date(self, start_date):
        self.start_date_picker.picker.datetime = start_date

    @property
    def due_date(self):
        return self.due_date_picker.picker.datetime

    @due_date.setter
    def due_date(self, due_date):
        self.due_date_picker.datetime = due_date

    @property
    def done_date(self):
        return self.__done_date

    @done_date.setter
    def done_date(self, done_date):
        self.__done_date = done_date
        self._update_mark_done_buttons()

    @property
    def recurrence(self):
        return self._recurrence_picker.popover.recurrence_object

    @recurrence.setter
    def recurrence(self, recurrence):
        self._recurrence_picker.recurrence_object = recurrence
