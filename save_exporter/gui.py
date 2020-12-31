try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk
from tkcalendar import DateEntry
from save_fetcher import SaveFetcher

class Page(tk.Frame):
    """Class used for basic pages, with labels and maybe buttons."""

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.labels = []
        self.buttons = []
    
    def add_label(self, text):
        label = tk.Label(self, text=text)
        label.pack(padx=10, pady=10)
        self.labels.append(label)
    
    def change_label(self, text, num=0):
        self.labels[num]["text"] = text

    def add_button(self, text, func):
        button = tk.Button(self, text=text, command=func)
        button.pack(padx=10, pady=10)
        self.buttons.append(button)

class CredentialInput(Page):
    """Class used for pages with inputs."""

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.entries = []
    
    def add_entry(self, text, show=False):
        label = tk.Label(self, text=text)
        label.pack(padx=10, pady=10)
        self.labels.append(label)

        if show:
            cal = tk.Entry(self, show="*")
        else:
            cal = tk.Entry(self)
        cal.pack(padx=10, pady=10)
        self.entries.append(cal)

class CalendarSelect(Page):
    """Class used for pages with calendar inputs."""

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.calendars = []
    
    def add_calendar(self, text):
        label = tk.Label(self, text=text)
        label.pack(padx=10, pady=10)
        self.labels.append(label)

        cal = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2)
        cal.pack(padx=10, pady=10)
        self.calendars.append(cal)

class SaveFetcherGUI(tk.Frame):
    """Class that sets up the GUI for the save fetcher and handles running functions on SaveFetcher."""

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.save_fetcher = SaveFetcher()
        self.pages = self.page_setup()
        self.setup_gui()
        self.current_page = 0

    def page_setup(self):
        """Method that builds all of the pages used for this application."""

        pages = [CredentialInput(self), CalendarSelect(self), Page(self)]
        pages[0].add_entry("Username")
        pages[0].add_entry("Password", True)
        pages[0].add_label("Input your credentials here.")
        pages[1].add_calendar("From Date")
        pages[1].add_calendar("To Date")
        pages[1].add_label("Input the from and to dates here.")
        pages[2].add_label("Press the button to begin.")
        pages[2].add_button("Begin!", self.saved_posts)
        return pages

    def setup_gui(self):
        """Method that sets up the actual gui, including implementing the pages and other frames."""

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)

        buttonframe.pack(side="bottom", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        for page in self.pages:
            page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
            page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
            page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        self.button = tk.Button(buttonframe, text="next page", command=self.next_page)
        self.button.pack(side="top", anchor="center", pady=50)
        self.pages[0].lift()

    def next_page(self):
        """Method that determines what to do when the next page button is clicked."""

        if self.current_page + 1 < len(self.pages):
            if self.current_page == 0:
                result, err = self.save_fetcher.reddit_signin(self.pages[0].entries[0].get(), self.pages[0].entries[1].get())
            elif self.current_page == 1:
                result, err = self.save_fetcher.create_stamps(self.pages[1].calendars[0].get_date(), self.pages[1].calendars[1].get_date())
            else:
                return False

            if result:
                self.current_page += 1
                self.pages[self.current_page].lift()
                if self.current_page == 2:
                    self.button.pack_forget()
            else:
                self.pages[self.current_page].change_label(err, -1)

    def saved_posts(self):
        """Wrapper method that calls the main functionality in self.save_fetcher."""

        self.pages[2].buttons[-1].pack_forget()
        message = self.save_fetcher.saved_posts()
        self.pages[2].change_label(message, -1)

def main():
    """Main method that sets up the root frame and runs the program."""

    root = tk.Tk()
    main = SaveFetcherGUI(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.resizable(0, 0)
    root.mainloop()

if __name__ == "__main__":
    main()
