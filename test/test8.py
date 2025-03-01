# -*- coding: utf-8 -*-
import logging
from typing import Dict, Any
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import Ollama

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaQAExpert:
    def __init__(self):
        # 初始化模型
        self.models = {
            'validator': Ollama(base_url="http://localhost:11434", model="llama3.2"),
            'enhancer': Ollama(model="qwen2.5"),
            'fast': Ollama(model="phi3")
        }
        
        # 构建工具链
        self.knowledge_tool = self._create_knowledge_tool()
        self.agent_executor = self._build_validation_agent()
        self.workflow = self._construct_workflow()
        
        # 初始化统计
        self.stats = {'total': 0}

    def _create_knowledge_tool(self) -> Tool:
        """创建知识检索工具"""
        return Tool(
            name="KnowledgeSearch",
            func=self._search_knowledge,
            description="用于访问本地知识库的核心工具，输入应为完整问题"
        )

    def _search_knowledge(self, query: str) -> str:
        """知识库查询实现"""
        knowledge = {
            "langchain": "LangChain是用于构建LLM应用的开源框架，支持模块化组件和链式调用",
            "ollama": "Ollama是本地大模型部署平台，支持多模型管理和GPU加速推理"
        }
        return knowledge.get(query.strip().lower(), "无匹配结果")

    def _build_validation_agent(self) -> AgentExecutor:
        """修复模板参数冲突问题"""
        prompt_template = """请严格按以下格式处理：

        可用工具：
        {tools}

        必须使用工具名称（仅限以下选项）：
        {tool_names}

        问题：{input}

        思考过程：
        {agent_scratchpad}
        """

        # 关键修复点：移除input_variables参数
        prompt = PromptTemplate.from_template(template=prompt_template)
        
        agent = create_react_agent(
            llm=self.models['validator'],
            tools=[self.knowledge_tool],
            prompt=prompt
        )
        return AgentExecutor(
            agent=agent, 
            tools=[self.knowledge_tool], 
            handle_parsing_errors=True,
            verbose=True
        )

    def _construct_workflow(self) -> Any:
        """构建处理流程"""
        def route_logic(data: Dict) -> Dict:
            self.stats['total'] += 1
            result = self.agent_executor.invoke(data)
            return {
                "output": result["output"],
                "question": data["input"]
            }

        return RunnablePassthrough() | route_logic

    def query(self, question: str) -> str:
        """执行查询"""
        try:
            response = self.workflow.invoke({"input": question})
            return response["output"]
        except Exception as e:
            logger.error(f"Query failed: {str(e)}")
            return "系统暂时不可用，请稍后再试"

if __name__ == "__main__":
    # 初始化系统
    qa_system = OllamaQAExpert()
    
    # 测试用例
    test_cases = [
        "LangChain是什么？",
        "Ollama的主要功能？",
        "如何训练大模型？"
    ]
    
    for q in test_cases:
        print(f"\n【问题】{q}")
        print(f"【回答】\n{qa_system.query(q)}")
        print("="*50)å
    
    print(f"\n总查询次数：{qa_system.stats['total']}")
