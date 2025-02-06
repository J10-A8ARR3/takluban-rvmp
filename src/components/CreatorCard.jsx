import React from 'react';

const CreatorCard = ({ creator }) => {
  return (
    <div className="w-[290px] h-[320px] p-4 bg-[#F9EFEF] shadow-md border-2 border-gray-300 rounded-md flex flex-col items-center text-center box-border">
      <img 
        src={creator.img} 
        alt={creator.name} 
        className="w-[170px] h-[190px] rounded-full object-cover shadow-md" 
      />
      <p className="text-lg font-bold">{creator.name}</p>
      <p className="text-md font-semibold italic">{creator.role}</p>
      <p className="text-sm font-bold">{creator.degree}</p>
      <p className="text-xs">{creator.school}</p>
    </div>
  );
};

export default CreatorCard;
