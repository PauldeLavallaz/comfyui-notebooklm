"""
NotebookLM Chat Node
────────────────────
Sends a message to an existing NotebookLM notebook and returns the response.
Supports follow-up conversations via conversation_id.
"""

import logging

logger = logging.getLogger("comfyui-notebooklm")

DEFAULT_MESSAGE = (
    "Necesito que crees una secuencia de prompts para Nano Banana para una "
    "publicidad en estilo [Claymotion] que represente todo lo que [PRODUCTO] "
    "mostraria en un anuncio de TV de 60 segundos. Genera los prompts de "
    "imagen para Nano Banana en orden para contar la mejor historia posible. "
    "Debe tener un inicio, desarrollo y cierre claros, y estar disenado para "
    "un anuncio de 60 segundos. Optimizalo para lograr un alto CTR en Facebook. "
    "Sos un marketer de elite con una creatividad sobresaliente."
)


class NotebookLM_ScriptGenerator:
    """Send a message to a NotebookLM notebook and get a response."""

    CATEGORY = "NotebookLM"
    FUNCTION = "send_message"
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("response", "conversation_id", "notebook_id")
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "notebook_id": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "placeholder": "Notebook ID (from notebooklm list)",
                    },
                ),
                "message": (
                    "STRING",
                    {
                        "default": DEFAULT_MESSAGE,
                        "multiline": True,
                    },
                ),
            },
            "optional": {
                "conversation_id": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "placeholder": "For follow-up messages (optional)",
                    },
                ),
            },
        }

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def send_message(
        self,
        notebook_id: str,
        message: str,
        conversation_id: str = "",
    ):
        from ..utils.notebooklm_cli import ask_question

        notebook_id = notebook_id.strip()
        if not notebook_id:
            raise ValueError("notebook_id is required. Run: notebooklm list")
        if not message.strip():
            raise ValueError("message is required")

        logger.info(f"Sending message to notebook {notebook_id[:8]}...")

        conv_id = conversation_id.strip() if conversation_id else None
        result = ask_question(notebook_id, message.strip(), conversation_id=conv_id)

        response = result.get("answer", "")
        new_conv_id = result.get("conversation_id", "")

        logger.info(f"Response: {len(response)} chars")

        return (response, new_conv_id, notebook_id)
