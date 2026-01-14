import logging
import sys
import os
import traceback
import json
from datetime import datetime
from supabase import create_client, Client

SUPABASE_URL = "https://vgmmwtrxrxlmuxgfbete.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZnbW13dHJ4cnhsbXV4Z2ZiZXRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE4MjI5OTYsImV4cCI6MjA3NzM5ODk5Nn0.9LmZxNYYDjrk_SfBTFvEw5H1uAm5Kto4dKKJ0axPn8E"

class Logger:
    def __init__(self, log_file='backend.log'):
        self.log_file = log_file
        self.supabase: Client = None
        self.supabase_enabled = False

        try:
            if SUPABASE_URL and SUPABASE_ANON_KEY:
                self.supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
                self.supabase_enabled = True
                print("Supabase logging enabled", file=sys.stdout)
            else:
                print("Supabase logging disabled (credentials not configured)", file=sys.stdout)
        except Exception as e:
            print(f"Failed to initialize Supabase client: {e}. Continuing without remote logging.", file=sys.stderr)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('ML_Pipeline')

    def _log_to_supabase(self, level, message, details=None, stack_trace=None):
        if not self.supabase_enabled or not self.supabase:
            return

        try:
            self.supabase.table('error_logs').insert({
                'source': 'backend',
                'level': level,
                'message': message,
                'details': details,
                'stack_trace': stack_trace
            }).execute()
        except Exception as e:
            print(f"Failed to log to Supabase: {e}", file=sys.stderr)

    def info(self, message, details=None):
        self.logger.info(message)
        self._log_to_supabase('info', message, details)

    def warning(self, message, details=None):
        self.logger.warning(message)
        self._log_to_supabase('warning', message, details)

    def error(self, message, exception=None, details=None):
        self.logger.error(message)
        stack_trace = None

        if exception:
            stack_trace = ''.join(traceback.format_exception(
                type(exception), exception, exception.__traceback__
            ))
            self.logger.error(f"Exception: {stack_trace}")

        if details is None:
            details = {}

        if exception:
            details['exception_type'] = type(exception).__name__
            details['exception_message'] = str(exception)

        self._log_to_supabase('error', message, details, stack_trace)

    def critical(self, message, exception=None, details=None):
        self.logger.critical(message)
        stack_trace = None

        if exception:
            stack_trace = ''.join(traceback.format_exception(
                type(exception), exception, exception.__traceback__
            ))
            self.logger.critical(f"Exception: {stack_trace}")

        if details is None:
            details = {}

        if exception:
            details['exception_type'] = type(exception).__name__
            details['exception_message'] = str(exception)

        self._log_to_supabase('critical', message, details, stack_trace)

    def log_experiment(self, experiment_data):
        if not self.supabase_enabled or not self.supabase:
            # Silently skip if Supabase is not configured
            return None

        try:
            result = self.supabase.table('experiments').insert(experiment_data).execute()
            self.info(f"Experiment saved to database: {experiment_data['dataset_id']}/{experiment_data['model_id']}")
            return result.data[0] if result.data else None
        except Exception as e:
            # Log the error but don't fail the experiment
            print(f"Failed to save experiment to database: {e}", file=sys.stderr)
            return None

global_logger = Logger()
