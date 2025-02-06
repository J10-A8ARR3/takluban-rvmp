import React from 'react';
import CreatorCard from './CreatorCard';
import Creator1 from '../assets/creators/tklbn-creator-1.png';
import Creator2 from '../assets/creators/tklbn-creator-2.png';
import Creator3 from '../assets/creators/tklbn-creator-3.png';
import Creator4 from '../assets/creators/tklbn-creator-4.png';

const creators = [
  { name: 'ABARRE, Jeo C.', role: 'Developer', degree: 'BS Computer Science', school: 'Polytechnic University of the Philippines - Sta. Mesa, Manila', img: Creator1 },
  { name: 'BELEN, Annalyn P.', role: 'Developer', degree: 'BS Computer Science', school: 'Polytechnic University of the Philippines - Sta. Mesa, Manila', img: Creator2 },
  { name: 'GONZALES, Telisha B.', role: 'Developer', degree: 'BS Computer Science', school: 'Polytechnic University of the Philippines - Sta. Mesa, Manila', img: Creator3 },
  { name: 'LARANO, Randolph V.', role: 'Developer', degree: 'BS Computer Science', school: 'Polytechnic University of the Philippines - Sta. Mesa, Manila', img: Creator4 }
];

const Creators = () => {
  return (
    <div className="container">
      {/* Left Side */}
      <div className="left-container">
        <h2>WHAT IS TAKLUBAN</h2>
        <img src="/static/assets/tklbn-logo-xl.png" alt="Takluban Logo" className="takluban-logo" />
        <div className="rectangle">
          <p>
            Derived from the Filipino word <b>'TAKLUBAN'</b>, meaning 'to cover,' this tool is designed to filter and protect online conversations by detecting and masking inappropriate Tagalog, Cebuano, and Bikol languages.
          </p>
          <p>
            <b>TAKLUBAN</b>, a tool developed for an undergraduate thesis, ensures a respectful and safe digital environment for Filipinos, shielding users from offensive content.
          </p>
        </div>
      </div>
      
      {/* Right Side */}
      <div className="right-container">
        <h2>MEET THE CREATORS</h2>
        <div className="creators-grid">
          {creators.map((creator, index) => (
            <CreatorCard key={index} creator={creator} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Creators;
