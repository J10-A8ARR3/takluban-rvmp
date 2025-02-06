import React, { useEffect, useState } from 'react';

const Home = () => {
  const [visited, setVisited] = useState(sessionStorage.getItem('visited'));
  const [wordsLeft, setWordsLeft] = useState(10);
  const maxWords = 10;

  useEffect(() => {
    if (visited) {
      document.getElementById('loader').style.display = 'none';
    } else {
      setTimeout(() => {
        document.getElementById('loader').style.display = 'none';
        sessionStorage.setItem('visited', 'true');
      }, 5900);
    }
  }, [visited]);

  const handleTextChange = (e) => {
    const words = e.target.value.split(/\s+/).filter(word => word.length > 0);
    const wordsLeft = maxWords - words.length;
    setWordsLeft(wordsLeft >= 0 ? wordsLeft : 0);
    if (words.length > maxWords) {
      e.target.value = words.slice(0, maxWords).join(' ');
      alert(`Word limit of ${maxWords} reached.`);
    }
  };

  const handleDetect = () => {
    const text = document.getElementById('text-area').value;

    fetch('/detect_language', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `text=${encodeURIComponent(text)}`,
    })
      .then(response => response.json())
      .then(data => {
        if (data.predicted_language) {
          document.getElementById('detected-language').innerText = `${data.predicted_language}`;
        } else {
          document.getElementById('detected-language').innerText = 'Error detecting language';
        }

        if (data.pos_tagged_sentence) {
          document.getElementById('pos-tagged-sentence').innerText = `${data.pos_tagged_sentence}`;
        }

        if (data.censored_sentence) {
          document.getElementById('censored-sentence').innerText = `${data.censored_sentence}`;
        } else {
          document.getElementById('censored-sentence').innerText = 'Error processing the sentence.';
        }
      })
      .catch(error => {
        console.error('Error:', error);
        document.getElementById('detected-language').innerText = 'Error detecting language';
        document.getElementById('pos-tagged-sentence').innerText = 'Error processing the sentence.';
        document.getElementById('censored-sentence').innerText = 'Error processing the sentence.';
      });
  };

  return (
    <div className="bg-cover bg-center bg-fixed min-h-screen flex flex-col justify-center items-center mt-8">
      <div id="loader" className="fixed inset-0 bg-black flex justify-center items-center z-50">
        <video autoPlay muted loop id="loadingVideo" className="w-full h-full object-cover">
          <source src="../static/assets/tklbn-loading.mp4" type="video/mp4" />
        </video>
      </div>

      {/* No more landingPage div, as it's handled in index.jsx */}
      <div className="flex-grow p-5 flex justify-center items-center">
        <div className="container flex justify-center items-start gap-6">
          {/* Left container */}
          <div className="left w-[600px] h-[700px] bg-[#F9EFEF] shadow-lg rounded-lg p-6 relative flex flex-col justify-between">
            <textarea
              id="text-area"
              className="w-full h-[calc(100%-60px)] bg-[#F9EFEF] p-5 rounded-md text-lg italic placeholder-opacity-50 focus:outline-none resize-none overflow-y-auto"
              placeholder="To detect profanities, input text here and click 'DETECT'."
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
              <div className="module-title text-[#800000] text-[25px] font-bold mb-2">FILIPINO NATIVE LANGUAGE IDENTIFIED:</div>
              <div id="detected-language" className="text-center text-lg"></div>
            </div>

            <div className="module-2 w-[600px] h-[300px] bg-[#F9EFEF] shadow-lg rounded-lg p-6">
              <div className="module-title text-[#800000] text-[25px] font-bold mb-2">POS TAGGED SENTENCE:</div>
              <div id="pos-tagged-sentence" className="text-center text-lg"></div>
            </div>

            <div className="module-3 w-[600px] h-[200px] bg-[#F9EFEF] shadow-lg rounded-lg p-6">
              <div className="module-title text-[#800000] text-[25px] font-bold mb-2">CENSORED OR CLEAN SENTENCE:</div>
              <div id="censored-sentence" className="text-center text-lg"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
