"""
Sapphire Standard Library Exports
"""
from src.stdlib.os_mod import OSModule
from src.stdlib.fs_mod import FSModule
from src.stdlib.http_mod import HTTPModule
from src.stdlib.gui_mod import GUIModule
from src.stdlib.ai_mod import AIModule
from src.stdlib.data_mod import DataModule
from src.stdlib.scheduler_mod import SchedulerModule
from src.stdlib.ml_mod import MLModule
from src.stdlib.agent_mod import AgentModule

STDLIB = {
    "os": OSModule,
    "fs": FSModule,
    "http": HTTPModule,
    "gui": GUIModule,
    "ai": AIModule,
    "data": DataModule,
    "scheduler": SchedulerModule,
    "ml": MLModule,
    "agent": AgentModule,
}
