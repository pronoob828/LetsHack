from django.forms import ClearableFileInput

class ClearableMultipleFileInput(ClearableFileInput):
    """When setting the initial value of this widget, provide a list of the File instances."""
    template_name = "documents/clearable_multiple_file_input.html"

    def is_initial(self, value):
        return bool(value)
