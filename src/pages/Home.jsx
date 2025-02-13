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
    let text = e.target.value;
    let words = text.trim().split(/\s+/);
    let wordsLeft = maxWords - words.length;

    if (words.length > maxWords) {
      text = words.slice(0, maxWords).join(" ") + " ";
      wordsLeft = 0;
    }

    setWordsLeft(wordsLeft >= 0 ? wordsLeft : 0);
    setInputText(text);
  };

  const handleDetect = () => {
    if (!inputText.trim()) {
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
          setDetectedLanguage(data.predicted_language || "No data available");
          setPosTaggedSentence(data.pos_tagged_sentence || "No data available");
          setCensoredSentence(data.censored_sentence || "No data available");
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
