from model.silicon_flow_api import SiliconFlowLLMConfig,SiliconFlowLLM
from model.base import BaseLLM,BaseLLMConfig
# from tools import setup_logger
#
#
# logger = setup_logger(__name__)

# llm_registry = ComponentRegistry[SiliconFlowLLM]("llm", SiliconFlowLLMConfig, entry_point_group= "manual")
# llm_registry._components = {
#     "SiliconFlowInterface": SiliconFlowLLM,
#     "SiliconFlowChatLLMConfig":SiliconFlowLLMConfig,
#     "BaseLLM":BaseLLM
# }
#
# def create_llm(config: BaseLLMConfig) -> BaseLLM:
#
#     config_class_name = config.__class__.__name__
#     logger.info(f"Check the config class name:{config_class_name}")
#
#     if config_class_name.endswith("Config"):
#         llm_class_name = config_class_name[:-6]
#         logger.info(f"Check llm class name:{llm_class_name}")
#         try:
#             llm_class = llm_registry.get_component_class(llm_class_name)
#             logger.info(f"Manually registered components: {list(llm_registry._components.keys())}")
#             logger.info(f"Get llm {llm_class_name} registry successfully.")
#             return llm_class(config)
#         except ValueError:
#             logger.error(f"Failed to register {llm_class_name}")
#             pass
#
#     raise ValueError(f"Cannot Create LLM from Config: {config}")