from util import *
from window import Window
from PyQt4 import QtGui, uic, QtCore, Qt
from data_handle import *

class MainWindow(Window):
    def __init__(self):
        # Initially an empty list, until other windows are created
        self.child_windows = []

        # Create a new instance of the GUI container class
        self.gui = MainWindowGui()

        self.is_open = True

        # Extract the name of each molocule that hapi has data on and add it to
        # our list of molecule names in the gui
        for k, v in ISO.iteritems():
            (molecule_id, isotopologue_id) = k
            # The iso list includes molocules and their isotopologues, but if
            # isotopologue_id is 1 it means it is the normal molecule, so we add
            # it to the drop-down menu named molecule_id

            # Molecules with ID greater than 1000, as of right now, don't have
            # data in HITRAN that can be accessed
            if molecule_id >= 1000:
                continue
            if isotopologue_id == 1:
                self.gui.molecule_id.addItem(ISO[k][4])

        # Add all parameter groups to the parameter groups list.
        for (group, _) in PARAMETER_GROUPS.iteritems():
            item = QtGui.QListWidgetItem(group)
            item.setFlags(item.flags() |
            QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

            item.setCheckState(QtCore.Qt.Unchecked)

            self.gui.param_group_list.addItem(item)

        # Add all parameter groups to the parameter groups list.
        for par in PARLIST_ALL:
            item = QtGui.QListWidgetItem(par)
            item.setFlags(item.flags() |
            QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

            item.setCheckState(QtCore.Qt.Unchecked)

            self.gui.param_list.addItem(item)

        # Hide error messages
        self.gui.err_small_range.hide()
        self.gui.err_bad_connection.hide()
        self.gui.err_bad_iso_list.hide()

        # Connect the function to be executed when wn_max's value changes
        self.gui.wn_max.valueChanged.connect(
                                    lambda value: self.__wn_max_change(value))
        # Connect the function to be executed when wn_min's value changes
        self.gui.wn_max.valueChanged.connect(
                                    lambda value: self.__wn_max_change(value))
        # Calling this will populate the isotopologue list with isotopologues of
        # whatever the default selected molecule is. This has to be called after
        # the drop-down list is populated so there is something to be selected
        self.__molecule_id_index_changed()

        # Set the molecule_id change method to the one we defined in the class
        self.gui.molecule_id.currentIndexChanged.connect(
                                    lambda: self.__molecule_id_index_changed())

        # Set the fetch_button onclick method to the one we defined in the class
        self.gui.fetch_button.clicked.connect(
                                    lambda: self.__handle_fetch_clicked())

        # Set the clear_console button onckick method to the one defined in the class
        self.gui.clear_console.clicked.connect(
                                    lambda: self.__handle_clear_console_clicked())


        # Set the function for when an item gets clicked to the one defined in the class
        self.gui.iso_list.itemPressed.connect(
                                    lambda item: self.__iso_list_item_click(item))

        # Display the GUI since we're done configuring it
        self.gui.show()


    # Toggle the item that was activated
    def __iso_list_item_click(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)


    def __wn_max_change(self, value):
        max = self.gui.wn_max.maximum()
        if value > max:
            self.gui.wn_min.setValue(max)

    def __wn_min_change(self, value):
        min = self.gui.wn_min.minimum()
        if value < min:
            self.gui.wn_min.setValue(min)

    def fetch_error(self, errors):
        if not isinstance(errors, list):
            t = [errors]
            errors = t
        for err in errors:
            # This means the wavenumber range was too small (probably), so
            # we'll tell the user it is too small
            if err.error == FetchErrorKind.FailedToRetreiveData:
                self.gui.err_small_range.show()
                err_(' The entered wavenumber range is too small, try increasing it')
            # Not much to do in regards to user feedback in this case....
            elif err.error == FetchErrorKind.FailedToOpenThread:
                err_(' Failed to open thread to make query HITRAN')
            elif err.error == FetchErrorKind.BadConnection:
                self.gui.err_bad_connection.show()
                err_(' Error: Failed to connect to HITRAN. Check your internet connection and try again.')
            elif err.error == FetchErrorKind.BadIsoList:
                self.gui.err_bad_iso_list.show()
                err_(' Error: You must select at least one isotopologue.')

    def __handle_fetch_clicked(self):
        # Hide any error messages for now, if they persist they'll be shown
        # at the end of the method
        self.gui.err_small_range.hide()
        self.gui.err_bad_connection.hide()
        self.gui.err_bad_iso_list.hide()

        molecule = self.gui.get_selected_molecule_id()

        wn_max = self.gui.get_wn_max()
        wn_min = self.gui.get_wn_min()

        data_handle = DataHandle(self.gui.get_data_name())

        param_groups = self.gui.get_selected_param_groups()
        params = self.gui.get_selected_params()

        result = data_handle.try_fetch(
                                    self,
                                    self.gui.get_selected_isotopologues(),
                                    wn_min,
                                    wn_max,
                                    param_groups,
                                    params)

        # TODO: Handle the case where the fetch isn't successfull
        if result == True:
            return
        else:
            self.fetch_error(errors)


    def __handle_clear_console_clicked(self):
        self.gui.console_output.clear()

    # This method repopulates the isotopologue list widget after the molecule
    # that is being worked with changes.
    def __molecule_id_index_changed(self):
        # Get the local molecule id
        molecule_id = self.gui.get_selected_molecule_id()

        if molecule_id in MOLECULE_DATA_RANGE:
            # Get the range
            min, max = MOLECULE_DATA_RANGE[molecule_id]

            # Change the range for wn
            self.gui.wn_min.setMinimum(min)
            self.gui.wn_max.setMaximum(max)

            self.gui.wn_min.setValue(min)
            self.gui.wn_max.setValue(max)

        else:
            log_('No wavenumber range-data for molecule id ' + str(molecule_id))

        # Remove all old elements
        self.gui.iso_list.clear()

        # How many isotopologues this molecule has
        number_of_isos = MOLECULE_ID_TO_ISO_COUNT[molecule_id]

        # The keys to ISO in hapi are tuples of numbers (k, v), where k is the
        # molecule id and v is the isotopologue number. It must be taken into
        # account that the isotopologue numbers are not gaurenteed to be
        # sequential, and as things stand right now they skip some numbers. So
        # instead of iterating through 1..n, we iterate through every number
        # until we have added the appropriate number of isos to the list.

        # How many isotopologues we've added
        count = 0
        # the v in the (k, v) key we use to access ISO
        index = 0

        # while we havent added the appropriate number of items to list, keep
        # looking for an isotopologue.
        while count < number_of_isos:
            if not ((molecule_id, index) in ISO):
                index += 1
                continue

            isotopologue = ISO[(molecule_id, index)]

            # Create a new item, ensure it is enabled and can be checked.
            item = QtGui.QListWidgetItem()

            # Create a label to allow the rendering of rich text (fancy molecular formulas)
            label = QtGui.QLabel(ISOTOPOLOGUE_NAME_TO_HTML[isotopologue[1]])

            # Ensure we can use html
            label.setTextFormat(QtCore.Qt.RichText)

            # Make sure there is a key associated with the item so we can use it later
            item.setData(QtCore.Qt.UserRole, isotopologue[1])
            item.setFlags(item.flags() |
                        QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

            # The normal molecule is always at index 1, and we always want that
            # molecule to be selected
            if index != 1: item.setCheckState(QtCore.Qt.Unchecked)
            else: item.setCheckState(QtCore.Qt.Checked)

            self.gui.iso_list.addItem(item)
            self.gui.iso_list.setItemWidget(item, label)
            count += 1
            index += 1


    def open_graph_window(self):
        # Open a fetch window
        self.child_windows.append(GraphWindow())


    def close_window(self, to_close):
        # Close all occurences of the window to_close in the windows list.
        # There should only be one but you never know...
        self.child_windows = filter(
                        lambda window: window != to_close, self.child_windows)
        to_close.close()


    def close(self):
        for window in self.child_windows:
            if window.is_open:
                window.close()

        self.gui.close()


    def open(self):
        self.gui.open()

    @pyqtSlot(str)
    def append_text(self, text):
        self.gui.console_output.moveCursor(QtGui.QTextCursor.End)
        self.gui.console_output.insertPlainText(text)

class MainWindowGui(QtGui.QMainWindow):

    # Constructor for the gui - essentially just calls the parent constructor
    # and loads the ui layout
    def __init__(self):
        super(MainWindowGui, self).__init__()
        uic.loadUi('layouts/main_window.ui', self)


    # converts the selected molecule to a molecule id
    def get_selected_molecule_id(self):
        return MOLECULE_NAME_TO_LOCAL_ID[str(self.molecule_id.currentText())]

    # Returns a list containing all of the checked isotopologues
    def get_selected_isotopologues(self):
        selected_isos = []

        # Iterate through all of the items in the isotopologue list
        for i in xrange(self.iso_list.count()):

            # get the i'th item from the list
            item = self.iso_list.item(i)

            # Only add checked items
            if item.checkState() == QtCore.Qt.Checked:

                # Convert the item text to a string, and then convert that new
                # string into a number using the ISOTOPOLOGUE_NAME_TO_GLOBAL_ID
                # map, then add it to the list of selected isotopologues
                # We bound the QtCore.Qt.UserRole data for the element to be the key
                # value we need to use if it is checked - so access it and convert it
                # from QVarient, to QString, to String
                text = str(item.data(QtCore.Qt.UserRole).toString())
                selected_isos.append(ISOTOPOLOGUE_NAME_TO_GLOBAL_ID[text])

        return selected_isos


    # Returns a list containing all of the checked parameters
    def get_selected_params(self):
        selected_params = []

        # Look at each parameter and add the checked ones to the list
        for i in xrange(self.param_list.count()):

            item = self.param_list.item(i)

            if item.checkState() == QtCore.Qt.Checked:
                selected_params.append(str(item.text()))

        return selected_params


    # Returns a list containing all of the checked groups
    def get_selected_param_groups(self):
        selected_groups = []

        # Look at each group and add the checked ones to the list
        for i in xrange(self.param_group_list.count()):

            item = self.param_group_list.item(i)

            if item.checkState() == QtCore.Qt.Checked:
                selected_groups.append(str(item.text()))

        return selected_groups

    def get_data_name(self):
        return str(self.data_name.text())


    # Fetches the double value from the QDoubleSpinBox wn_max
    def get_wn_max(self):
        return self.wn_max.value()


    # Fetches the double value from the QDoubleSpinBox wn_min
    def get_wn_min(self):
        return self.wn_min.value()
