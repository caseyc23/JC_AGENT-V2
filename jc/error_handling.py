"""Error handling utilities for JC Agent.

Provides retry logic, circuit breakers, and graceful degradation.
"""
from __future__ import annotations

import asyncio
import functools
import logging
import time
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class RetryExhausted(Exception):
    """Raised when all retry attempts are exhausted."""
    pass


class CircuitBreakerOpen(Exception):
    """Raised when circuit breaker is open (service unavailable)."""
    pass


def retry_with_backoff(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
):
    """Decorator for retrying functions with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for delay on each retry
        exceptions: Tuple of exception types to catch and retry
    
    Example:
        >>> @retry_with_backoff(max_attempts=3)
        ... def fetch_data():
        ...     response = requests.get("https://api.example.com/data")
        ...     response.raise_for_status()
        ...     return response.json()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            delay = initial_delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exception = exc
                    if attempt == max_attempts:
                        break
                    
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed: {exc}. "
                        f"Retrying in {delay:.1f}s...",
                        exc_info=True,
                    )
                    time.sleep(delay)
                    delay *= backoff_factor
            
            raise RetryExhausted(
                f"Failed after {max_attempts} attempts"
            ) from last_exception
        
        return wrapper
    return decorator


async def retry_with_backoff_async(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
):
    """Async version of retry_with_backoff decorator.
    
    Example:
        >>> @retry_with_backoff_async(max_attempts=3)
        ... async def fetch_data():
        ...     async with httpx.AsyncClient() as client:
        ...         response = await client.get("https://api.example.com/data")
        ...         response.raise_for_status()
        ...         return response.json()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            delay = initial_delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as exc:
                    last_exception = exc
                    if attempt == max_attempts:
                        break
                    
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed: {exc}. "
                        f"Retrying in {delay:.1f}s...",
                        exc_info=True,
                    )
                    await asyncio.sleep(delay)
                    delay *= backoff_factor
            
            raise RetryExhausted(
                f"Failed after {max_attempts} attempts"
            ) from last_exception
        
        return wrapper
    return decorator


class CircuitBreaker:
    """Circuit breaker pattern implementation for external service calls.
    
    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Service unavailable, requests fail immediately
    - HALF_OPEN: Testing if service recovered, limited requests allowed
    
    Example:
        >>> breaker = CircuitBreaker(failure_threshold=5, timeout=60)
        >>> 
        >>> @breaker
        ... def call_external_api():
        ...     response = requests.get("https://api.example.com/data")
        ...     response.raise_for_status()
        ...     return response.json()
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        expected_exceptions: tuple[type[Exception], ...] = (Exception,),
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exceptions = expected_exceptions
        
        self.failure_count = 0
        self.last_failure_time: float | None = None
        self.state = "CLOSED"
    
    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            if self.state == "OPEN":
                if time.time() - self.last_failure_time >= self.timeout:
                    self.state = "HALF_OPEN"
                    logger.info("Circuit breaker transitioning to HALF_OPEN")
                else:
                    raise CircuitBreakerOpen(
                        f"Circuit breaker is OPEN. Service unavailable for {self.timeout}s."
                    )
            
            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except self.expected_exceptions as exc:
                self._on_failure()
                raise
        
        return wrapper
    
    def _on_success(self):
        """Handle successful call."""
        if self.state == "HALF_OPEN":
            logger.info("Circuit breaker recovered, transitioning to CLOSED")
            self.state = "CLOSED"
        self.failure_count = 0
    
    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.error(
                f"Circuit breaker OPENED after {self.failure_count} failures"
            )


def handle_errors(
    fallback_value: Any = None,
    log_exceptions: bool = True,
    reraise: bool = False,
):
    """Decorator for graceful error handling with fallback values.
    
    Args:
        fallback_value: Value to return on error
        log_exceptions: Whether to log caught exceptions
        reraise: Whether to re-raise exceptions after handling
    
    Example:
        >>> @handle_errors(fallback_value=[])
        ... def get_optional_data():
        ...     # Might fail, but returns [] instead of crashing
        ...     return requests.get("https://api.example.com/optional").json()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T | Any]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T | Any:
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                if log_exceptions:
                    logger.error(
                        f"Error in {func.__name__}: {exc}",
                        exc_info=True,
                    )
                if reraise:
                    raise
                return fallback_value
        
        return wrapper
    return decorator
