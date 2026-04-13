#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="emma-ia",
    version="0.3.0",
    description="Emma - IA Bot for Discord",
    author="gamesdoguin-eng",
    python_requires=">=3.12",
    packages=find_packages(),
    install_requires=[
        "discord.py",
        "groq",
        "python-dotenv",
        "torch",
        "torchaudio",
        "pyaudio",
        "requests",
        "edge-tts",
        "pygame",
        "keyboard",
        "pillow",
        "openai",
        "numpy",
    ],
)
