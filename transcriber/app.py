import json
import gradio as gr
import soundfile as sf
from numpy import arange
import matplotlib.pyplot as plt


def on_load(file):
    if file is None:
        return "No file uploaded", None

    with open(file.name) as f:
        data = json.load(f)

    audio_file_path = data["file_path"]
    frames = data["frame"]
    triads = data["triad"]

    waveform, sample_rate = sf.read(audio_file_path)

    fig, (ax_wave, ax_triads) = plt.subplots(
        2, 1, figsize=(14, 5),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True,
    )
    fig.tight_layout(pad=2)

    # Waveform in frames
    ax_wave.plot(arange(len(waveform)), waveform, linewidth=0.3, alpha=0.5, color="steelblue")

    ax_triads.set_yticks([])
    ax_triads.set_xlabel("Frames")
    ax_triads.set_title("Triads")

    info = (
        f"Audio: {audio_file_path}\n"
        f"Sample rate: {sample_rate:,} Hz  |  "
        f"Frames: {len(frames)}  |  "
        f"Duration: {max(frames)/sample_rate:.2f}s  |  "
        f"Unique triads: {len(set(triads))}"
    )
    return info, fig

# Gradio UI


with gr.Blocks() as demo:
    gr.Markdown("# Music transcriber")
    json_input = gr.File(label="Transcription artifact", file_types=[".json"])
    info_box = gr.Textbox(label="Description", lines=2)
    plot_out = gr.Plot(label="Waveform & triads")

    json_input.change(
        fn=on_load,
        inputs=json_input,
        outputs=[info_box, plot_out]
    )

demo.launch()
