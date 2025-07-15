# # src/utils/error_logger.py
# import os
# from datetime import datetime

# class ErrorLogger:
#     def __init__(self, log_file):
#         self.log_file = log_file
#         os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

#     def log(self, message, context=None, suggestion=None):
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         with open(self.log_file, "a", encoding="utf-8") as f:
#             f.write(f"[{timestamp}] ERROR: {message}\n")
#             if context:
#                 f.write(f"  Context: {context}\n")
#             if suggestion:
#                 f.write(f"  Suggestion: {suggestion}\n")
#             f.write("-" * 60 + "\n")

#     def log_exception(self, exc, context=None, suggestion=None):
#         self.log(str(exc), context, suggestion)
import os
from datetime import datetime

class ErrorLogger:
    def __init__(self, log_file="logs/errors.log"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def log(self, message, context=None, suggestion=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] ERROR: {message}\n")
            if context:
                f.write(f"  Context: {context}\n")
            if suggestion:
                f.write(f"  Suggestion: {suggestion}\n")
            f.write("-" * 60 + "\n")

    def log_exception(self, exc, context=None, suggestion=None):
        self.log(str(exc), context, suggestion)
