import sys
import PyQt4.QtCore as QtCore
from PyQt4.QtGui import QDialog, QDialogButtonBox, QApplication, QLabel, QVBoxLayout
from PyQt4.QtCore import Qt
import os
import errno
import threading
import pipereader

class SDDialog(QDialog):
    def __init__(self, parent = None):
        super(SDDialog, self).__init__(parent)

        layout = QVBoxLayout(self)

        self.display = QLabel()
        self.display.setText("SecureDrop message processing")
        layout.addWidget(self.display)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

messages = {
    # bootstrapping
    'EXISTING_SIGFILE': ("error", "Internal error: signal file given by caller already exists"),
    'POLLING_ERROR': {"error": "An internal error occurred while listening for events from VMs."},

    # sd-journalist
    'DOWNLOAD_FILE_MISSING': ("error", "The file downloaded from SecureDrop wasn't found."),
    'DOWNLOAD_BUNDLE_CREATED': ("success", "Initial download bundle created."),

    # decrypt
    'DECRYPTION_PROCESS_START': ("success", "Decryption process started."),
    'DECRYPTION_BUNDLE_OPEN_FAILURE': ("error", "Decryption bundle could not be opened."),
    'SUBMISSION_BUNDLE_UNBUNDLED': ("success", "Submission bundle looks valid."),
    'SUBMISSION_FILES_EXTRACTED': ("success", "Submission bundle files extracted."),
    'SUBMISSION_FILE_DECRYPTION_FAILED': ('error', "Submission file decryption failed."),
    'SUBMISSION_FILE_DECRYPTION_SUCCEEDED': ("success", "Submission file decrypted."),
    'SUBMISSION_DECRYPTED': ("success", "All submission files decrypted"),
}

def display(keyword):

    if keyword in messages:
        d.display.setText(messages[keyword][1])
    else:
        # XXX dev only, remove before deploying!
        d.display.setText("bad keyword: {}".format(keyword))

def poller_cb(poller, msg, err):
    # we're called with a keyword in `msg`. We look up that keyword
    # for the user-facing message to display.
    print("in poller_cb: {}".format(msg))
    display(msg.rstrip())


def create_sigfile(sigfile):
    # must be given a path to a file which does not already exist, and
    # can be created by this process

    if os.path.isfile(sigfile):
        display('EXISTING_SIGFILE')
    else:
        try:
            with open(sigfile,'a'):
                pass
        except Exception as e:
            display('BAD_SIGFILE')


if __name__ == '__main__':
    # we may be given the name of a file to create once we've started,
    # to signal to the invoking process that we're ready
    sigfile = sys.argv[1]

    app = QApplication([])
    d = SDDialog()

    reader = pipereader.PipeReader("myfifo", poller_cb)
    t = threading.Thread(target=reader.read)
    t.start()
    d.show()

    if sigfile != "":
        # tyvm https://stackoverflow.com/questions/6215690/how-to-execute-a-method-automatically-after-entering-qt-event-loop
        def on_start():
            create_sigfile(sigfile)

        QtCore.QTimer.singleShot(0, on_start)

    # blocks while the app runs.
    app.exec_()

    reader.quit()
    sys.exit()