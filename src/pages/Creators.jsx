import React from 'react';
import { useSpring, animated } from 'react-spring'; // Importing react-spring hooks for animations
import CreatorCard from '../components/CreatorCard';

import Creator1 from '../assets/creators/tklbn-creator-1.png';
import Creator2 from '../assets/creators/tklbn-creator-2.png';
import Creator3 from '../assets/creators/tklbn-creator-3.png';
import Creator4 from '../assets/creators/tklbn-creator-4.png';
import TaklubanLogo from '../assets/tklbn-logo-xl.png'; // Logo import

const creators = [
  { name: 'ABARRE, Jeo C.', role: 'Developer', degree: 'BS Computer Science', school: 'Polytechnic University of the Philippines - Sta. Mesa, Manila', img: Creator1 },
  { name: 'BELEN, Annalyn P.', role: 'Developer', degree: 'BS Computer Science', school: 'Polytechnic University of the Philippines - Sta. Mesa, Manila', img: Creator2 },
  { name: 'GONZALES, Telisha B.', role: 'Developer', degree: 'BS Computer Science', school: 'Polytechnic University of the Philippines - Sta. Mesa, Manila', img: Creator3 },
  { name: 'LARANO, Randolph V.', role: 'Developer', degree: 'BS Computer Science', school: 'Polytechnic University of the Philippines - Sta. Mesa, Manila', img: Creator4 }
];

const Creators = () => {
  // Animation for the creator cards using react-spring
  const animationProps = useSpring({
    opacity: 1,
    transform: 'translateY(0px)',
    from: { opacity: 0, transform: 'translateY(30px)' },
    config: { tension: 200, friction: 20 }
  });

  return (
    <div className="flex flex-col md:flex-row justify-center items-center gap-10 px-6 py-10">
      {/* Left Side */}
      <div className="flex-1 max-w-lg flex flex-col items-center text-center">
        <h2 className="text-2xl font-bold mb-6">WHAT IS TAKLUBAN</h2>
        <img src={TaklubanLogo} alt="Takluban Logo" className="mb-6" />
        <div className="h-[353px] p-5 bg-[#F9EFEF] shadow-md border-2 border-gray-300 rounded-md">
          <p className="text-xl leading-snug">
            Derived from the Filipino word <b>'TAKLUBAN'</b>, meaning 'to cover,' this tool is designed to filter and protect online conversations by detecting and masking inappropriate Tagalog, Cebuano, and Bikol languages.
          </p>
          <p className="text-xl leading-snug mt-4">
            <b>TAKLUBAN</b>, a tool developed for an undergraduate thesis, ensures a respectful and safe digital environment for Filipinos, shielding users from offensive content.
          </p>
        </div>
      </div>
      
      {/* Right Side */}
      <div className="flex-1 max-w-lg text-center">
        <h2 className="text-2xl font-bold mb-5">MEET THE CREATORS</h2>
        <div className="grid grid-cols-2 gap-3 gap-x-25">
          {creators.map((creator, index) => (
            <animated.div style={animationProps} key={index}> {/* Apply animation to each card */}
              <CreatorCard creator={creator} />
            </animated.div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Creators;
