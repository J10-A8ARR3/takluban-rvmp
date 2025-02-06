import React from 'react';

const CreatorCard = ({ creator }) => {
  return (
    <div className="creator-box">
      <img 
        src={`/static/assets/${creator.img}`} 
        alt={creator.name} 
        className="creator-image" 
      />
      <p className="creator-name">{creator.name}</p>
      <p className="creator-role">{creator.role}</p>
      <p className="creator-degree">{creator.degree}</p>
      <p className="creator-school">{creator.school}</p>
    </div>
  );
};

export default CreatorCard;
