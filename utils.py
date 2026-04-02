import logging
import os
import sys
from typing import Tuple, List, Dict, Type, TypeVar, Generic, Optional, Any
from logging.handlers import RotatingFileHandler
from schema import ConversationTurn
from configs import LOG_LEVEL



def setup_logger(name: str = "app_logger", log_file: str = "./app.log", level=LOG_LEVEL):
    """
    Setup an advanced logger with file and console output, showing detailed error paths and function names.

    :param name: Logger name
    :param log_file: Log file path
    :param level: Log level, defaults to LOG_LEVEL from configs
    :return: Logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Prevent duplicate logging

    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler with rotation
    if log_file and not any(isinstance(h, RotatingFileHandler) for h in logger.handlers):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

logger = setup_logger()

def is_user_turn(messages: List[Dict[str, str]]) -> bool:
    """
    Check if it's the user's turn based on the last message.

    :param messages: List of message dictionaries containing "role" and "content".
    :return: True if the last message is from the user, False otherwise.
    """
    role_name = messages[-1]["role"]

    return messages and len(messages) > 0 and role_name == "user"


def is_assistant_turn(messages: List[Dict[str, str]]) -> bool:
    """
    Check if it's the assistant's turn based on the last message.

    :param messages: List of message dictionaries containing "role" and "content".
    :return: True if the last message is from the assistant, False otherwise.
    """
    return messages and len(messages) > 0 and messages[-1]["role"] == "assistant"


# T = TypeVar('T')
#
# class ComponentRegistry(Generic[T]):
#     """
#     A registry for discovering, loading, and instantiating components via entry points.
#
#     :param component_type: The type name of the component（Eg：attacker, judge）.
#     :param base_class: The expected base class or interface that all registered components should inherit from.
#     :param entry_point_group: The name of the entry point group to search for available components.
#     """
#     def __init__(self,
#                  component_type: str,
#                  base_class: Type[T],
#                  entry_point_group: str
#                  ):
#         self.component_type = component_type
#         self.base_class = base_class
#         self.entry_point_group = entry_point_group
#         self._components: Dict[str, Any] = {}
#         self._loaded = False
#         logger.info(f"Init ComponentRegistry：type={component_type}, group={entry_point_group}")
#
#     def _ensure_loaded(self):
#         """
#         Ensure that components have been discovered and loaded.
#         """
#         if not self._loaded:
#             logger.debug(f"Load component for the first time：{self.component_type}")
#             self._discover_components()
#             self._loaded = True
#
#     def _discover_components(self):
#         """
#         Discover available components using Python's entry point mechanism.
#         """
#         logger.debug(f"Using entry_point_group `{self.entry_point_group}` to discover components...")
#         try:
#             try:
#                 from importlib.metadata import entry_points
#
#                 eps = list(entry_points(group=self.entry_point_group))
#                 logger.debug(f"Discover {len(eps)} component's entry points")
#             except (ImportError, TypeError):
#                 from pkg_resources import iter_entry_points
#                 eps = list(iter_entry_points(group=self.entry_point_group))
#
#             for ep in eps:
#                 try:
#                     logger.debug(f"Registry entry point：{ep.name} -> {ep.value}")
#                     self._components[ep.name] = ep
#                 except Exception as e:
#                     import traceback
#                     logger.error(f"Failed to registry：{ep.name} - {e}")
#                     traceback.print_exc()
#         except Exception as e:
#             import traceback
#             logger.error(f"Error during discover components：{e}")
#             traceback.print_exc()
#
#     def get_component_class(self, name: str) -> Type[T]:
#         """
#         Retrieve and load the class for a registered component by name.
#
#         :param name: The name of the component to retrieve.
#         :return: The loaded component class.
#         :raises ValueError: If the component name is not found in the registry.
#         """
#         self._ensure_loaded()
#
#         if name not in self._components:
#             logger.error(f"Component {name} not found in registry.")
#             raise ValueError(f"Unknown {self.component_type}: {name}")
#
#         if hasattr(self._components[name], 'load'):
#             logger.info(f"Loading {name} to components...")
#             self._components[name] = self._components[name].load()
#
#         return self._components[name]
#
#     def create_component(self, config: Any) -> T:
#         """
#         Instantiate a component using the provided configuration.
#
#         :param config: Configuration object that includes the component class name.
#         :return: An instance of the component initialized with the provided config.
#         """
#         component_cls_name = getattr(config, f"{self.component_type}_cls")
#         logger.info(f"Creating component cls name:{component_cls_name}")
#
#         component_cls = self.get_component_class(component_cls_name)
#         logger.info(f"Get component cls:{component_cls}")
#
#         return component_cls(config)
