from typing import Literal

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import ToolNode

from graph.tools import TOOLS

MODEL = ChatOpenAI(model='gpt-4o-mini', temperature=0).bind_tools(TOOLS)


def should_continue(state: MessagesState) -> Literal['tools', '__end__']:
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return 'tools'
    return END


def call_model(state: MessagesState):
    messages = state['messages']
    response = MODEL.invoke(messages)
    return {'messages': [response]}


def build_graph() -> CompiledGraph:
    workflow = StateGraph(MessagesState)

    workflow.add_node('agent', call_model)
    workflow.add_node('tools', ToolNode(TOOLS))

    workflow.set_entry_point('agent')

    workflow.add_edge('tools', 'agent')
    workflow.add_conditional_edges('agent', should_continue)

    checkpointer = MemorySaver()

    return workflow.compile(checkpointer=checkpointer)
