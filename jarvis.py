import platform
import subprocess
import webbrowser
from dataclasses import dataclass

import pyttsx3
import speech_recognition as sr


@dataclass
class CommandResult:
    handled: bool
    message: str
    should_exit: bool = False


class SpeechEngine:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 165)

    def speak(self, text: str) -> None:
        print(f"JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()


class CommandExecutor:
    def __init__(self) -> None:
        self.system = platform.system().lower()

    def execute(self, command: str) -> CommandResult:
        normalized = command.lower().strip()

        if normalized in {"çıkış", "kapat", "dur"}:
            return CommandResult(True, "Görüşürüz. JARVIS kapanıyor.", should_exit=True)

        if "tarayıcı" in normalized:
            webbrowser.open("https://www.google.com")
            return CommandResult(True, "Tarayıcıyı açtım.")

        if "hesap" in normalized:
            self._open_calculator()
            return CommandResult(True, "Hesap makinesini açtım.")

        if "dosya" in normalized or "finder" in normalized or "gezgin" in normalized:
            self._open_file_manager()
            return CommandResult(True, "Dosya yöneticisini açtım.")

        if "ekran" in normalized and "kilit" in normalized:
            self._lock_screen()
            return CommandResult(True, "Ekranı kilitledim.")

        if "ses aç" in normalized:
            self._volume_up()
            return CommandResult(True, "Sesi artırdım.")

        if "ses kıs" in normalized:
            self._volume_down()
            return CommandResult(True, "Sesi azalttım.")

        if "sessize" in normalized:
            self._mute()
            return CommandResult(True, "Sesi sessize aldım.")

        return CommandResult(False, "Bu komutu henüz bilmiyorum.")

    def _open_calculator(self) -> None:
        if "windows" in self.system:
            subprocess.run(["calc"], check=False)
        elif "darwin" in self.system:
            subprocess.run(["open", "-a", "Calculator"], check=False)

    def _open_file_manager(self) -> None:
        if "windows" in self.system:
            subprocess.run(["explorer"], check=False)
        elif "darwin" in self.system:
            subprocess.run(["open", "/"], check=False)

    def _lock_screen(self) -> None:
        if "windows" in self.system:
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=False)
        elif "darwin" in self.system:
            subprocess.run(
                ["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"],
                check=False,
            )

    def _volume_up(self) -> None:
        if "windows" in self.system:
            self._run_powershell(
                "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"
            )
        elif "darwin" in self.system:
            subprocess.run(["osascript", "-e", "set volume output volume ((output volume of (get volume settings)) + 10)"], check=False)

    def _volume_down(self) -> None:
        if "windows" in self.system:
            self._run_powershell(
                "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"
            )
        elif "darwin" in self.system:
            subprocess.run(["osascript", "-e", "set volume output volume ((output volume of (get volume settings)) - 10)"], check=False)

    def _mute(self) -> None:
        if "windows" in self.system:
            self._run_powershell(
                "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"
            )
        elif "darwin" in self.system:
            subprocess.run(["osascript", "-e", "set volume with output muted"], check=False)

    @staticmethod
    def _run_powershell(script: str) -> None:
        subprocess.run(["powershell", "-Command", script], check=False)


class JarvisAssistant:
    def __init__(self) -> None:
        self.speech = SpeechEngine()
        self.executor = CommandExecutor()
        self.recognizer = sr.Recognizer()
        self.wake_word = "jarvis"

    def start(self) -> None:
        self.speech.speak('Merhaba, ben JARVIS. Türkçe okunuşum "Jarvis". Hazırım.')
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            while True:
                text = self._listen_once(source)
                if not text:
                    continue

                if self.wake_word not in text.lower():
                    continue

                self.speech.speak("Seni dinliyorum.")
                command = self._listen_once(source)
                if not command:
                    self.speech.speak("Komutu duyamadım, tekrar eder misin?")
                    continue

                result = self.executor.execute(command)
                self.speech.speak(result.message)

                if result.should_exit:
                    break

    def _listen_once(self, source: sr.Microphone) -> str:
        try:
            audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=7)
            text = self.recognizer.recognize_google(audio, language="tr-TR")
            print(f"SEN: {text}")
            return text
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            self.speech.speak("Konuşma servisinde bağlantı hatası var.")
            return ""


if __name__ == "__main__":
    JarvisAssistant().start()
