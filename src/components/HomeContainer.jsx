import React from "react";

const HomeContainer = ({
  handleTextChange,
  wordsLeft,
  handleDetect,
  inputText,
  detectedLanguage,
  posTaggedSentence,
  censoredSentence,
}) => {
  return (
    <div className="flex-grow p-5 flex justify-center items-center mt-10">
      <div className="container flex justify-center items-start gap-6">
        {/* Left container */}
        <div className="left w-[600px] h-[700px] bg-[#F9EFEF] shadow-lg rounded-lg p-6 relative flex flex-col justify-between">
          <textarea
            className="w-full h-[calc(100%-60px)] bg-[#F9EFEF] p-5 rounded-md text-lg italic placeholder-opacity-50 focus:outline-none resize-none overflow-y-auto"
            placeholder="To detect profanities, input text here and click 'DETECT'."
            value={inputText} // Controlled input
            onChange={handleTextChange}
          />
          <div className="text-left mt-4 font-bold text-xl">
            Allowed number of words remaining: {wordsLeft}
          </div>
          <div className="detect-button-container flex justify-center items-center absolute bottom-5 right-5 w-[146px] h-[40px] bg-[#800000] rounded-lg">
            <button
              onClick={handleDetect}
              className="detect-button text-white font-semibold text-[20px] bg-none border-none cursor-pointer hover:text-yellow-500"
            >
              DETECT
            </button>
          </div>
        </div>

        {/* Right container */}
        <div className="right flex flex-col gap-6">
          <div className="module-1 w-[600px] h-[150px] bg-[#F9EFEF] shadow-lg rounded-lg p-6">
            <div className="module-title text-[#800000] text-[25px] font-bold mb-2">
              FILIPINO NATIVE LANGUAGE IDENTIFIED:
            </div>
            <div className="text-center text-lg">{detectedLanguage || "No data available"}</div>
          </div>

          <div className="module-2 w-[600px] h-[300px] bg-[#F9EFEF] shadow-lg rounded-lg p-6">
            <div className="module-title text-[#800000] text-[25px] font-bold mb-2">
              POS TAGGED SENTENCE:
            </div>
            <div className="text-center text-lg">{posTaggedSentence || "No data available"}</div>
          </div>

          <div className="module-3 w-[600px] h-[200px] bg-[#F9EFEF] shadow-lg rounded-lg p-6">
            <div className="module-title text-[#800000] text-[25px] font-bold mb-2">
              CENSORED OR CLEAN SENTENCE:
            </div>
            <div className="text-center text-lg">{censoredSentence || "No data available"}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomeContainer;
