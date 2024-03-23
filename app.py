from flask import Flask, render_template, request, redirect
import speech_recognition as sr

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index_page():
    transcript = ""
    if request.method == "POST":
        print("Form data received")

        # validating the filename exists and if not we do the following:
        if "file" not in request.files:
            return redirect(request.url)
        # if blank file
        file = request.files["file"]  # getting the filename if it exists
        if file.filename == "":
            return redirect(request.url)

        # we have a valid file
        if file:
            recogniser = sr.Recognizer()  # creating a recogniser object
            audioFile = sr.AudioFile(
                file
            )  # creating the file to use with our recogniser
            with audioFile as source:
                audio = recogniser.record(source)
            # this is now our transcribed audiofile created using google's recogniser

            # this could fail so, we handle the possible failure
            try:
                # success if this prints
                transcript = recogniser.recognize_google(audio)
                # print("Google Speech Recognition thinks you said:\n" + transcript)
            except sr.UnknownValueError:
                # print("Google Speech Recognition could not understand audio")
                transcript = "Google Speech Recognition could not understand audio"
            except sr.RequestError as e:
                print(
                    "Could not request results from Google Speech Recognition service; {0}".format(
                        e
                    )
                )

    return render_template("index.html", transcript=transcript)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
