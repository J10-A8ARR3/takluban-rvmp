import React, { useEffect, useState } from "react";
import HomeContainer from "../components/HomeContainer";

const Home = () => {
  const [visited, setVisited] = useState(sessionStorage.getItem("visited"));
  const [wordsLeft, setWordsLeft] = useState(10);
  const [detectedLanguage, setDetectedLanguage] = useState("");
  const [posTaggedSentence, setPosTaggedSentence] = useState("");
  const [censoredSentence, setCensoredSentence] = useState("");
  const [inputText, setInputText] = useState("");

  const maxWords = 10;

  useEffect(() => {
    if (!visited) {
      setTimeout(() => {
        sessionStorage.setItem("visited", "true");
        setVisited(true);
      }, 5900);
    }
  }, [visited]);

  const handleTextChange = (e) => {
    let words = e.target.value.split(/\s+/).filter((word) => word.length > 0);
    let wordsLeft = maxWords - words.length;

    if (words.length > maxWords) {
      words = words.slice(0, maxWords);
    }

    setWordsLeft(wordsLeft >= 0 ? wordsLeft : 0);
    setInputText(words.join(" "));
  };

  const handleDetect = () => {
    const inputText = document.getElementById("text-area").value.trim();
  
    if (!inputText) {
      alert("Please enter text to detect language.");
      return;
    }
  
    fetch("http://127.0.0.1:5000/detect_language", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: inputText }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Response:", data);
        if (data.error) {
          alert(`Error: ${data.error}`);
        } else {
          document.getElementById("detected-language").innerText = data.predicted_language;
          document.getElementById("pos-tagged-sentence").innerText = data.pos_tagged_sentence;
          document.getElementById("censored-sentence").innerText = data.censored_sentence;
        }
      })
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="bg-cover bg-center bg-fixed flex flex-col justify-center items-center">
      <HomeContainer
        handleTextChange={handleTextChange}
        wordsLeft={wordsLeft}
        handleDetect={handleDetect}
        inputText={inputText}
        detectedLanguage={detectedLanguage}
        posTaggedSentence={posTaggedSentence}
        censoredSentence={censoredSentence}
      />
    </div>
  );
};

export default Home;
