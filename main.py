"""Main entry point for the conversational form filler."""

import sys
from logger import get_logger
from src.agents.form_agent import ConversationalFormAgent
from src.agents.state import ConversationState

logger = get_logger(__name__)

def main():
    """Main function - interactive CLI."""
    logger.info("="*70)
    logger.info("Starting Conversational Form Filler")
    logger.info("="*70)
    
    agent = ConversationalFormAgent()
    state = ConversationState(
        session_id="demo_session_001",
        user_id="demo_user",
        required_slots=agent.required_slots,
        pending_slots=agent.required_slots.copy(),
    )

    print("\n" + "="*70)
    print(" INTERACTIVE CONVERSATIONAL FORM FILLER WITH STATE MEMORY")
    print("="*70)
    print("\n🧑 Welcome! I'll help you fill out a customer onboarding form.")
    print("   Type 'quit' to exit, 'reset' to start over.\n")
    print(f"📋 Session ID: {state.session_id}")
    print(f"📝 Required Fields: {', '.join(state.required_slots)}")
    print("-"*70 + "\n")

    conversation_turn = 1

    while True:
        try:
            if conversation_turn == 1:
                initial_response = "Hello! Welcome to our onboarding process. To get started, could you please tell me your full name?"
                print(f"Assistant: {initial_response}\n")
                state.add_message("assistant", initial_response)

            user_input = input("You: ").strip()

            if user_input.lower() == "quit":
                print("\n" + "-"*70)
                print("Thank you for using our service. Goodbye!")
                print("-"*70 + "\n")
                break

            if user_input.lower() == "reset":
                state = ConversationState(
                    session_id="demo_session_001",
                    user_id="demo_user",
                    required_slots=agent.required_slots,
                    pending_slots=agent.required_slots.copy(),
                )
                conversation_turn = 0
                print("\n✓ Session reset. Let's start over!\n")
                continue

            if not user_input:
                continue

            response, state = agent.process_message(user_input, state)
            print(f"\nAssistant: {response}\n")

            print("📋 Current Status:")
            if state.extracted_slots:
                print(f"   ✓ Extracted: {dict(state.extracted_slots)}")
            else:
                print(f"   ✓ Extracted: None yet")
            
            if state.pending_slots:
                print(f"   ⏳ Pending: {state.pending_slots}")
            else:
                print(f"   ⏳ Pending: All complete!")
            
            if state.confidence_scores:
                conf_str = ", ".join([f"{k}: {v:.0%}" for k, v in state.confidence_scores.items()])
                print(f"   📊 Confidence: {conf_str}")
            print()

            if state.is_form_complete():
                print("\n" + "="*70)
                print(" ✓ FORM COMPLETED SUCCESSFULLY!")
                print("="*70)
                print("\n📋 Extracted Customer Information:")
                print("-"*70)
                for slot, value in state.extracted_slots.items():
                    confidence = state.confidence_scores.get(slot, 0.0)
                    slot_display = slot.upper()
                    print(f"  • {slot_display:<15}: {value:<30} [Confidence: {confidence:.0%}]")
                print("-"*70)
                print(f"\n✓ Session Complete: {state.session_id}")
                print(f"  Total Conversation Turns: {conversation_turn}")
                print(f"  Total Messages: {len(state.conversation_history)}")
                if state.confidence_scores:
                    avg_confidence = sum(state.confidence_scores.values())/len(state.confidence_scores)
                    print(f"  Extraction Accuracy: {avg_confidence:.0%}")
                print("="*70 + "\n")
                break

            conversation_turn += 1

        except KeyboardInterrupt:
            print("\n\n" + "-"*70)
            print("Session interrupted by user.")
            print("-"*70 + "\n")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            print(f"\n⚠️  An error occurred: {e}")
            continue

if __name__ == "__main__":
    main()
