import React, { useEffect, useState } from 'react';
import HomeContainer from '../components/HomeContainer';

const Home = () => {
  const [visited, setVisited] = useState(sessionStorage.getItem('visited'));
  const [wordsLeft, setWordsLeft] = useState(10);
  const maxWords = 10;

  useEffect(() => {
    if (visited) {
      // No loader, as it's removed
    } else {
      setTimeout(() => {
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
    <div className="bg-cover bg-center bg-fixed flex flex-col justify-center items-center">
      <HomeContainer
        handleTextChange={handleTextChange}
        wordsLeft={wordsLeft}
        handleDetect={handleDetect}
      />
    </div>
  );
};

export default Home;
