"""Main conversational form agent using LangGraph."""

from typing import Optional
from logger import get_logger
from config import settings
from src.agents.state import ConversationState
from src.agents.tools import (
    extract_email,
    extract_phone,
    extract_name,
    calculate_confidence,
)

logger = get_logger(__name__)

class ConversationalFormAgent:
    """Agent for conversational form filling with state memory."""

    def __init__(
        self,
        required_slots: Optional[list] = None,
        session_id: str = "default_session",
    ):
        """Initialize the agent."""
        self.required_slots = required_slots or settings.required_slots
        self.session_id = session_id
        logger.info(f"Agent initialized with slots: {self.required_slots}")

    def extract_slots_from_message(self, state: ConversationState, text: str) -> ConversationState:
        """Extract slots from user message."""
        logger.info(f"Extracting slots from: {text}")
        
        if "email" in state.pending_slots:
            email = extract_email(text)
            if email:
                state.extract_slot("email", email, calculate_confidence(email, "email"))
                logger.info(f"✓ Extracted email: {email}")

        if "phone" in state.pending_slots:
            phone = extract_phone(text)
            if phone:
                state.extract_slot("phone", phone, calculate_confidence(phone, "phone"))
                logger.info(f"✓ Extracted phone: {phone}")

        if "name" in state.pending_slots:
            name = extract_name(text)
            if name and len(name.split()) >= 1:
                state.extract_slot("name", name, calculate_confidence(name, "name"))
                logger.info(f"✓ Extracted name: {name}")

        state.iteration_count += 1
        return state

    def generate_response(self, state: ConversationState) -> str:
        """Generate agent response."""
        next_slot = state.pending_slots[0] if state.pending_slots else None
        
        if next_slot:
            return f"Thank you! Could you please provide your {next_slot}?"
        else:
            extracted_info = ", ".join([f"{k}={v}" for k, v in state.extracted_slots.items()])
            return f"Great! I have all the information: {extracted_info}. Thank you for completing the form!"

    def process_message(self, user_message: str, state: Optional[ConversationState] = None) -> tuple:
        """Process a user message and return agent response."""
        if state is None:
            state = ConversationState(
                session_id=self.session_id,
                user_id="default_user",
                required_slots=self.required_slots,
                pending_slots=self.required_slots.copy(),
            )

        state.add_message("user", user_message)
        logger.info(f"User message: {user_message}")

        state = self.extract_slots_from_message(state, user_message)
        response = self.generate_response(state)
        state.add_message("assistant", response)
        state.is_complete = state.is_form_complete()
        
        logger.info(f"Agent response: {response}")
        logger.info(f"Extracted slots: {state.extracted_slots}")
        
        return response, state
