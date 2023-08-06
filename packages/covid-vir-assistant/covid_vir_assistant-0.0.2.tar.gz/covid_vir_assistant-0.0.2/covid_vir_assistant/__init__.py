import wx
import wikipedia
import wolframalpha
import pyttsx
import speech_recognition as sr

engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[-1].id)

engine.say('Welcome my boss! How can I help you?')
engine.runAndWait()

APP_ID = 'YOUR_APP_ID'

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
            pos=wx.DefaultPosition, size=wx.Size(450, 100),
            style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
             wx.CLOSE_BOX | wx.CLIP_CHILDREN,
            title="CauUt")
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel,
        label="Con có thể giúp gì cho cậu chủ?")
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER,size=(400,30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        self.Show()

    def OnEnter(self, event):
        question = self.txt.GetValue()
        question = question.lower()
        if question == '':
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                text_autio = r.recognize_google(audio)
                self.txt.SetValue(text_autio)
            except sr.UnknownValueError:
                engine.say("Google Speech Recognition could not understand audio")
                engine.runAndWait()
                print("Google Speech Recognition could not understand audio, please enter and try again")
                
            except sr.RequestError as e:
                engine.say("Could not request results from Google Speech Recognition service; {0}".format(e))
                engine.runAndWait()
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        else:
            try:
                #wolframalpha
                client = wolframalpha.Client(APP_ID)
                res = client.query(question)
                answer = next(res.results).text
                engine.say(answer)
                engine.runAndWait()
                print(answer)
            except:
                #wikipedia
                wikipedia.set_lang('en')
                answer = wikipedia.summary(question, sentences=2) 
                engine.say(answer)
                engine.runAndWait()
                print(answer)


if __name__ == "__main__":
    app = wx.App(True)
    frame = MyFrame()
    app.MainLoop()