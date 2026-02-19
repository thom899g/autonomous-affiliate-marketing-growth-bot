import logging
from typing import Dict, Optional
import sentry_sdk

class BotMonitor:
    def __init__(self, dsn: str):
        self.sentry = sentry_sdk.init(dsn)
        
    def report_error(self, error: Exception, context: Optional[Dict] = None) -> None:
        """
        Reports an error to Sentry.
        Args:
            error: The exception that occurred.
            context: Additional context information.
        """
        try:
            self.sentry.capture_exception