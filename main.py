"""
Outbound Course Lead Qualification Voice Agent
Silence-based recording + Deepgram STT
Conversation progresses based on user speech
"""

import os
import asyncio
from dotenv import load_dotenv

from agent.agent import CourseLeadAgent
from agent.policy_engine import PolicyEngine
from agent.router import Router
from memory.memory import ConversationMemory

from audio.recorder import SilenceRecorder
from stt.deepgram_stt import DeepgramSTT
from tts.deepgram_tts import DeepgramTTS
from audio.playback import AudioPlayer


# ------------------------------------------------------
# Environment
# ------------------------------------------------------

load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

if not DEEPGRAM_API_KEY:
    raise RuntimeError("DEEPGRAM_API_KEY not set in .env")


# ------------------------------------------------------
# Voice Agent
# ------------------------------------------------------

class VoiceLeadAgent:
    def __init__(self):
        # Memory
        self.memory = ConversationMemory()
        self.memory.start_session("voice_session_001")

        # Agent core
        self.agent = CourseLeadAgent(
            memory=self.memory,
            policy_engine=PolicyEngine(),
            router=Router()
        )

        # Audio + STT + TTS
        self.recorder = SilenceRecorder(
            start_timeout_ms=5000,
            silence_threshold=350.0,
            silence_duration_ms=900,
            max_record_ms=10000,
        )

        self.stt = DeepgramSTT(DEEPGRAM_API_KEY)
        self.tts = DeepgramTTS(DEEPGRAM_API_KEY)
        self.player = AudioPlayer(sample_rate=24000)

        # Conversation control
        self.no_response_count = 0

    # --------------------------------------------------

    async def speak(self, text: str):
        print(f"\n🤖 AGENT: {text}")
        audio = self.tts.synthesize(text)
        self.player.play(audio)

    # --------------------------------------------------

    async def listen_and_transcribe(self) -> str:
        """
        Record user speech → transcribe → return text
        """
        audio_bytes = self.recorder.record()

        print("🧠 Transcribing user speech...")
        transcript = self.stt.transcribe(audio_bytes)

        transcript = transcript.strip()
        if transcript:
            print(f"📝 STT RESULT: {transcript}")
        else:
            print("📝 STT RESULT: <empty>")

        return transcript

    # --------------------------------------------------

    async def run(self):
        print("=" * 60)
        print("🎓 Course Lead Qualification Voice Agent (Outbound)")
        print("=" * 60)

        # Agent starts the call
        await self.speak(
            "Hello, this is Jerry calling from Outlook. "
            "I noticed you attended the Gen AI Mastermind recently. "
            "Is this a good time to talk?"
        )

        # Main conversation loop
        while True:
            user_text = await self.listen_and_transcribe()

            # ----------------------------
            # CASE 1: USER DID NOT SPEAK
            # ----------------------------
            if not user_text:
                self.no_response_count += 1

                if self.no_response_count == 1:
                    await self.speak(
                        "Hello, just checking if you can hear me."
                    )
                    continue

                if self.no_response_count == 2:
                    await self.speak(
                        "No worries if now is not a good time."
                    )
                    continue

                if self.no_response_count >= 3:
                    await self.speak(
                        "I'll drop this call for now. "
                        "Feel free to reach out when it's convenient."
                    )
                    print("👋 Call ended due to no response.")
                    break

            # ----------------------------
            # CASE 2: USER SPOKE
            # ----------------------------
            self.no_response_count = 0

            print(f"\n👤 HUMAN: {user_text}")

            # Let agent decide next step
            response = self.agent.handle_input(user_text)

            await self.speak(response)


# ------------------------------------------------------
# Entrypoint
# ------------------------------------------------------

if __name__ == "__main__":
    try:
        asyncio.run(VoiceLeadAgent().run())
    except KeyboardInterrupt:
        print("\n👋 Call ended.")