#!/usr/bin/env python3
import pathlib
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from datetime_popover import DateTimeButton
from task_recurrence import Recurrence


class RecurrencePopover:
    """
    This class handles the logic for the recurrence editor popover
    """
    def __init__(self, set_relative_to=None):
        # gtk builder preparation
        glade_file_path = str((pathlib.Path(__file__).parent / "recurrence_popover.glade").resolve())
        builder = Gtk.Builder()
        builder.add_from_file(glade_file_path)
        builder.connect_signals(self)
        # widget fetching
        self._popover = builder.get_object('popover')
        self._enabled_toggle = builder.get_object('enabled_toggle')
        self._increment_spinbutton = builder.get_object('increment_spinbutton')
        self._interval_menu = builder.get_object('interval_menu')
        self._weekdays_label = builder.get_object('weekdays_label')
        self._weekdays_box = builder.get_object('weekdays_box')
        self._weekday_sunday_toggle = builder.get_object('sunday_togglebutton')
        self._weekday_monday_toggle = builder.get_object('monday_togglebutton')
        self._weekday_tuesday_toggle = builder.get_object('tuesday_togglebutton')
        self._weekday_wednesday_toggle = builder.get_object('wednesday_togglebutton')
        self._weekday_thursday_toggle = builder.get_object('thursday_togglebutton')
        self._weekday_friday_toggle = builder.get_object('friday_togglebutton')
        self._weekday_saturday_toggle = builder.get_object('saturday_togglebutton')
        self._day_of_month_label = builder.get_object('day_of_month_label')
        self._day_of_month_box = builder.get_object('day_of_month_box')
        self._day_of_month_inner_box = builder.get_object('day_of_month_inner_box')
        self._day_of_month_set_button = builder.get_object('day_of_month_set_button')
        self._day_of_month_position_menu = builder.get_object('day_of_month_position_menu')
        self._day_of_month_menu = builder.get_object('day_of_month_menu')
        self._day_of_month_clear_button = builder.get_object('day_of_month_clear_button')
        self._stop_type_box = builder.get_object('stop_type_box')
        self._stop_type_menu = builder.get_object('stop_type_menu')
        self._stop_number_spinbox = builder.get_object('stop_number_spinbox')
        self._stop_date_picker = DateTimeButton()
        self._stop_date_picker.button.set_visible(False)
        self._stop_type_box.pack_start(self._stop_date_picker.button, True, True, 0)
        # setting relative widget
        if set_relative_to:
            self.set_relative_to(set_relative_to)

    # element updaters -------------------------------------------------------------------------------------------------
    def _on_enabled_toggle_state_set(self, *_):
        self.update_enabled()

    def _on_increment_spinbutton_value_changed(self, *_):
        self.update_increment()

    def _on_interval_menu_changed(self, *_):
        self.update_interval()

    def _on_day_of_month_set_button_clicked(self, *_):
        self._update_day_of_month(True)

    def _on_day_of_month_clear_button_clicked(self, *_):
        self._update_day_of_month(False)

    def _on_stop_type_menu_changed(self, *_):
        self.update_stop_info()

    # Element update methods -------------------------------------------------------------------------------------------
    def update_enabled(self):
        for element in [
                self._increment_spinbutton, self._interval_menu, self._weekdays_box, self._day_of_month_box,
                self._stop_type_box]:
            element.set_sensitive(self.enabled)

    def update_increment(self):
        active_value = self._interval_menu.get_active_id()
        self._interval_menu.remove_all()
        for interval in ['Minute', 'Hour', 'Day', 'Week', 'Month', 'Year']:
            interval_string = f'{interval}s' if self._increment_spinbutton.get_value_as_int() > 1 else interval
            self._interval_menu.append(interval.lower(), interval_string)
        self._interval_menu.set_active_id(active_value)

    def update_interval(self):
        for weekday_widget in [self._weekdays_box, self._weekdays_label]:
            weekday_widget.set_visible(True if self._interval_menu.get_active_id() == 'week' else False)

        for day_of_month_widget in [self._day_of_month_label, self._day_of_month_box]:
            day_of_month_widget.set_visible(True if self._interval_menu.get_active_id() == 'month' else False)

    def _update_day_of_month(self, is_enabled):
        self._day_of_month_inner_box.set_visible(True if is_enabled else False)
        self._day_of_month_set_button.set_visible(False if is_enabled else True)

    def update_stop_info(self):
        self._stop_number_spinbox.set_visible(True if self._stop_type_menu.get_active_id() == 'number' else False)
        self._stop_date_picker.button.set_visible(True if self._stop_type_menu.get_active_id() == 'date' else False)

    # popover methods --------------------------------------------------------------------------------------------------
    def set_relative_to(self, widget):
        self._popover.set_relative_to(widget)

    def raise_popover(self):
        """This raises the popup"""
        self._popover.popup()

    def connect_popover_closed_signals(self, function, *args):
        """This connects the given function to the signal specified"""
        self._popover.connect('closed', function, *args)

    def connect_recurrence_changed_signal(self, function, *args):
        self._enabled_toggle.connect('state-set', function, *args)
        self._increment_spinbutton.connect('value-changed', function, *args)
        self._interval_menu.connect('changed', function, *args)
        self._weekday_sunday_toggle.connect('toggled', function, *args)
        self._weekday_monday_toggle.connect('toggled', function, *args)
        self._weekday_tuesday_toggle.connect('toggled', function, *args)
        self._weekday_wednesday_toggle.connect('toggled', function, *args)
        self._weekday_thursday_toggle.connect('toggled', function, *args)
        self._weekday_friday_toggle.connect('toggled', function, *args)
        self._weekday_saturday_toggle.connect('toggled', function, *args)
        self._day_of_month_set_button.connect('clicked', function, *args)
        self._day_of_month_menu.connect('changed', function, *args)
        self._day_of_month_position_menu.connect('changed', function, *args)
        self._day_of_month_clear_button.connect('clicked', function, *args)
        self._stop_type_menu.connect('changed', function, *args)
        self._stop_date_picker.picker.connect_datetime_changed_signal(function, *args)
        self._stop_number_spinbox.connect('value-changed', function, *args)

    # Recurrence Saving Methods ----------------------------------------------------------------------------------------
    @property
    def enabled(self):
        return self._enabled_toggle.get_active()

    @enabled.setter
    def enabled(self, enabled):
        self._enabled_toggle.set_active(enabled)
        self.update_enabled()

    @property
    def increment(self):
        return self._increment_spinbutton.get_value_as_int()

    @increment.setter
    def increment(self, increment):
        self._increment_spinbutton.set_value(increment)
        self.update_increment()

    @property
    def interval(self):
        return self._interval_menu.get_active_id()

    @interval.setter
    def interval(self, interval):
        self._interval_menu.set_active_id(interval)
        self.update_interval()

    @property
    def weekdays(self):
        return {
            'sunday': self._weekday_sunday_toggle.get_active(),
            'monday': self._weekday_monday_toggle.get_active(),
            'tuesday': self._weekday_tuesday_toggle.get_active(),
            'wednesday': self._weekday_wednesday_toggle.get_active(),
            'thursday': self._weekday_thursday_toggle.get_active(),
            'friday': self._weekday_friday_toggle.get_active(),
            'saturday': self._weekday_saturday_toggle.get_active()
        }

    @weekdays.setter
    def weekdays(self, weekdays_dict):
        self._weekday_sunday_toggle.set_active(weekdays_dict['sunday'])
        self._weekday_monday_toggle.set_active(weekdays_dict['monday'])
        self._weekday_tuesday_toggle.set_active(weekdays_dict['tuesday'])
        self._weekday_wednesday_toggle.set_active(weekdays_dict['wednesday'])
        self._weekday_thursday_toggle.set_active(weekdays_dict['thursday'])
        self._weekday_friday_toggle.set_active(weekdays_dict['friday'])
        self._weekday_saturday_toggle.set_active(weekdays_dict['saturday'])

    @property
    def weekday_of_month(self):
        day_of_month_enabled = self._day_of_month_inner_box.get_visible()
        ordinal = self._day_of_month_position_menu.get_active_id()
        weekday = self._day_of_month_menu.get_active_id()
        return {
            'ordinal': int(ordinal) if day_of_month_enabled else None,
            'weekday': int(weekday) if day_of_month_enabled else None
        }

    @weekday_of_month.setter
    def weekday_of_month(self, weekday_of_month_dict):
        if weekday_of_month_dict:
            self._day_of_month_position_menu.set_active_id(weekday_of_month_dict['ordinal'])
            self._day_of_month_menu.set_active_id(weekday_of_month_dict['weekday'])
            self._update_day_of_month(True)
        else:
            self._update_day_of_month(False)

    @property
    def stop_info(self):
        return {
            'type': self._stop_type_menu.get_active_id(),
            'number': self._stop_number_spinbox.get_value_as_int(),
            'date': self._stop_date_picker.picker.datetime
        }

    @stop_info.setter
    def stop_info(self, stop_info_dict):
        self._stop_type_menu.set_active_id(stop_info_dict['type'])
        self._stop_number_spinbox.set_value(stop_info_dict['number'])
        self._stop_date_picker.picker.datetime = stop_info_dict['date']
        self.update_stop_info()

    @property
    def recurrence_dict(self):
        return {
            'enabled': self.enabled,
            'increment': self.increment,
            'interval': self.interval,
            'weekdays': self.weekdays,
            'weekday_of_month': self.weekday_of_month,
            'stop_info': self.stop_info
        }

    @recurrence_dict.setter
    def recurrence_dict(self, recurrence_dict):
        self.enabled = recurrence_dict['enabled']
        self.increment = recurrence_dict['increment']
        self.interval = recurrence_dict['interval']
        self.weekdays = recurrence_dict['weekdays']
        self.weekday_of_month = recurrence_dict['weekday_of_month']
        self.stop_info = recurrence_dict['stop_info']

    @property
    def recurrence_object(self):
        return Recurrence(
            enabled=self.enabled, interval=self.interval, increment=self.increment, weekdays=self.weekdays,
            weekday_of_month=self.weekday_of_month, stop_info=self.stop_info)

    @recurrence_object.setter
    def recurrence_object(self, recurrence: Recurrence):
        self.enabled = recurrence.enabled
        self.increment = recurrence.increment
        self.interval = recurrence.interval
        self.weekdays = recurrence.weekdays.dict
        self.weekday_of_month = recurrence.weekday_of_month.dict
        self.stop_info = recurrence.stop_info.dict


class RecurrenceButton:
    def __init__(self):
        self.button = Gtk.Button()
        self.popover = RecurrencePopover()
        self.button.show()
        self.button.connect('clicked', self._on_button_clicked)
        self.popover.set_relative_to(self.button)
        self.popover.connect_popover_closed_signals(self._on_popover_closed)
        self.popover.connect_recurrence_changed_signal(self._on_recurrence_changed)
        self._update_button_label()

    def _on_button_clicked(self, *_):
        self.popover.raise_popover()

    def _on_popover_closed(self, *_):
        self._update_button_label()

    def _on_recurrence_changed(self, *_):
        self._update_button_label()

    def _update_button_label(self):
        recurrence = self.popover.recurrence_object
        self.button.set_label("Repeats " + recurrence.string if recurrence.enabled else "Select Recurrence")
