import React, { useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { Menu, X } from "lucide-react";
import logo from "../assets/tklbn-logo.png";

const Navbar = () => {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(true);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <nav className="h-16 flex items-center justify-between bg-maroon px-6 font-montserrat relative">
      <div className="flex items-center">
        <img src={logo} alt="Takluban Logo" className="h-10" />
      </div>
      
      {/* Fixed position for the text */}
      <span className="text-white text-lg font-bold uppercase tracking-wide text-center absolute left-1/2 transform -translate-x-1/2">
        Filipino Native Language Profane Detection
      </span>
      
      <div className="flex items-center space-x-4">
        {isOpen && (
          <>
            <NavLink 
              to="/home" 
              className={({ isActive }) => 
                `text-white text-sm uppercase transition duration-300 hover:text-yellow-400 px-4 py-2 ${isActive ? 'font-bold' : ''}`
              }
            >
              Home
            </NavLink>
            <NavLink 
              to="/creator" 
              className={({ isActive }) => 
                `text-white text-sm uppercase transition duration-300 hover:text-yellow-400 px-4 py-2 ${isActive ? 'font-bold' : ''}`
              }
            >
              About Us
            </NavLink>
            <NavLink 
              to="/faqs" 
              className={({ isActive }) => 
                `text-white text-sm uppercase transition duration-300 hover:text-yellow-400 px-4 py-2 ${isActive ? 'font-bold' : ''}`
              }
            >
              FAQs
            </NavLink>
          </>
        )}
        {/* Burger Icon Always Visible */}
        <button 
          className="text-white focus:outline-none" 
          onClick={toggleMenu}
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
