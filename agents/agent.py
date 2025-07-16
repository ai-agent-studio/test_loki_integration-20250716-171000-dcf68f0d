#!/usr/bin/env python3
"""
Generated agent: Test Agent with Loki
Factory function to create the agent with runtime context and enhanced memory.
"""

    LOKI_AVAILABLE = False
    LOKI_AVAILABLE = True
    from agent_studio.services.loggers import Logger as LokiLogger
    print('Warning: Loki logger not available. Logs will only go to console.')
# Loki integration for Grafana logging
except ImportError:
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from loguru import logger
from pathlib import Path
import os
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
try:

from typing import Optional
from textwrap import dedent

class MemoryEnabledTest_Agent_With_Loki:
    """Test Agent with Loki with enhanced conversation memory capabilities"""
    
    def __init__(self, user_id: str, session_id: str, debug_mode: bool = False):
        self.user_id = user_id
        self.session_id = session_id
        self.debug_mode = debug_mode
        self.agent = None
        self.conversation_history = []
        self.last_query_context = ""
        
        # Initialize Loki logger for Grafana
        if LOKI_AVAILABLE:
            self.loki_logger = LokiLogger(name='Test Agent with Loki', console_output=True, log_level='INFO')
            self.client_id = f'Test Agent with Loki-{user_id}-{session_id}'
        else:
            self.loki_logger = None
            self.client_id = f'Test Agent with Loki-{user_id}-{session_id}'
        
        self.setup_agent()
        
    def log_info(self, message: str, labels: dict = None):
        """Send info log to Loki and console"""
        if self.loki_logger:
            self.loki_logger.info(message, client_id=self.client_id, labels=labels or {})
        else:
            logger.info(f"[{self.client_id}] {message}")
    
    def log_error(self, message: str, labels: dict = None):
        """Send error log to Loki and console"""
        if self.loki_logger:
            self.loki_logger.error(message, client_id=self.client_id, labels=labels or {})
        else:
            logger.error(f"[{self.client_id}] {message}")
    
    def log_debug(self, message: str, labels: dict = None):
        """Send debug log to Loki and console"""
        if self.loki_logger:
            self.loki_logger.debug(message, client_id=self.client_id, labels=labels or {})
        else:
            logger.debug(f"[{self.client_id}] {message}")
    
    def setup_agent(self):
        """Initialize the agent with memory capabilities"""
        self.log_info(f"Setting up agent for user {self.user_id}, session {self.session_id}")
        
        model = OpenAIChat(name="gpt-4o", temperature=0.7, base_url=os.getenv("LLM_BASE_URL"), api_key=os.getenv("LLM_PROXY_API_KEY"))
        tools = None
        
        # Create agent with memory and runtime parameters
        self.log_info("Creating agent instance with memory capabilities")
        self.agent = Agent(
            user_id=self.user_id,
            session_id=self.session_id,
            debug_mode=self.debug_mode,
            model=model,
            tools=tools,
            name="Test Agent with Loki",
            instructions="""You are a test agent with Loki logging integration.
Help users with their questions and log all interactions to Grafana.
""",
            description="A test agent to verify Loki logging integration works correctly",
            agent_id="d3380f4a-0c75-4c7d-83e2-e37d7ed29e5c",
        )
        self.log_info("Agent setup completed successfully")
    
    def ask(self, question: str) -> str:
        """Ask a question with memory context and logging"""
        self.log_info(f"Processing question: {question[:100]}{'...' if len(question) > 100 else ''}")
        
        # Enhance question with context for follow-up queries
        enhanced_question = question
        follow_up_indicators = ["those", "that", "these", "same", "previous", "earlier", "them"]
        if any(indicator in question.lower() for indicator in follow_up_indicators):
            if self.last_query_context:
                enhanced_question = f"[CONTEXT: {self.last_query_context}]\n\nUser question: {question}"
                self.log_debug("Enhanced question with previous context")
        
        try:
            # Get response from agent
            self.log_debug("Sending question to agent for processing")
            response = self.agent.run(enhanced_question)
            
            # Extract content
            if hasattr(response, 'content'):
                agent_response = response.content
            else:
                agent_response = str(response)
            
            # Update context for next query
            self.update_context(question, agent_response)
            self.log_info(f"Successfully processed question, response length: {len(agent_response)} chars")
            return agent_response
        except Exception as e:
            error_msg = f"Error processing question: {str(e)}"
            self.log_error(error_msg)
            raise e
    
    def update_context(self, question: str, response: str):
        """Update context based on the latest query"""
        context_parts = []
        question_lower = question.lower()
        
        # Add context based on question content
        if "department" in question_lower:
            if "distribution" in question_lower or "count" in question_lower:
                context_parts.append("Previously analyzed department distribution")
            elif "satisfaction" in question_lower:
                context_parts.append("Previously analyzed job satisfaction by department")
        
        # Add more context patterns as needed
        if "employee" in question_lower:
            context_parts.append("Previously discussed employee data")
        
        self.last_query_context = ". ".join(context_parts)

def test_agent_with_loki_agent(
    user_id: str,
    session_id: str,
    model_id: str = "gpt-4o",
    debug_mode: bool = False,
) -> MemoryEnabledTest_Agent_With_Loki:
    """
    Factory function to create the agent with runtime context, enhanced memory, and Loki logging.
    """
    # Log agent creation
    if LOKI_AVAILABLE:
        creation_logger = LokiLogger(name='Test Agent with Loki-Factory', console_output=True, log_level='INFO')
        creation_logger.info(f"Creating Test Agent with Loki agent for user {user_id}, session {session_id}", client_id=f'Test Agent with Loki-Factory')
    else:
        logger.info(f"Creating Test Agent with Loki agent for user {user_id}, session {session_id}")
    
    return MemoryEnabledTest_Agent_With_Loki(user_id=user_id, session_id=session_id, debug_mode=debug_mode)