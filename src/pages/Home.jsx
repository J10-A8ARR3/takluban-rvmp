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

  const handleDetect = async () => {
    try {
      const response = await fetch("/detect_language", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `text=${encodeURIComponent(inputText)}`,
      });

      const data = await response.json();

      setDetectedLanguage(data.predicted_language || "Error detecting language");
      setPosTaggedSentence(data.pos_tagged_sentence || "Error processing the sentence.");
      setCensoredSentence(data.censored_sentence || "Error processing the sentence.");
    } catch (error) {
      console.error("Error:", error);
      setDetectedLanguage("Error detecting language");
      setPosTaggedSentence("Error processing the sentence.");
      setCensoredSentence("Error processing the sentence.");
    }
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
