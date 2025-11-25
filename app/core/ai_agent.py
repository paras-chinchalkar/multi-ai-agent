import os
from typing import Iterable, List, Union

from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.prebuilt import create_react_agent

from app.config.settings import settings


def _normalize_messages(raw_messages: Union[str, Iterable[str]]) -> List[HumanMessage]:
    """
    Convert the incoming payload (string or list of strings) into LangChain
    HumanMessage objects so the graph agent receives the structure it expects.
    """
    if isinstance(raw_messages, str):
        messages = [raw_messages]
    else:
        messages = list(raw_messages or [])
    return [HumanMessage(content=msg) for msg in messages if msg]


def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not configured")

    # Keep env vars in sync for downstream libraries that read from os.environ
    os.environ.setdefault("GROQ_API_KEY", settings.GROQ_API_KEY)
    if settings.TAVILY_API_KEY:
        os.environ.setdefault("TAVILY_API_KEY", settings.TAVILY_API_KEY)

    llm = ChatGroq(model=llm_id, groq_api_key=settings.GROQ_API_KEY)
    tools = []
    if allow_search:
        if not settings.TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY is required when web search is enabled")
        tools = [TavilySearchResults(max_results=2)]
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt or None,
    )
    state = {"messages": _normalize_messages(query)}
    response = agent.invoke(state)

    messages = response.get("messages", [])
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
    if not ai_messages:
        raise ValueError("Agent response did not contain any AI messages")
    return ai_messages[-1]