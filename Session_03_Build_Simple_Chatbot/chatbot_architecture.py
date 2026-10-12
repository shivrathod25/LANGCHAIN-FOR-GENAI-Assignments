"""
SESSION 3 - Task 1: LLM Chatbot Architecture Flow Diagram
Objective: Set up the project and print a text-based architecture diagram 
illustrating how user input is processed by a chatbot using LLMs and LangChain.
"""

def display_chatbot_architecture():
    diagram = r"""
========================================================================================
                 LANGCHAIN-POWERED LLM CHATBOT ARCHITECTURE
========================================================================================

   +------------------------+
   |       USER INPUT       |  e.g., "Who is the captain of Gujarat Titans?"
   +-----------+------------+
               |
               v
   +------------------------+
   | CONVERSATION MEMORY    |  Loads past dialogue history (ConversationBufferMemory)
   |  (Context Injection)   |  to maintain state and resolve references
   +-----------+------------+
               |
               v
   +------------------------+
   |    PROMPT TEMPLATE     |  Merges:
   | (System + Memory + Q)  |  1. Persona / System Rules ("You are a helpful sports bot")
   +-----------+------------+  2. Injected History ("User previously mentioned cricket")
               |               3. Current User Question
               v
   +------------------------+
   |   ROUTER / AGENT LOOP  |  Decides:
   |   (Reasoning Engine)   |  - Can LLM answer directly? -> Proceed to LLM
   +-----+------------+-----+  - Needs external tool/data? -> Call Tools / RAG Vector DB
         |            |
  [Need Data]    [Direct Answer]
         |            |
         v            v
   +-----------+  +-------------------------------------+
   | EXTERNAL  |  |      LARGE LANGUAGE MODEL (LLM)     |
   | TOOLS/RAG |  |       (e.g., GPT-3.5 / GPT-4o)      |
   +-----+-----+  +------------------+------------------+
         |                           ^
         +--- Observation / Data ----+
                                     |
                                     v
   +---------------------------------+------------------+
   |           OUTPUT PARSER & RESPONSE GUARDRAILS       |
   |       (Formats raw token stream into clean text)   |
   +---------------------------------+------------------+
                                     |
                                     v
   +---------------------------------+------------------+
   |          UPDATE MEMORY (Save Input + Output)       |
   +---------------------------------+------------------+
                                     |
                                     v
   +---------------------------------+------------------+
   |              FINAL ASSISTANT RESPONSE              |
   |   "Shubman Gill is the captain of Gujarat Titans!" |
   +----------------------------------------------------+
========================================================================================
"""
    print(diagram)

def main():
    display_chatbot_architecture()

if __name__ == "__main__":
    main()
