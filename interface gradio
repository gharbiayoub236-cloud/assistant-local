import gradio as gr
from main import repondre_agent, L


def repondre(message, historique):
    if not historique:
        L.clear()

    return repondre_agent(message)


interface = gr.ChatInterface(
    fn=repondre,
    title="",
    concurrency_limit=1
)

interface.launch(
    server_name="ip",
    server_port=,
    share=False,
    inbrowser=True
)
