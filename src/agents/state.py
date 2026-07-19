"""State definitions for LangGraph."""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ConversationState:
    """State object for conversation management."""

    session_id: str
    user_id: str
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    extracted_slots: Dict[str, Any] = field(default_factory=dict)
    required_slots: List[str] = field(default_factory=list)
    pending_slots: List[str] = field(default_factory=list)
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    iteration_count: int = 0
    last_message: str = ""
    is_complete: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def add_message(self, role: str, content: str) -> None:
        """Add a message to conversation history.

        Args:
            role: 'user' or 'assistant'
            content: Message content
        """
        self.conversation_history.append({"role": role, "content": content})
        self.last_message = content
        self.updated_at = datetime.utcnow()

    def extract_slot(self, slot_name: str, value: str, confidence: float) -> None:
        """Extract and store a slot value.

        Args:
            slot_name: Name of the slot
            value: Extracted value
            confidence: Confidence score (0-1)
        """
        self.extracted_slots[slot_name] = value
        self.confidence_scores[slot_name] = confidence
        if slot_name in self.pending_slots:
            self.pending_slots.remove(slot_name)

    def is_form_complete(self) -> bool:
        """Check if all required slots are filled.

        Returns:
            True if all required slots have values
        """
        return all(slot in self.extracted_slots for slot in self.required_slots)
