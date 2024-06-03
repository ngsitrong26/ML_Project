import gradio as gr
import numpy as np

def flip(im):
    return np.flipud(im)

demo = gr.Interface( 
    gr.Image(sources=["webcam"], streaming=True), 
    "image",
    live=True
)
demo.launch()