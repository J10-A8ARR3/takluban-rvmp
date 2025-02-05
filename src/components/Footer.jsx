import React from 'react';
import footerIcon from '../assets/tklbn-favicon.png'; 

const Footer = () => {
  return (
    <footer className="bg-maroon text-white text-center py-2 text-sm fixed bottom-0 w-full mt-12">
      <img
        src={footerIcon} 
        alt="Footer Icon"
        className="h-5 inline align-middle"
      />
      <p className="inline-block text-sm align-middle ml-2">
        All Rights Reserved, 2024
      </p>
    </footer>
  );
};

export default Footer;
