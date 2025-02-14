import React, { useState } from "react";
import HomeContainer from "../components/HomeContainer";

const Home = () => {
  const [inputText, setInputText] = useState("");
  const [detectedLanguage, setDetectedLanguage] = useState(null);
  const [posTaggedSentence, setPosTaggedSentence] = useState(null);
  const [censoredSentence, setCensoredSentence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [wordsLeft, setWordsLeft] = useState(100); // Example word limit

  const handleTextChange = (e) => {
    const text = e.target.value;
    setInputText(text);
    setWordsLeft(10 - text.split(" ").length); // Example word limit logic
  };

  const handleDetect = async () => {
    if (!inputText.trim()) return;
    setLoading(true);
    
    try {
      const res = await fetch("http://localhost:5000/detect_language", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ sentence: inputText }),
      });

      const data = await res.json();
      setDetectedLanguage(data.language || "No data available");
      setPosTaggedSentence(data.pos_tagged || "No data available");
      setCensoredSentence(data.censored_sentence || "No data available");
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <HomeContainer
      handleTextChange={handleTextChange}
      wordsLeft={wordsLeft}
      handleDetect={handleDetect}
      inputText={inputText}
      detectedLanguage={detectedLanguage}
      posTaggedSentence={posTaggedSentence}
      censoredSentence={censoredSentence}
    />
  );
};

export default Home;
