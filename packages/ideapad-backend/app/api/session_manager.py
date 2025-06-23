

from app.models.model_runner import ModelRunner
from app.exceptions import ConversationNotFoundError, to_http_exception

# In-memory session store: conversation_id -> ModelRunner
_sessions: dict[str, ModelRunner] = {}

def add_runner(conversation_id: str, runner: ModelRunner):
    """Add a new runner to the session store."""
    _sessions[conversation_id] = runner

def get_runner_or_404(conversation_id: str) -> ModelRunner:
    """Retrieve a runner or raise 404 if not found."""
    runner = _sessions.get(conversation_id)
    if not runner:
        raise to_http_exception(ConversationNotFoundError())
    return runner

def pop_runner_or_404(conversation_id: str) -> ModelRunner:
    """Pop a runner or raise 404 if not found."""
    runner = _sessions.pop(conversation_id, None)
    if not runner:
        raise to_http_exception(ConversationNotFoundError())
    return runner